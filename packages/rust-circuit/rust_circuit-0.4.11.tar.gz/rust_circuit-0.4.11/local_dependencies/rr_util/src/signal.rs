use std::{
    ffi::{c_int, c_ulong},
    mem::MaybeUninit,
    process::abort,
    ptr,
};

use libc::{dladdr, sigaction, siginfo_t, sigset_t, stack_t, Dl_info};
use once_cell::sync::OnceCell;
use pyo3::exceptions::PyKeyboardInterrupt;

// https://github.com/lattera/glibc/blob/master/sysdeps/unix/sysv/linux/x86/sys/ucontext.h
#[repr(C)]
struct ucontext_t {
    pub uc_flags: c_ulong,
    pub uc_link: *mut ucontext_t,
    pub uc_stack: stack_t,
    pub uc_mcontext: mcontext_t,
    pub uc_sigmask: sigset_t,
}

#[repr(C)]
struct mcontext_t {
    pub gregs: [c_ulong; 23],
    pub _fpregs: *mut [c_ulong; 32],
    pub __reserved1: [c_ulong; 8],
}

// this is somewhat unreliable & hacky
// e.g. dladdr could in deadlock if called during e.g. dlopen
// also sometimes aborts w/ "fatal runtime error: failed to initiate panic, error 3"
// works w/o C-unwind (but maybe is less undefined with? idk)
// if breaks maybe see https://github.com/rust-lang/rust/issues/74990
extern "C-unwind" fn rust_circuit_signal_handler(
    signal: c_int,
    _info: *mut siginfo_t,
    ucontext: *mut ucontext_t,
) {
    let mut dl_info = Dl_info {
        dli_fname: ptr::null(),
        dli_fbase: ptr::null_mut(),
        dli_sname: ptr::null(),
        dli_saddr: ptr::null_mut(),
    };

    let should_panic = unsafe {
        let ip = (*ucontext).uc_mcontext.gregs[16];
        dladdr(ip as *const _, &mut dl_info);
        // println!("signal handler {signal}, ip {ip}");
        if dl_info.dli_fname.is_null() {
            false
        } else {
            let fname = std::ffi::CStr::from_ptr(dl_info.dli_fname)
                .to_str()
                .unwrap();
            // not always correct, e.g. can be rust_circuit -> libc
            // could walk the stack if libc but meh i think this's good enough
            fname.contains("rust_circuit")
        }
    };

    if should_panic {
        match signal {
            libc::SIGINT => {
                std::panic::panic_any(PyKeyboardInterrupt::new_err(
                    "SIGINT caught by rust_circuit signal handler",
                ));
            }
            _ => panic!("rust_circuit signal handler {signal}"),
        }
    } else {
        // println!("signal handler {signal}, not in rust_circuit, rerasing w/ chain...");
        let action = CHAIN_SIGACTION.get().unwrap();
        unsafe {
            sigaction(signal, action, ptr::null_mut());
            libc::raise(signal);
        }
    }
}

#[derive(Debug, PartialEq)]
enum SigHandler {
    SigHandler(extern "C" fn(c_int)),
    SigAction(extern "C" fn(c_int, *mut siginfo_t, *mut ucontext_t)),
    SigDfl,
    SigIgn,
}

static PREV_SIGHANDLER: OnceCell<SigHandler> = OnceCell::new();
static CHAIN_SIGACTION: OnceCell<sigaction> = OnceCell::new();

// used to set sigmask & sigaltstack etc correctly for previous handler
extern "C" fn chain_prev_handler(signal: c_int, info: *mut siginfo_t, ucontext: *mut ucontext_t) {
    assert!(signal == libc::SIGINT); // otherwise PREV_SIGHANDLER would need to be array for each signal

    // restore our signal handler
    let mut new_action: sigaction = unsafe { MaybeUninit::zeroed().assume_init() };
    new_action.sa_flags = libc::SA_SIGINFO & libc::SA_NODEFER;
    new_action.sa_sigaction = rust_circuit_signal_handler as usize;
    unsafe { sigaction(signal, &new_action, ptr::null_mut()) };

    // then call prev handler
    let prev_handler = PREV_SIGHANDLER.get().unwrap();
    match prev_handler {
        SigHandler::SigHandler(handler) => handler(signal),
        SigHandler::SigAction(handler) => handler(signal, info, ucontext),
        SigHandler::SigIgn => {}
        SigHandler::SigDfl => {
            println!("signal {signal} caught by rust_circuit signal handler but no previous handler set, aborting");
            abort();
        }
    }
}

// currently just catches SIGINT & turns it into a KeyboardInterrupt, could also catch SIGTERM if we wanted (& e.g. reraise it after unwinding but before returning to python)
pub fn install_signal_handler() {
    let mut new_action: sigaction = unsafe { MaybeUninit::zeroed().assume_init() };
    new_action.sa_flags = libc::SA_SIGINFO & libc::SA_NODEFER;
    new_action.sa_sigaction = rust_circuit_signal_handler as usize;
    let mut old_action: sigaction = unsafe { MaybeUninit::zeroed().assume_init() };
    unsafe { sigaction(libc::SIGINT, &new_action, &mut old_action) };

    if old_action.sa_sigaction == rust_circuit_signal_handler as usize {
        return;
    }

    let handler = if old_action.sa_sigaction == libc::SIG_DFL as usize {
        SigHandler::SigDfl
    } else if old_action.sa_sigaction == libc::SIG_IGN as usize {
        SigHandler::SigIgn
    } else if old_action.sa_flags & libc::SA_SIGINFO != 0 {
        SigHandler::SigAction(unsafe {
            std::mem::transmute::<*const (), _>(old_action.sa_sigaction as *const ())
        })
    } else {
        SigHandler::SigHandler(unsafe {
            std::mem::transmute::<*const (), _>(old_action.sa_sigaction as *const ())
        })
    };

    if let Some(prev_handler) = PREV_SIGHANDLER.get() {
        if *prev_handler != handler {
            panic!("rust_circuit signal handler already installed with different wrapped handler");
        }
    } else {
        PREV_SIGHANDLER.set(handler).unwrap();
        old_action.sa_flags |= libc::SA_SIGINFO;
        old_action.sa_sigaction = chain_prev_handler as usize;
        assert!(CHAIN_SIGACTION.set(old_action).is_ok());
    }
}
