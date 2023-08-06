use std::{
    collections::{BTreeMap, BTreeSet},
    fmt::{self, Debug},
    iter::{self, zip},
    ops,
    sync::Arc,
    vec,
};

use anyhow::{bail, Context, Result};
use circuit_base::{
    opaque_iterative_matcher::{
        OpaqueIterativeMatcherVal, Update as BaseUpdate,
        UpdatedIterativeMatcher as BaseUpdatedIterativeMatcher,
    },
    CircuitNode, CircuitNodeUnion, CircuitRc, CircuitType,
};
use circuit_utils::SetOfCircuitIdentities;
use macro_rules_attribute::apply;
use pyo3::{
    exceptions::{PyTypeError, PyValueError},
    prelude::*,
    AsPyPointer,
};
use rr_util::{
    eq_by_big_hash::EqByBigHash,
    py_types::PyCallable,
    python_error_exception, setup_callable, simple_default, simple_from,
    tensor_util::Slice,
    util::{
        arc_unwrap_or_clone, flip_op_result, transpose, CowArcHash, EmptySingleMany as ESM,
        HashBytes,
    },
};
use thiserror::Error;
use uuid::uuid;

use crate::{
    library::{apply_in_traversal, replace_outside_traversal_symbols},
    operations::AssertFound,
    AnyFound, BoundAnyFound, BoundGetter, BoundUpdater, Getter, Matcher, MatcherData,
    MatcherFromPyBase, MatcherRc, TransformRc, Updater,
};

#[derive(Clone, FromPyObject)]
pub enum IterativeMatcherFromPy {
    BaseMatch(MatcherFromPyBase),
    // Finished(Finished),
    IterativeMatcher(IterativeMatcher),
    #[pyo3(transparent)]
    PyMatcherFunc(PyCallable), // goes to matcher!
}

#[derive(Clone, Debug)]
pub enum IterativeMatcherData {
    Match(Matcher),
    Term(bool), // TODO maybe remove Term(true) for Chains(true, [])
    Restrict(RestrictIterativeMatcher),
    Children(ChildrenMatcher),
    ModuleArg(ModuleArgMatcher),
    SpecCircuit(IterativeMatcherRc),
    NoModuleSpec(IterativeMatcherRc),
    Chains(Chains),
    All(Vec<IterativeMatcherRc>),
    Raw(RawIterativeMatcher),
    PyFunc(PyCallable), // NOTE: not PyMatcherFunc
}
setup_callable!(IterativeMatcher, IterativeMatcherData, IterativeMatcherFromPy, match_iterate(circuit : CircuitRc) -> IterateMatchResults,no_py_callable);
simple_from!(|x: Matcher| -> IterativeMatcher { IterativeMatcherData::Match(x).into() });
simple_from!(|x: MatcherData| -> IterativeMatcher { Matcher::from(x).into() });
simple_from!(|x: MatcherFromPyBase| -> IterativeMatcher { Matcher::from(x).into() });
simple_from!(|x: MatcherFromPyBase| -> IterativeMatcherFromPy {
    IterativeMatcherFromPy::BaseMatch(x)
});
simple_from!(|x: Matcher| -> IterativeMatcherRc { IterativeMatcher::from(x).into() });
simple_from!(|x: MatcherData| -> IterativeMatcherRc { IterativeMatcher::from(x).into() });
simple_from!(|x: MatcherFromPyBase| -> IterativeMatcherRc { IterativeMatcher::from(x).into() });
simple_default!(IterativeMatcherFromPy {
    MatcherFromPyBase::default().into()
});
simple_default!(IterativeMatcher {
    Matcher::default().into()
});
simple_default!(IterativeMatcherRc {
    IterativeMatcher::default().into()
});

impl From<IterativeMatcherFromPy> for IterativeMatcher {
    fn from(m: IterativeMatcherFromPy) -> Self {
        match m {
            IterativeMatcherFromPy::BaseMatch(x) => x.into(),

            // TODO: maybe Finished should be convertible to Term
            // IterativeMatcherFromPy::Finished(_) => IterativeMatcherData::Term.into(),
            IterativeMatcherFromPy::IterativeMatcher(x) => x,
            // we intentionally do a matcher here as the default - if users want
            // a IterativeMatcher pyfunc, they can explicitly use IterativeMatcher
            // factory.
            IterativeMatcherFromPy::PyMatcherFunc(x) => MatcherData::PyFunc(x).into(),
        }
    }
}

#[derive(Clone, Debug)]
pub struct Chains {
    pub found: bool,
    // TODO maybe replace with just Arc & use different mutable Chains in match_iterate?
    // TODO empty | single | many enum
    pub chains: CowArcHash<BTreeMap<IterativeMatcherRc, Chains>>, /* fst must not be Chain */
}

impl EqByBigHash for Chains {
    fn hash(&self) -> HashBytes {
        let mut hasher = blake3::Hasher::new();
        hasher.update(&[self.found as u8]);
        hasher.update(&self.chains.hash());
        hasher.finalize().into()
    }
}

impl EqByBigHash for IterativeMatcherRc {
    fn hash(&self) -> HashBytes {
        self.hash
    }
}

impl Chains {
    pub fn found() -> Self {
        Self {
            found: true,
            chains: CowArcHash::new(BTreeMap::new()),
        }
    }

    pub fn new() -> Self {
        Self {
            found: false,
            chains: CowArcHash::new(BTreeMap::new()),
        }
    }

    fn merge(&mut self, other: &Chains) {
        self.found |= other.found;
        for (fst, snd) in other.chains.iter() {
            self.add_chain(fst, snd);
        }
    }

    fn add_chain_many(&mut self, first: &IterativeMatcherRc, y: &Chains, ys: &[&Chains]) {
        match ys.len() {
            0 => return self.add_chain(first, y),
            _ => {}
        }
        match &first.data {
            IterativeMatcherData::Chains(cs) => self.merge_many(cs, &[&[y], ys].concat()),
            _ => self
                .chains
                .make_mut()
                .entry(first.clone())
                .or_insert_with(|| Chains::new())
                .merge_many(y, ys),
        }
    }
    fn merge_many(&mut self, y: &Chains, ys: &[&Chains]) {
        if ys.len() == 0 {
            return self.merge(y);
        }
        if y.found {
            self.merge_many(ys[0], &ys[1..])
        }
        for (fst, snd) in &*y.chains {
            self.add_chain_many(fst, snd, ys)
        }
    }

