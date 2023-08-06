use std::{
    borrow::Cow,
    fmt::Debug,
    hash::Hash,
    ops::{BitAnd, BitOr, Not},
    sync::Arc,
};

use anyhow::{Context, Result};
use num_bigint::BigUint;
use once_cell::{race::OnceBox, sync::Lazy};
use rr_util::{
    name::Name,
    shape::Shape,
    tensor_util::{TorchDeviceDtype, TorchDeviceDtypeOp},
    util::{ArcCow, HashBytes, NamedAxes},
    IndexSet,
};

use crate::{CircuitNode, CircuitRc};

pub struct CachedCircuitInfo {
    pub shape: Shape,
    pub flags: CircuitFlags,
    pub hash: HashBytes,
    pub device_dtype: TorchDeviceDtypeOp,
    pub named_axes: NamedAxes,
    pub free_symbols: Option<OnceBox<Arc<IndexSet<CircuitRc>>>>, // always Symbols
    pub name: Option<Name>,
    pub children: Vec<CircuitRc>,
}

impl CachedCircuitInfo {
    // leaves some fields undefined/default for now... TODO move more stuff here
    pub fn incomplete(
        name: Option<Name>,
        shape: Shape,
        children: Vec<CircuitRc>,
    ) -> Result<CachedCircuitInfo> {
        let ddt = compute_device_dtype(&children, || std::iter::empty())?;
        Ok(Self::with_device_dtype(name, shape, children, ddt))
    }
    pub fn with_device_dtype_extra<I>(
        name: Option<Name>,
        shape: Shape,
        children: Vec<CircuitRc>,
        device_dtype_extra: impl Fn() -> I,
    ) -> Result<Self>
    where
        I: Iterator<Item = TorchDeviceDtypeOp>,
    {
        let ddt = compute_device_dtype(&children, device_dtype_extra)?;
        Ok(Self::with_device_dtype(name, shape, children, ddt))
    }
    pub fn with_device_dtype(
        name: Option<Name>,
        shape: Shape,
        children: Vec<CircuitRc>,
        device_dtype: TorchDeviceDtypeOp,
    ) -> Self {
        let free_symbols = if children
            .iter()
            .all(|x| !x.is_symbol() && x.info().free_symbols.is_none())
        {
            None
        } else {
            Some(OnceBox::new())
        };
        CachedCircuitInfo {
            shape,
            flags: Default::default(),
            hash: Default::default(),
            device_dtype,
            named_axes: Default::default(),
            free_symbols,
            name,
            children,
        }
    }
}

impl Clone for CachedCircuitInfo {
    fn clone(&self) -> Self {
        Self {
            shape: self.shape.clone(),
            flags: self.flags,
            hash: self.hash,
            device_dtype: self.device_dtype,
            named_axes: self.named_axes.clone(),
            free_symbols: self.free_symbols.as_ref().map(|x| {
                let b = OnceBox::new();
                if let Some(y) = x.get() {
                    let _ = b.set(Box::new(y.clone()));
                };
                b
            }),
            name: self.name,
            children: self.children.clone(),
        }
    }
}

#[derive(Clone, Copy, Hash, Debug, Eq, PartialEq)]
pub struct CircuitFlags(pub u8);
impl CircuitFlags {
    pub const IS_CONSTANT: CircuitFlags = CircuitFlags(0b0001);
    pub const IS_EXPLICITLY_COMPUTABLE: CircuitFlags = CircuitFlags(0b0010);
    pub const CAN_BE_SAMPLED: CircuitFlags = CircuitFlags(0b0100);
    pub const USE_AUTONAME: CircuitFlags = CircuitFlags(0b1000);

    pub const NONE: CircuitFlags = CircuitFlags(0b0);
    pub fn check(self, other: CircuitFlags) -> bool {
        (self & other).0 != 0
    }

    pub fn all_true() -> Self {
        CircuitFlags::IS_EXPLICITLY_COMPUTABLE
            | CircuitFlags::IS_CONSTANT
            | CircuitFlags::CAN_BE_SAMPLED
            | CircuitFlags::USE_AUTONAME
    }
}

impl Default for CircuitFlags {
    fn default() -> Self {
        Self::all_true()
    }
}

impl BitOr for CircuitFlags {
    type Output = CircuitFlags;
    fn bitor(self, rhs: Self) -> Self::Output {
        Self(self.0 | rhs.0)
    }
}
impl BitAnd for CircuitFlags {
    type Output = CircuitFlags;
    fn bitand(self, rhs: Self) -> Self::Output {
        Self(self.0 & rhs.0)
    }
}
use std::ops::BitOrAssign;
impl BitOrAssign for CircuitFlags {
    fn bitor_assign(&mut self, rhs: Self) {
        self.0 |= rhs.0
    }
}
use std::ops::BitAndAssign;
impl BitAndAssign for CircuitFlags {
    fn bitand_assign(&mut self, rhs: Self) {
        self.0 &= rhs.0
    }
}
impl Not for CircuitFlags {
    type Output = CircuitFlags;
    fn not(self) -> CircuitFlags {
        Self(!self.0)
    }
}

/// don't want to print hash with Debug; print selected fields
impl Debug for CachedCircuitInfo {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "{} {:?} {:?}",
            self.name.map_or("", |n| n.str()),
            self.shape,
            self.device_dtype,
        )
    }
}

