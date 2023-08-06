import hypothesis
import hypothesis.extra.numpy as st_np
import hypothesis.strategies as st
import pytest
import torch
from hypothesis import given, note
from torch.testing import assert_close

import rust_circuit as rc
from interp.circuit.testing.topdown_circuit import CircuitProbs as CP
from interp.circuit.testing.utils import mark_not_interesting_if
from rust_circuit import (
    Index,
    IterativeMatcherIn,
    Module,
    Parser,
    PushDownIndexError,
    PushDownIndexModuleSomeAxesNotPossibleError,
    default_index_traversal,
    new_traversal,
    push_down_index,
    push_down_index_once,
    restrict,
)

from .test_algebric_rewrites import check_transform_equality
from .util import st_Circuit

po = rc.PrintOptions(tensor_index_literal=True, bijection=False)


def run_test_push_down_index_raw(circuit: Index, options, traversal: IterativeMatcherIn = new_traversal()):
    note(circuit.repr(po))
    new_circ = push_down_index(circuit.cast_index(), traversal=traversal, **options)
    if hypothesis.currently_in_test_context():
        hypothesis.assume(new_circ != circuit)
    note(new_circ.repr(po))
    x = circuit.evaluate()
    assert_close(circuit.evaluate(), new_circ.evaluate().type(x.dtype))


index_probs = CP.kw(
    all=0, Index=(1, dict(allow_out_of_bounds_slice=False, allow_none_slice=False, allow_neg_slice=False))
)

options_st = st.fixed_dictionaries(
    dict(
        allow_partial_pushdown=st.booleans(),
        into_module_spec=st.booleans(),
        elim_identity=st.booleans(),
    )
)


@given(
    circuit=st_Circuit(
        st_np.array_shapes(min_dims=0),
        must_be_explicitly_computable=True,
        max_growth_steps=10,
        probs_per_depth=[index_probs],
        probs_default=CP.kw(all=1, Cumulant=0),  # TODO fix bugs and make this 1
        rust=True,
    ),
    options=options_st,
)
@hypothesis.settings(suppress_health_check=[hypothesis.HealthCheck.filter_too_much])
@mark_not_interesting_if(PushDownIndexError)
def test_push_down_index(circuit: Index, options):
    run_test_push_down_index_raw(circuit, options)


@given(
    circuit=st_Circuit(
        st_np.array_shapes(min_dims=0),
        must_be_explicitly_computable=True,
        max_growth_steps=10,
        probs_per_depth=[index_probs],
        probs_default=CP.kw(all=1, Cumulant=0),
        rust=True,
    ),
    options=options_st,
    end_depth=st.integers(min_value=1, max_value=5),
)
@hypothesis.settings(suppress_health_check=[hypothesis.HealthCheck.filter_too_much])
@mark_not_interesting_if(PushDownIndexError)
def test_push_down_index_variable_iters(circuit: Index, options, end_depth: int):
    run_test_push_down_index_raw(circuit, options, restrict(default_index_traversal(), end_depth=end_depth))


@given(
    circuit=st_Circuit(
        st_np.array_shapes(min_dims=0),
        must_be_explicitly_computable=True,
        max_growth_steps=4,
        probs_per_depth=[index_probs, CP.kw(all=0, Concat=1)],
        probs_default=CP.kw(all=1, Cumulant=0),
        rust=True,
    ),
    options=options_st,
)
@hypothesis.settings(suppress_health_check=[hypothesis.HealthCheck.filter_too_much])
@mark_not_interesting_if(PushDownIndexError)
def test_push_down_index_concat(circuit: Index, options):
    run_test_push_down_index_raw(circuit, options)


@given(
    circuit=st_Circuit(
        st_np.array_shapes(min_dims=0),
        must_be_explicitly_computable=True,
        max_growth_steps=4,
        probs_per_depth=[index_probs, CP.kw(all=0, Einsum=1)],
        probs_default=CP.kw(all=1, Cumulant=0),
        rust=True,
    ),
    options=options_st,
)
@hypothesis.settings(suppress_health_check=[hypothesis.HealthCheck.filter_too_much])
@mark_not_interesting_if(PushDownIndexError)
def test_push_down_index_einsum(circuit: Index, options):
    run_test_push_down_index_raw(circuit, options)