    fn add_chain(&mut self, first: &IterativeMatcherRc, rest: &Chains) {
        match &first.data {
            IterativeMatcherData::Chains(cs) => self.merge_many(cs, &[rest]),
            _ => {
                self.chains
                    .make_mut()
                    .entry(first.clone())
                    .and_modify(|x| x.merge(rest))
                    .or_insert_with(|| rest.clone());
            }
        }
    }

    fn add(&mut self, x: &IterativeMatcherRc) {
        match &x.data {
            IterativeMatcherData::Chains(x) => {
                self.merge(x);
            }
            _ => {
                self.chains
                    .make_mut()
                    .entry(x.clone())
                    .or_insert_with(|| Chains::new())
                    .found = true;
            }
        }
    }

    pub fn from(x: &IterativeMatcherRc) -> Self {
        match &x.data {
            IterativeMatcherData::Chains(x) => x.clone(),
            _ => {
                let mut c = Chains::new();
                c.add(x);
                c
            }
        }
    }

    pub fn as_single(&self) -> Option<IterativeMatcherRc> {
        if self.chains.len() == 1 {
            let (fst, snd) = self.chains.iter().next().unwrap();
            if snd.found && snd.chains.is_empty() {
                return Some(fst.clone());
            }
        }
        None
    }

    pub fn next_into_update(self) -> BaseUpdate<IterativeMatcherRc> {
        if !self.found && self.chains.is_empty() {
            None.into()
        } else {
            Some(IterativeMatcherData::Chains(self).into()).into()
        }
    }

    pub fn is_empty(&self) -> bool {
        !self.found && self.chains.is_empty()
    }

    pub fn validate_matched(&self, matched: &BTreeSet<CircuitRc>) -> Result<()> {
        for (fst, snd) in &*self.chains {
            if snd.found {
                fst.validate_matched(matched)?;
            }
            snd.validate_matched(matched)?;
        }
        Ok(())
    }
}

impl IterativeMatcherData {
    fn uuid(&self) -> [u8; 16] {
        match self {
            Self::Match(_) => uuid!("f1d5e8ec-cba0-496f-883e-78dd5cdc3a49"),
            Self::Term(_) => uuid!("365bc6b4-cbc6-4d82-8e14-7505e1229eec"),
            Self::Restrict(_) => uuid!("bcc5ccaa-afbe-414d-88b4-b8eac8c93ece"),
            Self::Children(_) => uuid!("0081e9c9-7fdb-43e1-900e-f1adde28f23d"),
            Self::ModuleArg(_) => uuid!("7a48bd8f-c028-4da8-9467-1277351aca35"),
            Self::SpecCircuit(_) => uuid!("b728a8c3-0493-4ee5-96c2-71e4900fc0f8"),
            Self::NoModuleSpec(_) => uuid!("b728a8c3-0493-4ee5-96c2-71e4900fc0f8"),
            Self::Chains(_) => uuid!("958d03ed-7a1a-4ea9-8dd4-d4a8a68feecb"),
            Self::All(_) => uuid!("b4079909-ad3e-4a32-a016-43c96f262237"),
            Self::Raw(_) => uuid!("5838ac96-0f48-4cdb-874f-d4f68ce3a52b"),
            Self::PyFunc(_) => uuid!("d3afc3c0-5c86-46df-9e41-7944caedd901"),
        }
        .into_bytes()
    }

    fn item_hash(&self, hasher: &mut blake3::Hasher) {
        match self {
            Self::Match(x) => {
                hasher.update(&x.hash());
            }
            Self::Restrict(RestrictIterativeMatcher {
                iterative_matcher,
                term_if_matches,
                start_depth,
                end_depth,
                term_early_at,
                depth,
            }) => {
                hasher.update(&iterative_matcher.hash);
                hasher.update(&[*term_if_matches as u8]);
                hasher.update(&[start_depth.is_some() as u8]);
                hasher.update(&start_depth.unwrap_or(0).to_le_bytes());
                hasher.update(&[end_depth.is_some() as u8]);
                hasher.update(&end_depth.unwrap_or(0).to_le_bytes());
                hasher.update(&term_early_at.hash());
                hasher.update(&depth.to_le_bytes());
            }
            Self::Children(ChildrenMatcher {
                iterative_matcher,
                child_numbers,
            }) => {
                hasher.update(&iterative_matcher.hash);
                for num in child_numbers {
                    hasher.update(&num.to_le_bytes());
                }
            }
            Self::ModuleArg(ModuleArgMatcher {
                module_matcher,
                arg_sym_matcher,
            }) => {
                hasher.update(&module_matcher.hash);
                hasher.update(&arg_sym_matcher.hash());
            }
            Self::SpecCircuit(matcher) | Self::NoModuleSpec(matcher) => {
                hasher.update(&matcher.hash);
            }
            Self::Chains(chains) => {
                hasher.update(&[chains.found as u8]);
                hasher.update(&chains.chains.hash());
            }
            Self::All(matchers) => {
                for matcher in matchers {
                    hasher.update(&matcher.hash);
                }
            }
            Self::Raw(x) => {
                hasher.update(&(Arc::as_ptr(&x.0) as *const () as usize).to_le_bytes());
            }
            Self::PyFunc(x) => {
                hasher.update(&(x.as_ptr() as usize).to_le_bytes());
            }
            &Self::Term(next) => {
                hasher.update(&[next as u8]);
            }
        }
    }
}

/// Helper with some basic rules you may want to use to control your node matching iterations.
#[derive(Clone, Debug)]
pub struct RestrictIterativeMatcher {
    pub iterative_matcher: IterativeMatcherRc,
    ///if true, stops once it has found a match
    pub term_if_matches: bool,
    /// depth at which we start matching
    pub start_depth: Option<u32>,
    /// depth at which we stop matching
    pub end_depth: Option<u32>,
    /// terminate iterative matching if we reach a node which matches this
    pub term_early_at: MatcherRc,
    pub depth: u32,
}

impl RestrictIterativeMatcher {
    /// Fancy constructor which supports range
    ///
    /// TODO: add support for a builder with defaults because this is really annoying...
    /// TODO: actually test this when builder is added!
    pub fn new_range<R: ops::RangeBounds<u32>>(
        iterative_matcher: IterativeMatcherRc,
        term_if_matches: bool,
        depth_range: R,
        term_early_at: MatcherRc,
    ) -> Self {
        use ops::Bound;

        let start_depth = match depth_range.start_bound() {
            Bound::Unbounded => None,
            Bound::Included(x) => Some(*x),
            Bound::Excluded(x) => Some(*x + 1),
        };
        let end_depth = match depth_range.end_bound() {
            Bound::Unbounded => None,
            Bound::Included(x) => Some(*x + 1),
            Bound::Excluded(x) => Some(*x),
        };
        Self {
            iterative_matcher,
            term_if_matches,
            start_depth,
            end_depth,
            term_early_at,
            depth: 0,
        }
    }

