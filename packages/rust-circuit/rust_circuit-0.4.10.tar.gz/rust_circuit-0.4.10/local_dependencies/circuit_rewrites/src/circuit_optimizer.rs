use std::io::prelude::*;

use anyhow::Result;
use circuit_base::{
    module::{
        any_children_with_symbolic_sizes, any_modules, conform_all_modules,
        inline_single_callsite_modules,
    },
    self_funcs::{compiler_default_print, print_circuit_stats},
    CircuitNode, CircuitRc, ModuleSpec,
};
use num_bigint::BigUint;
use once_cell::sync::Lazy;
use pyo3::prelude::*;
use rr_util::{
    opt_einsum::EinsumSpec,
    py_types::{is_python_running, Tensor, PY_UTILS},
    python_println,
    repr::RustRepr,
    shape::Shape,
    timed,
    util::{apply_fn_until_same, HashBytes},
};
use rustc_hash::FxHashMap as HashMap;

use crate::{
    canonicalize::deep_canonicalize,
    compiler_heuristics::deep_maybe_distribute,
    compiler_strip::strip_names_and_tags,
    deep_rewrite::{
        compiler_simp, deep_heuristic_nest_adds, deep_optimize_einsums, deep_push_down_index_raw,
        SimpFnSubset,
    },
    module_rewrite::deep_module_remove_unused_inputs,
    scheduled_execution::{
        circuit_to_schedule, circuit_to_schedule_naive_toposort, schedule_out_many, Schedule,
    },
};

// a lot of the function boundries in this are there because it would be too hard to optimize things jointly
// not because we don't need to optimize things jointly
// like scheduling does impact whether you should distribute, but using that info would be
// difficult

#[pyclass]
#[derive(Debug, Clone)]
pub struct OptimizationSettings {
    #[pyo3(get, set)]
    pub verbose: usize,
    #[pyo3(get, set)]
    pub max_memory: usize,
    #[pyo3(get, set)]
    pub max_single_tensor_memory: usize,
    #[pyo3(get, set)]
    pub distribute_min_size: Option<usize>,
    #[pyo3(get, set)]
    pub scheduling_naive: bool,
    #[pyo3(get, set)]
    pub scheduling_simplify: bool,
    #[pyo3(get, set)]
    pub scheduling_timeout: usize,
    #[pyo3(get, set)]
    pub adjust_numerical_scale: bool,
    #[pyo3(get, set)]
    pub numerical_scale_min: f64,
    #[pyo3(get, set)]
    pub numerical_scale_max: f64,
    #[pyo3(get, set)]
    pub log_simplifications: bool,
    #[pyo3(get, set)]
    pub log_slow_einsums: bool,
    #[pyo3(get, set)]
    pub save_circ: bool,
    #[pyo3(get, set)]
    pub optimization_parallelism: Option<usize>,
    #[pyo3(get, set)]
    pub keep_all_names: bool,
    #[pyo3(get, set)]
    pub push_down_index: bool,
    #[pyo3(get, set)]
    pub deep_maybe_distribute: bool,
    #[pyo3(get, set)]
    /// plausibly this should instead by SimpFnSubset which defaults to compiler subset
    pub simp_fn_subset: SimpFnSubset,
}

impl Default for OptimizationSettings {
    fn default() -> Self {
        static NUM_CPUS: Lazy<usize> = Lazy::new(|| {
            std::thread::available_parallelism()
                .map_or(1, |x| x.get() - 2)
                .max(1)
                .min(8)
        });
        Self {
            verbose: 0,
            max_memory: 9_000_000_000,
            max_single_tensor_memory: 9_000_000_000,
            distribute_min_size: None,
            scheduling_naive: false,
            scheduling_timeout: 500,
            scheduling_simplify: true,
            adjust_numerical_scale: false,
            numerical_scale_min: 1e-8,
            numerical_scale_max: 1e8,
            log_simplifications: false,
            log_slow_einsums: false,
            save_circ: false,
            optimization_parallelism: Some(*NUM_CPUS),
            keep_all_names: false,
            push_down_index: true,
            deep_maybe_distribute: true,
            simp_fn_subset: SimpFnSubset::compiler_default(),
        }
    }
}