# @given(
#     circuit=st_Circuit(
#         st_np.array_shapes(min_dims=0),
#         must_be_explicitly_computable=True,
#         max_growth_steps=4,
#         probs_per_depth=[index_probs, CP.kw(all=0, Cumulant=1)],
#     )
# )
# @mark_not_interesting_if(PushDownIndexError)
# def test_push_down_index_cumulant(circuit: Index):
#     run_test_push_down_index_raw(circuit)


def test_push_down_index_module_manual():
    s = """
    'spec' Einsum ij,kj,i->kj
      'arg0' [2, 3] Symbol cf812243-3520-40c0-8dc8-56ee05f0fa94
      'arg1' [?, 3] Symbol c2ff6f83-a8cd-4f3e-b16a-476cce27b4c0
      'arg2' [2] Symbol 8f1b8454-43b8-422a-ade0-ee0c1ff136b1

    'a' Module
      'spec'
      'arg0_nb' [2, 3] Array rand ! 'arg0'
      'arg1_nb' [4, 3] Array rand ! 'arg1'
      'arg2_nb' [2] Array rand ! 'arg2'

    'b' Module
      'spec'
      'arg0_b_few' [4, 5, 2, 3] Array rand ! 'arg0'
      'arg1_nb' ! 'arg1'
      'arg2_nb' ! 'arg2'

    'c' Module
      'spec'
      'arg0_b_sing' [7, 2, 3] Array rand ! 'arg0'
      'arg1_nb' ! 'arg1'
      'arg2_b_sing' [7, 2] Array rand ! 'arg2'

    'd' Module
      'spec'
      'arg0_nb' ! 'arg0'
      'arg1_nb' ! 'arg1'
      'arg2_few' [3, 7, 2] Array rand ! 'arg2'

    'e' Module
      'spec'
      'arg0_few' [2, 3] Array rand ! 'arg0'
      'arg1_few' [3, 7, 4, 3] Array rand ! 'arg1'
      'arg2_b_sing' ! 'arg2'

    'f' Module
      'spec'
      'arg0_s_few' [7, 2, 3] Array rand ! 'arg0'
      'arg1_few' ! 'arg1'
      'arg2_b_sing' ! 'arg2'
    """
    spec, *mods = Parser().parse_circuits(s)
    for m in mods:
        num_batch_dims = m.rank - spec.rank

        idxed = m.index([], name="m_idxed")
        out = push_down_index_once(idxed, allow_partial_pushdown=False)
        assert isinstance(out, Module)
        torch.testing.assert_close(out.evaluate(), idxed.evaluate())

        idxed = m.index([0] * num_batch_dims, name="m_idxed")
        out = push_down_index_once(idxed, allow_partial_pushdown=False)
        assert isinstance(out, Module)
        torch.testing.assert_close(out.evaluate(), idxed.evaluate())

        assert push_down_index_once(idxed, allow_partial_pushdown=False) == out
        assert (
            push_down_index_once(
                m.index([*([0] * num_batch_dims), slice(None), slice(None)], name="m_idxed"),
                allow_partial_pushdown=False,
            )
            == out
        )

        idxed_more = m.index([0] * (num_batch_dims + 1), name="m_idxed")

        with pytest.raises(PushDownIndexModuleSomeAxesNotPossibleError):
            push_down_index_once(idxed_more, allow_partial_pushdown=False)

        push_idxed_more = push_down_index_once(idxed_more, allow_partial_pushdown=True)
        assert push_idxed_more.are_any_found(spec)  # still has spec
        assert isinstance(push_idxed_more, Index)

        torch.testing.assert_close(push_idxed_more.evaluate(), idxed_more.evaluate())