    pub fn new(
        iterative_matcher: IterativeMatcherRc,
        term_if_matches: bool,
        start_depth: Option<u32>,
        end_depth: Option<u32>,
        term_early_at: MatcherRc,
    ) -> Self {
        Self {
            iterative_matcher,
            term_if_matches,
            start_depth,
            end_depth,
            term_early_at,
            depth: 0,
        }
    }

    pub fn match_iterate(&self, circuit: CircuitRc) -> Result<IterateMatchResults> {
        let with_dist_of_end = |offset: u32| {
            self.end_depth
                .map(|x| self.depth >= x.saturating_sub(offset))
                .unwrap_or(false)
        };

        let after_end = with_dist_of_end(0);
        if after_end {
            return Ok(IterateMatchResults {
                updated: Some(None.into()),
                found: false,
            });
        }

        let IterateMatchResults { updated, found } =
            self.iterative_matcher.match_iterate(circuit.clone())?;

        let before_start = self.start_depth.map(|x| self.depth < x).unwrap_or(false);

        let found = found && !before_start;

        let reached_end = with_dist_of_end(1);
        if all_finished(&updated)
            || (found && self.term_if_matches)
            || reached_end
            || self.term_early_at.call(circuit)?
        {
            return Ok(IterateMatchResults {
                updated: Some(None.into()),
                found,
            });
        }

        let needs_depth_update = self.end_depth.is_some() || before_start;

        let new_depth = if needs_depth_update {
            self.depth + 1
        } else {
            self.depth
        };

        let updated = if needs_depth_update {
            // we can't keep same if we need to update end_depth
            Some(updated.unwrap_or(Some(self.iterative_matcher.clone()).into()))
        } else {
            updated
        };

        let updated = map_updated(updated, |new| {
            IterativeMatcherData::Restrict(RestrictIterativeMatcher {
                iterative_matcher: new,
                depth: new_depth,
                ..self.clone()
            })
            .into()
        });

        Ok(IterateMatchResults { updated, found })
    }
}

#[derive(Clone, Debug)]
pub struct ChildrenMatcher {
    pub iterative_matcher: IterativeMatcherRc,
    pub child_numbers: BTreeSet<usize>,
}

impl ChildrenMatcher {
    pub fn new(
        iterative_matcher: IterativeMatcherRc,
        child_numbers: BTreeSet<usize>,
    ) -> Result<Self> {
        Ok(Self {
            iterative_matcher,
            child_numbers,
        })
    }

    pub fn check_num_children(&self, num_children: usize) -> Result<()> {
        for n in &self.child_numbers {
            if n >= &num_children {
                bail!(IterativeMatcherError::ChildNumbersOutOfBounds {
                    child_numbers: self.child_numbers.clone(),
                    num_children
                });
            }
        }
        Ok(())
    }

    pub fn match_iterate(&self, circuit: CircuitRc) -> Result<IterateMatchResults> {
        let num_children = circuit.num_children();
        let IterateMatchResults { updated, found } =
            self.iterative_matcher.match_iterate(circuit)?;

        let updated_to_children_matcher = |iterative_matcher| {
            IterativeMatcherData::Children(Self {
                iterative_matcher,
                child_numbers: self.child_numbers.clone(),
            })
            .into()
        };

        let out = if found {
            self.check_num_children(num_children)?;

            let per_child = per_child(updated, self.iterative_matcher.clone(), num_children);
            assert_eq!(per_child.len(), num_children);
            let updated = per_child
                .into_iter()
                .enumerate()
                .map(|(i, x)| {
                    Some(
                        IterativeMatcher::special_case_any(
                            x.map(updated_to_children_matcher)
                                .into_iter()
                                .chain(
                                    (self.child_numbers.contains(&i))
                                        .then(|| IterativeMatcher::term(true).into()),
                                )
                                .collect(),
                        )
                        .rc(),
                    )
                    .into()
                })
                .collect::<Vec<Update>>()
                .into();

            IterateMatchResults {
                updated: Some(updated),
                found: false,
            }
        } else {
            IterateMatchResults {
                updated: map_updated(updated, updated_to_children_matcher),
                found: false,
            }
        };
        Ok(out)
    }
}

#[derive(Clone, Debug)]
pub struct ModuleArgMatcher {
    pub module_matcher: IterativeMatcherRc,
    pub arg_sym_matcher: MatcherRc,
}

impl ModuleArgMatcher {
    pub fn new(module_matcher: IterativeMatcherRc, arg_sym_matcher: MatcherRc) -> Result<Self> {
        Ok(Self {
            module_matcher,
            arg_sym_matcher,
        })
    }

    pub fn match_iterate(&self, circuit: CircuitRc) -> Result<IterateMatchResults> {
        let IterateMatchResults { updated, found } =
            self.module_matcher.match_iterate(circuit.clone())?;

        let wrap = |updated_matcher| {
            IterativeMatcherData::ModuleArg(Self {
                module_matcher: updated_matcher,
                arg_sym_matcher: self.arg_sym_matcher.clone(),
            })
            .into()
        };

        let wrapped_updated = if found {
            let module =
                circuit
                    .as_module()
                    .ok_or_else(|| IterativeMatcherError::ExpectedModule {
                        circuit_type: circuit.type_tag(),
                    })?;

            let per_child = per_child(updated, self.module_matcher.clone(), circuit.num_children());
            assert_eq!(per_child.len(), circuit.num_children());
            Some(
                per_child
                    .into_iter()
                    .enumerate()
                    .map(|(i, x)| {
                        let arg_matches = i > 0
                            && self
                                .arg_sym_matcher
                                .call(module.spec.arg_specs[i - 1].symbol.crc())?;
                        Ok(Some(
                            IterativeMatcher::special_case_any(
                                x.map(wrap)
                                    .into_iter()
                                    .chain(arg_matches.then(|| IterativeMatcher::term(true).into()))
                                    .collect(),
                            )
                            .rc(),
                        )
                        .into())
                    })
                    .collect::<Result<Vec<Update>>>()?
                    .into(),
            )
        } else {
            map_updated(updated, wrap)
        };

        Ok(IterateMatchResults {
            updated: wrapped_updated,
            found: false,
        })
    }
}

