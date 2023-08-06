use circuit_base::{deep_map_op_context, CircuitNode, CircuitRc};
use pyo3::prelude::*;

use crate::circuit_optimizer::OptimizationContext;

/// don't change symbols bc their names matter for correctness
#[pyfunction]
#[pyo3(name = "strip_names_and_tags")]
pub fn strip_names_and_tags_py(circuit: CircuitRc) -> CircuitRc {
    strip_names_and_tags(circuit, &mut Default::default())
}

pub fn strip_names_and_tags(circuit: CircuitRc, context: &mut OptimizationContext) -> CircuitRc {
    deep_map_op_context(
        circuit.clone(),
        &|circuit, _| {
            if let Some(tag) = circuit.as_tag() {
                return Some(tag.node());
            }
            if circuit.info().name.is_some() {
                if circuit.is_irreducible_node() {
                    return None;
                } else {
                    return Some(circuit.rename(None));
                }
            }
            None
        },
        &mut (),
        &mut context.cache.stripped_names,
    )
    .unwrap_or(circuit)
}