impl CachedCircuitInfo {
    pub fn numel(&self) -> BigUint {
        self.shape
            .iter()
            .map(|x| BigUint::from(x.t().unwrap_or(1)))
            .product()
    }
    /// Saturating element count
    pub fn numel_usize(&self) -> usize {
        let numel_digits = self.numel().to_u64_digits();
        match numel_digits.len() {
            0 => 0,
            1 => numel_digits[0] as usize,
            _ => usize::MAX,
        }
    }

    pub fn naive_mem_use(&self, device_dtype: Option<TorchDeviceDtype>) -> BigUint {
        self.numel()
            * BigUint::from(
                device_dtype
                    .unwrap_or(self.device_dtype.unwrap_or_defaults())
                    .size(),
            )
    }
    // once we're scheduling everything is batch-realizeable so we don't need biguint
    pub fn naive_mem_use_usize(&self, device_dtype: Option<TorchDeviceDtype>) -> usize {
        self.numel_usize().saturating_mul(
            device_dtype
                .unwrap_or(self.device_dtype.unwrap_or_defaults())
                .size(),
        )
    }
    pub fn rank(&self) -> usize {
        self.shape.len()
    }
    pub fn hash_usize(&self) -> usize {
        let mut hash_prefix: [u8; 8] = Default::default();
        hash_prefix.copy_from_slice(&self.hash[..8]);
        usize::from_le_bytes(hash_prefix)
    }
    pub fn is_constant(&self) -> bool {
        self.flags.check(CircuitFlags::IS_CONSTANT)
    }
    pub fn can_be_sampled(&self) -> bool {
        self.flags.check(CircuitFlags::CAN_BE_SAMPLED)
    }
    pub fn is_explicitly_computable(&self) -> bool {
        self.flags.check(CircuitFlags::IS_EXPLICITLY_COMPUTABLE)
    }
    pub fn use_autoname(&self) -> bool {
        self.flags.check(CircuitFlags::USE_AUTONAME)
    }
    // implementation helper
    pub fn already_set_named_axes(&self) -> Option<NamedAxes> {
        (!self.named_axes.is_empty()).then(|| self.named_axes.clone())
    }
}

pub fn get_free_symbols(x: &CircuitRc) -> Cow<IndexSet<CircuitRc>> {
    if x.is_symbol() {
        return Cow::Owned([x.clone()].into_iter().collect());
    } else {
        return Cow::Borrowed(get_raw_free_symbols(x));
    }
}

// assumes x isn't a Symbol
pub fn get_raw_free_symbols(x: &CircuitRc) -> &IndexSet<CircuitRc> {
    fn recurse(x: &CircuitRc, out: &mut Option<ArcCow<IndexSet<CircuitRc>>>) {
        // ideally, symbol would just store itself in info.free_symbols rather than doing this check here
        // but, then the symbol would have a circular reference to itself
        // So we can only include children and then we special case syms in various places. : /
        if x.is_symbol() {
            out.get_or_insert_with(|| ArcCow::from_owned(IndexSet::default()))
                .insert(x.clone());
        } else {
            let info = x.info();
            if info.free_symbols.is_none() {
                return;
            }
            // None = no free symbols, Some = at least one free symbol
            if let Some(free_symbols) = &info.free_symbols {
                if let Some(computed) = free_symbols.get() {
                    if let Some(out) = out {
                        out.extend(computed.iter().cloned());
                    } else {
                        *out = Some(computed.clone().into());
                    }
                } else {
                    // only one ref (we aren't using weakrefs), so don't bother caching
                    // todo maybe also dont cache in some other cases
                    if Arc::strong_count(&(*x)) <= 1 {
                        for child in x.children_sl() {
                            recurse(&child, out);
                        }
                    } else {
                        let mut x_out = None;
                        for c in x.children_sl() {
                            recurse(&c, &mut x_out);
                        }
                        let x_out = x_out.unwrap().into_arc();
                        if let Some(out) = out {
                            out.extend(x_out.iter().cloned());
                        } else {
                            *out = Some(x_out.clone().into());
                        }
                        let _ = free_symbols.set(Box::new(x_out));
                    }
                }
            }
        }
    }

    assert!(!x.is_symbol());
    if let Some(free_symbols) = &x.info().free_symbols {
        if let Some(free_symbols) = free_symbols.get() {
            return free_symbols;
        } else {
            let mut out = None;
            for c in x.children_sl() {
                recurse(&c, &mut out);
            }
            let out = out.unwrap().into_arc();
            let _ = free_symbols.set(Box::new(out));
            return free_symbols.get().unwrap();
        }
    } else {
        static NULL_INDEX_SET: Lazy<IndexSet<CircuitRc>> = Lazy::new(|| IndexSet::default());
        return &NULL_INDEX_SET;
    }
}

fn compute_device_dtype<I>(
    children: &[CircuitRc],
    extra: impl Fn() -> I,
) -> Result<TorchDeviceDtypeOp>
where
    I: Iterator<Item = TorchDeviceDtypeOp>,
{
    children
        .iter()
        .map(|c| c.info().device_dtype)
        .chain(extra())
        .try_fold(TorchDeviceDtypeOp::NONE, |acc, new| {
            TorchDeviceDtypeOp::combine(acc, new)
        })
        .with_context(|| {
            format!(
                "Could not combine device_dtype for node with children info {:?} and extra {:?}",
                children
                    .iter()
                    .map(|c| c.info().clone())
                    .collect::<Vec<_>>(),
                extra().collect::<Vec<_>>()
            )
        })
}