impl circuit_base::opaque_iterative_matcher::HasTerm for IterativeMatcherRc {
    fn term() -> Self {
        IterativeMatcher::term(false).into()
    }
}

pub type Update = BaseUpdate<IterativeMatcherRc>;
pub type UpdatedIterativeMatcher = BaseUpdatedIterativeMatcher<IterativeMatcherRc>;

pub fn require_single(x: UpdatedIterativeMatcher) -> Result<Update> {
    match x {
        UpdatedIterativeMatcher::Many(matchers) => {
            bail!(IterativeMatcherError::OperationDoesntSupportArgPerChild { matchers })
        }
        UpdatedIterativeMatcher::Single(x) => Ok(x),
    }
}

/// returned option inside of vec is whether or not finished
pub fn per_child(
    updated: Option<UpdatedIterativeMatcher>,
    matcher: IterativeMatcherRc,
    num_children: usize,
) -> Vec<Option<IterativeMatcherRc>> {
    updated
        .unwrap_or(Some(matcher).into())
        .per_child(num_children)
}

pub fn per_child_with_term(
    updated: Option<UpdatedIterativeMatcher>,
    matcher: IterativeMatcherRc,
    num_children: usize,
) -> Vec<IterativeMatcherRc> {
    per_child(updated, matcher, num_children)
        .into_iter()
        .map(|x| x.unwrap_or_else(|| IterativeMatcher::term(false).into()))
        .collect()
}

pub fn function_per_child_op(
    updated: Option<UpdatedIterativeMatcher>,
    matcher: IterativeMatcherRc,
    circuit: CircuitRc,
    mut func: impl FnMut(CircuitRc, IterativeMatcherRc) -> Result<CircuitRc>,
) -> Result<Option<CircuitRc>> {
    if all_finished(&updated) {
        return Ok(None);
    }
    match updated.unwrap_or(Some(matcher).into()) {
        UpdatedIterativeMatcher::Single(x) => {
            if let Some(m) = x.0 {
                circuit.map_children(|c| func(c, m.clone())).map(Some)
            } else {
                Ok(Some(circuit))
            }
        }
        UpdatedIterativeMatcher::Many(xs) => {
            let out = zip(xs, circuit.children())
                .map(|(x, c)| if let Some(m) = x.0 { func(c, m) } else { Ok(c) })
                .collect::<Result<Vec<_>>>()?;
            circuit.replace_children(out).map(Some)
        }
    }
}

pub fn function_per_child_map_op(
    updated: Option<UpdatedIterativeMatcher>,
    matcher: IterativeMatcherRc,
    circuit: &CircuitRc,
    mut func: impl FnMut(&CircuitRc, IterativeMatcherRc) -> Result<Option<CircuitRc>>,
) -> Result<Option<CircuitRc>> {
    if all_finished(&updated) {
        return Ok(None);
    }
    match updated.unwrap_or(Some(matcher).into()) {
        UpdatedIterativeMatcher::Single(x) => {
            if let Some(m) = x.0 {
                circuit.map_children_op_result(|c| func(c, m.clone()))
            } else {
                Ok(None)
            }
        }
        UpdatedIterativeMatcher::Many(xs) => {
            let mut new_children: Option<Vec<CircuitRc>> = None;
            let info = circuit.info();
            for (i, x) in xs.into_iter().enumerate() {
                if let Some(m) = x.0 && let Some(new) = func(&info.children[i], m)? {
                    new_children.get_or_insert_with(|| info.children.clone())[i] = new;
                }
            }
            Ok(if let Some(new_children) = new_children {
                Some(circuit.replace_children(new_children)?)
            } else {
                None
            })
        }
    }
}

pub fn function_per_child(
    updated: Option<UpdatedIterativeMatcher>,
    matcher: IterativeMatcherRc,
    circuit: CircuitRc,
    func: impl FnMut(CircuitRc, IterativeMatcherRc) -> Result<CircuitRc>,
) -> Result<CircuitRc> {
    function_per_child_op(updated, matcher, circuit.clone(), func).map(|x| x.unwrap_or(circuit))
}

pub fn map_updated(
    x: Option<UpdatedIterativeMatcher>,
    f: impl FnMut(IterativeMatcherRc) -> IterativeMatcherRc,
) -> Option<UpdatedIterativeMatcher> {
    x.map(|x| x.map_updated(f))
}

pub fn all_finished(x: &Option<UpdatedIterativeMatcher>) -> bool {
    x.as_ref().map(|x| x.all_finished()).unwrap_or(false)
}

#[pyclass]
#[derive(Clone, Debug)]
pub struct IterateMatchResults {
    /// here None, is 'use same'
    #[pyo3(set, get)]
    pub updated: Option<UpdatedIterativeMatcher>,
    #[pyo3(set, get)]
    pub found: bool,
}

#[pymethods]
impl IterateMatchResults {
    #[new]
    #[pyo3(signature=(updated = None, found = false))]
    fn new(updated: Option<UpdatedIterativeMatcher>, found: bool) -> Self {
        Self { updated, found }
    }

    #[staticmethod]
    #[pyo3(signature=(found = false))]
    pub fn new_finished(found: bool) -> Self {
        Self {
            updated: Some(None.into()),
            found,
        }
    }

    fn to_tup(&self) -> (Option<UpdatedIterativeMatcher>, bool) {
        (self.updated.clone(), self.found)
    }

    #[pyo3(name = "unwrap_or_same")]
    pub fn unwrap_or_same_py(
        &self,
        matcher: IterativeMatcherRc,
    ) -> (UpdatedIterativeMatcher, bool) {
        self.clone().unwrap_or_same(matcher)
    }
}

impl IterateMatchResults {
    pub fn unwrap_or_same(self, matcher: IterativeMatcherRc) -> (UpdatedIterativeMatcher, bool) {
        (self.updated.unwrap_or(Some(matcher).into()), self.found)
    }
}

impl IterativeMatcher {
    pub fn or(self, other: IterativeMatcherRc) -> Self {
        Self::any(vec![self.crc(), other])
    }

    pub fn and(self, other: IterativeMatcherRc) -> Self {
        Self::all(vec![self.crc(), other])
    }