#[pymethods]
impl OptimizationSettings {
    #[new]
    #[pyo3(signature=(
        verbose = OptimizationSettings::default().verbose,
        max_memory = OptimizationSettings::default().max_memory,
        max_single_tensor_memory = OptimizationSettings::default().max_single_tensor_memory,
        distribute_min_size = None,
        scheduling_naive = OptimizationSettings::default().scheduling_naive,
        scheduling_timeout = OptimizationSettings::default().scheduling_timeout,
        scheduling_simplify = OptimizationSettings::default().scheduling_simplify,
        adjust_numerical_scale = OptimizationSettings::default().adjust_numerical_scale,
        numerical_scale_min = OptimizationSettings::default().numerical_scale_min,
        numerical_scale_max = OptimizationSettings::default().numerical_scale_max,
        log_simplifications = OptimizationSettings::default().log_simplifications,
        log_slow_einsums = OptimizationSettings::default().log_slow_einsums,
        save_circ = OptimizationSettings::default().save_circ,
        optimization_parallelism = OptimizationSettings::default().optimization_parallelism.unwrap(),
        keep_all_names = OptimizationSettings::default().keep_all_names,
        push_down_index = OptimizationSettings::default().push_down_index,
        deep_maybe_distribute = OptimizationSettings::default().deep_maybe_distribute,
        simp_fn_subset = OptimizationSettings::default().simp_fn_subset
    ))]
    fn new(
        verbose: usize,
        max_memory: usize,
        max_single_tensor_memory: usize,
        distribute_min_size: Option<usize>,
        scheduling_naive: bool,
        scheduling_timeout: usize,
        scheduling_simplify: bool,
        adjust_numerical_scale: bool,
        numerical_scale_min: f64,
        numerical_scale_max: f64,
        log_simplifications: bool,
        log_slow_einsums: bool,
        save_circ: bool,
        optimization_parallelism: Option<usize>,
        keep_all_names: bool,
        push_down_index: bool,
        deep_maybe_distribute: bool,
        simp_fn_subset: SimpFnSubset,
    ) -> Self {
        Self {
            verbose,
            max_memory,
            max_single_tensor_memory,
            distribute_min_size,
            scheduling_naive,
            scheduling_timeout,
            scheduling_simplify,
            adjust_numerical_scale,
            numerical_scale_min,
            numerical_scale_max,
            log_simplifications,
            log_slow_einsums,
            save_circ,
            optimization_parallelism,
            keep_all_names,
            push_down_index,
            deep_maybe_distribute,
            simp_fn_subset,
        }
    }
}

#[derive(Debug, Clone, Default)]
pub struct OptimizationCache {
    pub simplified: HashMap<HashBytes, Option<CircuitRc>>,
    pub distributed: HashMap<HashBytes, Option<CircuitRc>>,
    pub module_removed_unused: HashMap<HashBytes, Option<CircuitRc>>,
    pub flops: HashMap<HashBytes, BigUint>,
    pub sum_of_node_sizes: HashMap<HashBytes, BigUint>,
    pub canonicalized: HashMap<HashBytes, Option<CircuitRc>>,
    pub module_specs_scheduled_same_settings: HashMap<ModuleSpec, Schedule>,
    pub module_specs_expanded_shape: HashMap<(ModuleSpec, Vec<Shape>), CircuitRc>,
    pub module_specs_expanded: HashMap<(ModuleSpec, Vec<HashBytes>), CircuitRc>,
    pub stripped_names: HashMap<HashBytes, Option<CircuitRc>>,
    pub times_distributed: usize,
    pub simplification_log: Vec<&'static str>,
    pub slow_einsum_log: Vec<EinsumSpec>,
}

/// Note: you can't change the settings once anything's been cached
/// bc cache assumes same settings on everything
#[pyclass]
#[derive(Debug, Clone, Default)]
pub struct OptimizationContext {
    pub cache: OptimizationCache,
    pub settings: OptimizationSettings,
}
#[pymethods]
impl OptimizationContext {
    #[staticmethod]
    pub fn new_settings(settings: OptimizationSettings) -> Self {
        Self {
            cache: Default::default(),
            settings,
        }
    }

    pub fn stringify_logs(&self) -> String {
        format!(
            "let slow_einsums = {}; let simplifications= {};",
            self.cache.slow_einsum_log.repr(),
            self.cache.simplification_log.repr()
        )
    }
}

#[pyfunction]
#[pyo3(name = "optimize_circuit", signature=(circuit, settings = Default::default()))]
pub fn optimize_circuit_py(
    circuit: CircuitRc,
    settings: OptimizationSettings,
) -> Result<CircuitRc> {
    optimize_circuit(circuit, &mut OptimizationContext::new_settings(settings))
}