    // TODO: this is kinda shitty, see https://github.com/redwoodresearch/unity/issues/1524
    pub fn validate_matched(&self, matched: &BTreeSet<CircuitRc>) -> Result<()> {
        match &self.data {
            IterativeMatcherData::Match(m) => m.validate_matched(matched),
            IterativeMatcherData::Term(_) => Ok(()),
            IterativeMatcherData::Restrict(m) => m.iterative_matcher.validate_matched(matched),
            IterativeMatcherData::Children(_)
            | IterativeMatcherData::ModuleArg(_)
            | IterativeMatcherData::SpecCircuit(_) => Ok(()), /* not sure what else you could do here */
            IterativeMatcherData::NoModuleSpec(m) => m.validate_matched(matched),
            IterativeMatcherData::Chains(m) => m.validate_matched(matched),
            IterativeMatcherData::All(_) => Ok(()), // TODO
            IterativeMatcherData::PyFunc(_) | IterativeMatcherData::Raw(_) => Ok(()),
        }
    }

    pub fn as_opaque(&self) -> OpaqueIterativeMatcherVal {
        Python::with_gil(|py| OpaqueIterativeMatcherVal::Py(self.clone().into_py(py)))
    }
    // TODO: more rust niceness funcs like the py ones!
}

impl IterativeMatcherRc {
    // -> (found, all_finished, children matchers)
    pub fn match_iterate_continue(
        self,
        circuit: CircuitRc,
    ) -> Result<(bool, bool, Vec<IterativeMatcherRc>)> {
        let num_children = circuit.num_children();
        let (updated, found) = self.match_iterate(circuit)?.unwrap_or_same(self);
        Ok((
            found,
            updated.all_finished(),
            updated.per_child_with_term(num_children),
        ))
    }
}

#[pymethods]
impl IterativeMatcher {
    #[new]
    #[pyo3(signature=(*inps))]
    // also py_new
    fn special_case_any(inps: Vec<IterativeMatcherRc>) -> Self {
        match inps.into() {
            ESM::Empty => Self::term(false),
            ESM::Single(x) => x.inner_or_clone(),
            ESM::Many(x) => Self::any(x),
        }
    }

    #[staticmethod]
    pub fn noop_traversal() -> Self {
        MatcherData::Always(true).into()
    }

    #[staticmethod]
    #[pyo3(signature=(match_next = false))]
    pub fn term(match_next: bool) -> Self {
        IterativeMatcherData::Term(match_next).into()
    }

    pub fn match_iterate(&self, circuit: CircuitRc) -> Result<IterateMatchResults> {
        let num_children = circuit.num_children();
        let res = match &self.data {
            IterativeMatcherData::Match(m) => IterateMatchResults {
                updated: None,
                found: m.call(circuit)?,
            },
            &IterativeMatcherData::Term(match_next) => {
                IterateMatchResults::new_finished(match_next)
            }
            IterativeMatcherData::Restrict(filter) => filter.match_iterate(circuit)?,
            IterativeMatcherData::Children(children_matcher) => {
                children_matcher.match_iterate(circuit)?
            }
            IterativeMatcherData::ModuleArg(module_arg_matcher) => {
                module_arg_matcher.match_iterate(circuit)?
            }
            IterativeMatcherData::SpecCircuit(module_matcher) => {
                let tag = circuit.type_tag();
                let IterateMatchResults { updated, found } =
                    module_matcher.match_iterate(circuit)?;
                let updated_to_spec_circuit_matcher =
                    |iterative_matcher| IterativeMatcherData::SpecCircuit(iterative_matcher).into();
                if found {
                    if tag != CircuitType::Module {
                        bail!(IterativeMatcherError::ExpectedModule { circuit_type: tag });
                    }

                    let per_child = per_child(updated, module_matcher.clone(), num_children);

                    let updated = per_child
                        .into_iter()
                        .enumerate()
                        .map(|(i, x)| {
                            Some(
                                IterativeMatcher::special_case_any(
                                    x.map(updated_to_spec_circuit_matcher)
                                        .into_iter()
                                        .chain(
                                            (i == 0) // spec circuit is child 0 on Module
                                                .then(|| IterativeMatcher::term(true).into()),
                                        )
                                        .collect(),
                                )
                                .rc(),
                            )
                            .into()
                        })
                        .collect::<Vec<Update>>()
                        .into();

                    IterateMatchResults {
                        updated: Some(updated),
                        found: false,
                    }
                } else {
                    IterateMatchResults {
                        updated: map_updated(updated, updated_to_spec_circuit_matcher),
                        found: false,
                    }
                }
            }
            IterativeMatcherData::NoModuleSpec(matcher) => {
                let is_module = circuit.is_module();
                let IterateMatchResults { updated, found } = matcher.match_iterate(circuit)?;
                if is_module {
                    let per_child = per_child(updated, matcher.clone(), num_children);
                    let updated = per_child
                        .into_iter()
                        .enumerate()
                        .map(|(i, x)| {
                            x.and_then(|x| {
                                (i != 0).then(|| IterativeMatcherData::NoModuleSpec(x).into())
                            })
                            .into()
                        })
                        .collect::<Vec<Update>>()
                        .into();

                    IterateMatchResults {
                        updated: Some(updated),
                        found,
                    }
                } else {
                    IterateMatchResults {
                        updated: map_updated(updated, |x| {
                            IterativeMatcherData::NoModuleSpec(x).into()
                        }),
                        found,
                    }
                }
            }
            IterativeMatcherData::Chains(chains) => {
                let mut same_up_to = 0;
                let mut found_outer = chains.found;
                let (first_matcher, first_results, first_rest) = 'a: {
                    for (first, rest) in chains.chains.iter() {
                        let results = first.match_iterate(circuit.clone())?;
                        let IterateMatchResults { updated, found } = &results;

                        match updated {
                            None => {}
                            _ => {
                                break 'a (first, results, rest);
                            }
                        }
                        if *found {
                            // TODO don't always need to break here i think
                            break 'a (first, results, rest);
                        }
                        same_up_to += 1;
                    }
                    return Ok(IterateMatchResults {
                        found: found_outer,
                        updated: None,
                    });
                };

                let mut new_chains: Chains = Chains {
                    chains: CowArcHash::new(
                        chains
                            .chains
                            .iter()
                            .take(same_up_to)
                            .map(|(x, y)| (x.clone(), y.clone()))
                            .collect(),
                    ),
                    found: false,
                };
                let mut chains_per_child: Option<Vec<Option<Chains>>> = None;

                fn recurse(
                    circuit: &CircuitRc,
                    first: &IterativeMatcherRc,
                    first_circuit_results: IterateMatchResults,
                    rest: &Chains,
                    new_chains: &mut Chains,
                    chains_per_child: &mut Option<Vec<Option<Chains>>>,
                ) -> Result<bool> {
                    use BaseUpdatedIterativeMatcher::*;

                    let IterateMatchResults { updated, found } = first_circuit_results;

                    match updated {
                        None => {
                            new_chains.add_chain(first, rest);
                        }
                        Some(Single(BaseUpdate(None))) => {} // finished
                        Some(Single(BaseUpdate(Some(x)))) => {
                            new_chains.add_chain(&x, rest);
                        }
                        Some(Many(items)) => {
                            for (x, c) in items.into_iter().zip(
                                chains_per_child
                                    .get_or_insert_with(|| vec![None; circuit.num_children()])
                                    .iter_mut(),
                            ) {
                                match x.0 {
                                    None => {}
                                    Some(x) => {
                                        c.get_or_insert_with(|| Chains::new()).add_chain(&x, rest);
                                    }
                                }
                            }
                        }
                    };

                    let mut found_done = false;

                    if found {
                        found_done |= rest.found;
                        for (rest_first, rest_rest) in rest.chains.iter() {
                            found_done |= recurse(
                                circuit,
                                rest_first,
                                rest_first.match_iterate(circuit.clone())?,
                                rest_rest,
                                new_chains,
                                chains_per_child,
                            )?;
                        }
                    }

                    Ok(found_done)
                }

                // handle failed case from break
                found_outer |= recurse(
                    &circuit,
                    &first_matcher,
                    first_results,
                    first_rest,
                    &mut new_chains,
                    &mut chains_per_child,
                )?;

                for (first, rest) in chains.chains.iter().skip(same_up_to) {
                    found_outer |= recurse(
                        &circuit,
                        &first,
                        first.match_iterate(circuit.clone())?,
                        rest,
                        &mut new_chains,
                        &mut chains_per_child,
                    )?;
                }

                IterateMatchResults {
                    found: found_outer,
                    updated: if let Some(per_child) = chains_per_child {
                        let mut new_chains_update: Option<Update> = None;
                        Some(
                            per_child
                                .into_iter()
                                .map(|x| {
                                    if let Some(mut x) = x {
                                        x.merge(&new_chains);
                                        x.next_into_update()
                                    } else {
                                        new_chains_update
                                            .get_or_insert_with(|| {
                                                new_chains.clone().next_into_update()
                                            })
                                            .clone()
                                    }
                                })
                                .collect::<Vec<Update>>()
                                .into(),
                        )
                    } else {
                        Some(UpdatedIterativeMatcher::Single(
                            new_chains.next_into_update(),
                        ))
                    },
                }
            }
            IterativeMatcherData::All(matchers) => {
                let results = matchers
                    .iter()
                    .map(|x| x.match_iterate(circuit.clone()))
                    .collect::<Result<Vec<_>>>()?;
                let found = results.iter().all(|x| x.found);
                let all_updated: Vec<_> = results.into_iter().map(|x| x.updated).collect();

                if all_updated.iter().all(|x| x.is_none()) {
                    IterateMatchResults {
                        found,
                        updated: None,
                    }
                } else if all_updated.iter().any(|x| all_finished(x)) {
                    IterateMatchResults {
                        found,
                        updated: Some(None.into()),
                    }
                } else if all_updated.iter().all(|x| {
                    x.as_ref()
                        .map(|x| matches!(x, UpdatedIterativeMatcher::Single(_)))
                        .unwrap_or(true)
                }) {
                    let updated_sub: Vec<_> = all_updated
                        .into_iter()
                        .zip(matchers)
                        .map(|(x, matcher)| {
                            x.map(|x| match x {
                                UpdatedIterativeMatcher::Single(x) => x.0.unwrap(),
                                UpdatedIterativeMatcher::Many(_) => unreachable!(),
                            })
                            .unwrap_or(matcher.clone())
                        })
                        .collect();
                    let updated = Some(Some(Self::all(updated_sub).rc()).into());

                    IterateMatchResults { found, updated }
                } else {
                    let all_per_child = all_updated
                        .into_iter()
                        .zip(matchers)
                        .map(|(updated, matcher)| per_child(updated, matcher.clone(), num_children))
                        .collect();
                    let updated = transpose(all_per_child, num_children)
                        .into_iter()
                        .map(|new_matchers| {
                            Some(Self::all(new_matchers.into_iter().collect::<Option<_>>()?).rc())
                        })
                        .collect::<Vec<_>>();
                    let updated = Some(updated.into());

                    IterateMatchResults { found, updated }
                }
            }
            IterativeMatcherData::Raw(f) => f.0(circuit)?,
            IterativeMatcherData::PyFunc(pyfunc) => Python::with_gil(|py| {
                pyfunc
                    .call1(py, (circuit,))
                    .context("calling python iterative matcher failed")
                    .and_then(|r| {
                        r.extract(py)
                            .context("extracting from python iterative matcher failed")
                    })
            })?,
        };

        if let Some(UpdatedIterativeMatcher::Many(items)) = &res.updated {
            // checking here allows us to assume valid in other places!
            if items.len() != num_children {
                bail!(IterativeMatcherError::NumUpdatedMatchersNEQToNumChildren {
                    num_updated_matchers: items.len(),
                    num_children,
                    updated_matchers: items.clone(),
                    from_matcher: self.crc()
                });
            }
        }

        // fast since just checks hash equality
        if let Some(UpdatedIterativeMatcher::Single(BaseUpdate(Some(s)))) = &res.updated && &***s == self {
            return Ok(IterateMatchResults {
                found: res.found,
                updated: None,
            })
        }