pub fn optimize_circuit(
    circuit: CircuitRc,
    context: &mut OptimizationContext,
) -> Result<CircuitRc> {
    let print_timings = context.settings.verbose >= 2;
    let circuit = if !context.settings.keep_all_names {
        timed!(strip_names_and_tags(circuit, context), 10, print_timings)
    } else {
        circuit
    };
    let circuit = conform_all_modules(circuit);
    let circuit = inline_single_callsite_modules(circuit);
    if is_python_running() && any_children_with_symbolic_sizes(circuit.clone()) {
        Python::with_gil(|py| {
            pyo3::PyErr::warn(
                py,
                PY_UTILS.optimizing_symbolic_size_warning.as_ref(py),
                "you're optimizing with symbolic sizes. This is not recommended!",
                1,
            )
        })?;
    }
    if is_python_running() && any_modules(circuit.clone()) {
        Python::with_gil(|py| {
            pyo3::PyErr::warn(
                py,
                PY_UTILS.optimizing_modules_warning.as_ref(py),
                "you're optimizing a circuit with modules. this is currently buggy, you might want to substitute_all_modules first",
                1,
            )
        })?;
    }
    let circuit = timed!(deep_canonicalize(circuit, context), 10, print_timings);
    if context.settings.verbose >= 4 {
        python_println!("Original Circuit");
        circuit.printu();
        print_circuit_stats(&circuit);
    }
    if context.settings.save_circ {
        let s = circuit.repru();
        let f_name = format!("cached_circ_{}.circ", circuit.info().hash_usize());
        python_println!("Save circ to {}", f_name);

        let mut file = std::fs::File::create(f_name).unwrap();
        file.write_all(s.as_bytes()).unwrap();
    }
    let circuit = timed!(compiler_simp(circuit, context), 10, print_timings);
    let circuit = timed!(
        apply_fn_until_same(&circuit, |x| deep_module_remove_unused_inputs(
            compiler_simp(x.clone(), context),
            &mut context.cache.module_removed_unused,
            false,
            true,
            true,
        )),
        10,
        print_timings
    );
    // originally tried push_down_index in compiler_simp, but that produced worse circuits
    // for unknown reasons, maybe i'll investigate
    let circuit = if context.settings.push_down_index {
        timed!(
            apply_fn_until_same(&circuit, |x| deep_push_down_index_raw(
                compiler_simp(x.clone(), context),
                None
            )),
            10,
            print_timings
        )
    } else {
        circuit
    };
    let circuit = timed!(compiler_simp(circuit, context), 10, print_timings);
    let circuit = timed!(deep_canonicalize(circuit, context), 10, print_timings);
    if context.settings.verbose >= 3 {
        python_println!("Simplified Circuit");
        compiler_default_print(&circuit);
        print_circuit_stats(&circuit);
    }
    let circuit = if context.settings.deep_maybe_distribute {
        timed!(
            apply_fn_until_same(&circuit, |x| {
                let distributed = deep_maybe_distribute(x.clone(), context);
                compiler_simp(distributed, context)
            }),
            10,
            print_timings
        )
    } else {
        circuit
    };

    let circuit = timed!(deep_canonicalize(circuit, context), 10, print_timings);
    if context.settings.verbose >= 3 {
        python_println!("Distributed Circuit");
        compiler_default_print(&circuit);
        print_circuit_stats(&circuit);
    }
    let circuit = timed!(deep_heuristic_nest_adds(circuit), 10, print_timings);
    let circuit = timed!(deep_canonicalize(circuit, context), 10, print_timings);

    let circuit = timed!(deep_optimize_einsums(circuit, context), 10, print_timings);

    let circuit = timed!(deep_canonicalize(circuit, context), 10, print_timings);
    if context.settings.verbose >= 3 {
        python_println!("Final Circuit");
        compiler_default_print(&circuit);
        print_circuit_stats(&circuit);
    }
    Ok(circuit)
}

#[pyfunction]
#[pyo3(signature=(circuit, settings = Default::default()))]
pub fn optimize_to_schedule(
    circuit: CircuitRc,
    settings: OptimizationSettings,
) -> Result<Schedule> {
    optimize_to_schedule_many(vec![circuit], settings)
}

#[pyfunction]
#[pyo3(signature=(circuits, settings = Default::default()))]
pub fn optimize_to_schedule_many(
    circuits: Vec<CircuitRc>,
    settings: OptimizationSettings,
) -> Result<Schedule> {
    let circuit = schedule_out_many(circuits);
    let context = &mut OptimizationContext::new_settings(settings.clone());
    let verbose = settings.verbose;
    if verbose > 0 {
        python_println!("Optimizing verbose {}", verbose)
    }
    let optimized_circuit = timed!(optimize_circuit(circuit, context), 10, verbose >= 1)?;
    let schedule = if settings.scheduling_naive {
        circuit_to_schedule_naive_toposort(optimized_circuit)?
    } else {
        timed!(
            circuit_to_schedule(optimized_circuit, context),
            10,
            verbose >= 1
        )?
    };
    if verbose > 1 {
        python_println!("{}", schedule.get_stats());
    }
    Ok(schedule)
}

#[pyfunction]
#[pyo3(signature=(circuit, settings = Default::default()))]
pub fn optimize_and_evaluate(circuit: CircuitRc, settings: OptimizationSettings) -> Result<Tensor> {
    Ok(optimize_and_evaluate_many(vec![circuit], settings)?
        .into_iter()
        .next()
        .unwrap())
}

/// in python, lots of functions take in collections of circuits and operate on them at once
/// with node caching for just that batch
/// because functions that take one circuit already cache nodes, it's convenient to compute multiple nodes
/// wrapping in generalfunction Output and then passing around as one circuit
/// generalfunction Output is removed in circuit_to_schedule before scheduling
#[pyfunction]
#[pyo3(signature=(circuits, settings = Default::default()))]
pub fn optimize_and_evaluate_many(
    circuits: Vec<CircuitRc>,
    settings: OptimizationSettings,
) -> Result<Vec<Tensor>> {
    let schedule = optimize_to_schedule_many(circuits, settings.clone())?;
    schedule.evaluate_many(settings)
}