        Ok(res)
    }

    #[pyo3(name = "validate_matched")]
    fn validate_matched_py(&self, matched: BTreeSet<CircuitRc>) -> Result<()> {
        self.validate_matched(&matched)
    }

    #[staticmethod]
    #[pyo3(signature = (*matchers))]
    pub fn any(matchers: Vec<IterativeMatcherRc>) -> Self {
        let mut chain = Chains::new();
        for m in matchers {
            chain.add(&m);
        }
        IterativeMatcherData::Chains(chain).into()
    }

    #[staticmethod]
    #[pyo3(signature = (*matchers))]
    pub fn all(matchers: Vec<IterativeMatcherRc>) -> Self {
        IterativeMatcherData::All(matchers).into()
    }

    #[staticmethod]
    #[pyo3(signature=(first, *rest, must_be_sub = false))]
    pub fn new_chain(
        first: IterativeMatcherRc,
        rest: Vec<IterativeMatcherRc>,
        must_be_sub: bool,
    ) -> Self {
        first.chain(rest, must_be_sub)
    }

    #[staticmethod]
    #[pyo3(signature=(*chains, must_be_sub = false))]
    pub fn new_chain_many(chains: Vec<Vec<IterativeMatcherRc>>, must_be_sub: bool) -> Result<Self> {
        Ok(Self::any(
            chains
                .into_iter()
                .map(|v| {
                    let ch2 = v
                        .into_iter()
                        .enumerate()
                        .rfold(Chains::found(), |ch, (ix, y)| {
                            // TODO cleanup this
                            let y = if ix >= 1 && must_be_sub {
                                restrict(
                                    y.clone(),
                                    false,
                                    Some(1),
                                    None,
                                    MatcherFromPyBase::Always(false).into(),
                                )
                                .rc()
                            } else {
                                y.clone()
                            };
                            let mut x = Chains::new();
                            x.add_chain(&y, &ch);
                            x
                        });
                    IterativeMatcherData::Chains(ch2).into()
                })
                .collect(),
        ))
    }

    #[staticmethod]
    pub fn new_children_matcher(
        first_match: IterativeMatcherRc,
        child_numbers: BTreeSet<usize>,
    ) -> Self {
        first_match.children_matcher(child_numbers)
    }

    #[staticmethod]
    pub fn new_module_arg_matcher(
        module_matcher: IterativeMatcherRc,
        arg_sym_matcher: MatcherRc,
    ) -> Self {
        module_matcher.module_arg_matcher(arg_sym_matcher)
    }

    #[staticmethod]
    pub fn new_spec_circuit_matcher(module_matcher: IterativeMatcherRc) -> Self {
        module_matcher.spec_circuit_matcher()
    }

    #[staticmethod]
    #[pyo3(name = "new_func")]
    pub(super) fn new_func_py(f: PyCallable) -> Self {
        IterativeMatcherData::PyFunc(f).into()
    }

    #[pyo3(signature=(*others))]
    pub fn new_or(&self, others: Vec<IterativeMatcherRc>) -> Self {
        Self::any([self.clone().into()].into_iter().chain(others).collect())
    }

    fn __or__(&self, other: IterativeMatcherRc) -> Self {
        self.clone().or(other)
    }
    fn __ror__(&self, other: IterativeMatcherRc) -> Self {
        arc_unwrap_or_clone(other.0).or(self.crc())
    }

    fn __and__(&self, other: IterativeMatcherRc) -> Self {
        self.clone().and(other)
    }
    fn __rand__(&self, other: IterativeMatcherRc) -> Self {
        arc_unwrap_or_clone(other.0).and(self.crc())
    }
    fn __bool__(&self) -> PyResult<bool> {
        PyResult::Err(PyTypeError::new_err("IterativeMatcher was coerced to a boolean. Did you mean to use & or | instead of \"and\" or \"or\"?"))
    }

    // TODO: write flatten/simplify method if we want the extra speed + niceness!
}

macro_rules! dup_functions {
    {
        #[self_id($self_ident:ident)]
        impl IterativeMatcher {
            $(
            $( #[$($meta_tt:tt)*] )*
        //  ^~~~attributes~~~~^
            $vis:vis fn $name:ident (
                &self
                $(, $arg_name:ident : $arg_ty:ty )* $(,)?
        //      ^~~~~~~~~~~~~~~argument list!~~~~~~~~~~~^
                )
                $( -> $ret_ty:ty )?
        //      ^~~~return type~~~^
                { $($tt:tt)* }
            )*

        }
    } => {
        #[pymethods]
        impl IterativeMatcher {
            $(
                $(#[$($meta_tt)*])*
                $vis fn $name(&self, $($arg_name : $arg_ty,)*) $(-> $ret_ty)* {
                    let $self_ident = self;
                    $($tt)*
                }
            )*
        }

        #[pymethods]
        impl Matcher {
            $(
                $(#[$($meta_tt)*])*
                $vis fn $name(&self, $($arg_name : $arg_ty,)*) $(-> $ret_ty)* {
                    self.to_iterative_matcher().$name($($arg_name,)*)
                }
            )*
        }

    };
}

#[apply(dup_functions)]
#[self_id(self_)]
impl IterativeMatcher {
    #[pyo3(signature=(*rest, must_be_sub = false))]
    pub fn chain(&self, rest: Vec<IterativeMatcherRc>, must_be_sub: bool) -> IterativeMatcher {
        // TODO: flatten
        Self::new_chain_many(
            vec![iter::once(self_.clone().rc()).chain(rest).collect()],
            must_be_sub,
        )
        .unwrap()
    }

    #[pyo3(signature=(*rest, must_be_sub = false))]
    pub fn chain_many(
        &self,
        rest: Vec<Vec<IterativeMatcherRc>>,
        must_be_sub: bool,
    ) -> IterativeMatcher {
        // TODO: flatten
        Self::new_chain_many(
            rest.into_iter()
                .map(|x| iter::once(self_.clone().rc()).chain(x).collect())
                .collect(),
            must_be_sub,
        )
        .unwrap()
    }

    pub fn children_matcher(&self, child_numbers: BTreeSet<usize>) -> IterativeMatcher {
        IterativeMatcherData::Children(ChildrenMatcher {
            iterative_matcher: self_.clone().rc(),
            child_numbers,
        })
        .into()
    }

    pub fn module_arg_matcher(&self, arg_sym_matcher: MatcherRc) -> IterativeMatcher {
        IterativeMatcherData::ModuleArg(ModuleArgMatcher {
            module_matcher: self_.clone().rc(),
            arg_sym_matcher,
        })
        .into()
    }

    pub fn spec_circuit_matcher(&self) -> IterativeMatcher {
        IterativeMatcherData::SpecCircuit(self_.clone().rc()).into()
    }

    #[pyo3(signature=(enable = true))]
    pub fn filter_module_spec(&self, enable: bool) -> IterativeMatcher {
        if enable {
            IterativeMatcherData::NoModuleSpec(self_.clone().rc()).into()
        } else {
            self_.clone()
        }
    }

    #[pyo3(signature=(circuit, fancy_validate = Getter::default().default_fancy_validate))]
    pub fn get(&self, circuit: CircuitRc, fancy_validate: bool) -> Result<BTreeSet<CircuitRc>> {
        Getter::default().get(circuit, self_.crc(), Some(fancy_validate))
    }

    #[pyo3(signature=(circuit, fancy_validate = Getter::default().default_fancy_validate))]
    pub fn get_unique_op(
        &self,
        circuit: CircuitRc,
        fancy_validate: bool,
    ) -> Result<Option<CircuitRc>> {
        Getter::default().get_unique_op(circuit, self_.crc(), Some(fancy_validate))
    }

    #[pyo3(signature=(circuit, fancy_validate = Getter::default().default_fancy_validate))]
    pub fn get_unique(&self, circuit: CircuitRc, fancy_validate: bool) -> Result<CircuitRc> {
        Getter::default().get_unique(circuit, self_.crc(), Some(fancy_validate))
    }

    pub fn get_paths(&self, circuit: CircuitRc) -> Result<BTreeMap<CircuitRc, Vec<CircuitRc>>> {
        Getter::default().get_paths(circuit, self_.crc())
    }
    pub fn get_all_paths(
        &self,
        circuit: CircuitRc,
    ) -> Result<BTreeMap<CircuitRc, Vec<Vec<CircuitRc>>>> {
        Getter::default().get_all_paths(circuit, self_.crc())
    }
    pub fn get_all_circuits_in_paths(&self, circuit: CircuitRc) -> Result<SetOfCircuitIdentities> {
        Getter::default().get_all_circuits_in_paths(circuit, self_.crc())
    }

    pub fn validate(&self, circuit: CircuitRc) -> Result<()> {
        Getter::default().validate(circuit, self_.crc())
    }

    #[pyo3(signature=(default_fancy_validate = Getter::default().default_fancy_validate))]
    pub fn getter(&self, default_fancy_validate: bool) -> BoundGetter {
        Getter::new(default_fancy_validate).bind(self_.crc())
    }

    pub fn are_any_found(&self, circuit: CircuitRc) -> Result<bool> {
        AnyFound::new().are_any_found(circuit, self_.crc())
    }
    pub fn any_found(&self) -> BoundAnyFound {
        AnyFound::new().bind(self_.crc())
    }

    #[pyo3(signature=(
        circuit,
        transform,
        fancy_validate = Updater::default().default_fancy_validate,
        assert_found = Updater::default().default_assert_found,
        assert_different = Updater::default().default_assert_different,
    ))]
    pub fn update(
        &self,
        circuit: CircuitRc,
        transform: TransformRc,
        fancy_validate: bool,
        assert_found: AssertFound,
        assert_different: bool,
    ) -> Result<CircuitRc> {
        Updater {
            transform,
            ..Default::default()
        }
        .update(
            circuit,
            self_.crc(),
            Some(fancy_validate),
            Some(assert_found),
            Some(assert_different),
        )
    }

    #[pyo3(signature=(
        transform,
        default_fancy_validate = Updater::default().default_fancy_validate,
        default_assert_found = Updater::default().default_assert_found,
        default_assert_different = Updater::default().default_assert_different,
    ))]
    pub fn updater(
        &self,
        transform: TransformRc,
        default_fancy_validate: bool,
        default_assert_found: AssertFound,
        default_assert_different: bool,
    ) -> BoundUpdater {
        Updater::new(
            transform,
            default_fancy_validate,
            default_assert_found,
            default_assert_different,
        )
        .bind(self_.crc())
    }

    pub fn apply_in_traversal(
        &self,
        circuit: CircuitRc,
        transform: TransformRc,
    ) -> Result<CircuitRc> {
        apply_in_traversal(circuit, self_.clone().rc(), |x| transform.run(x))
    }

    pub fn traversal_edges(&self, circuit: CircuitRc) -> Result<Vec<CircuitRc>> {
        Ok(
            replace_outside_traversal_symbols(circuit, self_.clone().rc(), |_| Ok(None))?
                .1
                .into_values()
                .collect(),
        )
    }
}

#[apply(python_error_exception)]
#[base_error_name(IterativeMatcher)]
#[base_exception(PyValueError)]
#[derive(Error, Debug, Clone)]
pub enum IterativeMatcherError {
    #[error(
        "num_updated_matchers={num_updated_matchers} != num_children={num_children}\nupdated_matchers={updated_matchers:?}, from_matcher={from_matcher:?}\n({e_name})"
    )]
    NumUpdatedMatchersNEQToNumChildren {
        num_updated_matchers: usize,
        num_children: usize,
        updated_matchers: Vec<Update>,
        from_matcher: IterativeMatcherRc,
    },

    #[error("operation doesn't support per child matching matchers={matchers:?}\n({e_name})")]
    OperationDoesntSupportArgPerChild { matchers: Vec<Update> },

    #[error("some child_numbers={child_numbers:?} >= num_children={num_children} ({e_name})")]
    ChildNumbersOutOfBounds {
        child_numbers: BTreeSet<usize>,
        num_children: usize,
    },

    #[error("matched circuit of type {circuit_type:?} is not a module ({e_name})")]
    ExpectedModule { circuit_type: CircuitType },
}

#[pyfunction]
#[pyo3(signature=(
    matcher,
    term_if_matches = false,
    start_depth = None,
    end_depth = None,
    term_early_at = MatcherFromPyBase::Always(false).into()
))]
pub fn restrict(
    matcher: IterativeMatcherRc,
    term_if_matches: bool,
    start_depth: Option<u32>,
    end_depth: Option<u32>,
    term_early_at: MatcherRc,
) -> IterativeMatcher {
    // TODO: flatten
    IterativeMatcherData::Restrict(RestrictIterativeMatcher::new(
        matcher,
        term_if_matches,
        start_depth,
        end_depth,
        term_early_at,
    ))
    .into()
}

#[pyfunction]
#[pyo3(signature=(
    matcher,
    term_if_matches = false,
    depth_slice = Slice::IDENT,
    term_early_at = MatcherFromPyBase::Always(false).into()
))]
pub fn restrict_sl(
    matcher: IterativeMatcherRc,
    term_if_matches: bool,
    depth_slice: Slice,
    term_early_at: MatcherRc,
) -> Result<IterativeMatcher> {
    Ok(restrict(
        matcher,
        term_if_matches,
        flip_op_result(depth_slice.start.map(|x| x.try_into()))?,
        flip_op_result(depth_slice.stop.map(|x| x.try_into()))?,
        term_early_at,
    ))
}

#[pyfunction]
#[pyo3(signature=(
    start_depth = None,
    end_depth = None,
    term_early_at = MatcherFromPyBase::Always(false).into()
))]
pub fn new_traversal(
    start_depth: Option<u32>,
    end_depth: Option<u32>,
    term_early_at: MatcherRc,
) -> IterativeMatcher {
    restrict(
        IterativeMatcher::noop_traversal().into(),
        false,
        start_depth,
        end_depth,
        term_early_at,
    )
}
