from datetime import timedelta
from functools import partial
from typing import Any, Callable, List, Sequence, Set, Tuple, cast

import hypothesis
import hypothesis.extra.numpy as st_np
import hypothesis.strategies as st
import torch
from hypothesis import example, given

import interp.circuit.testing.strategies as st_c
import rust_circuit as rc
from interp.circuit.circuit_compiler.util import TorchAxisIndex
from interp.circuit.testing.topdown_circuit import CircuitProbs as CP
from interp.circuit.testing.utils import mark_not_interesting_if, target_diff
from rust_circuit import Add
from rust_circuit import Add as rAdd
from rust_circuit import Array
from rust_circuit import Circuit
from rust_circuit import Circuit as rCircuit
from rust_circuit import Concat
from rust_circuit import Einsum
from rust_circuit import Einsum as rEinsum
from rust_circuit import Index, Matcher, Parser, Rearrange
from rust_circuit import Scalar
from rust_circuit import Scalar as rScalar
from rust_circuit import Tag, apply_in_traversal, new_traversal, replace_outside_traversal_symbols, simp
from rust_circuit.algebric_rewrite import (
    ImpossibleRewriteError,
    RewriteError,
    distribute_old,
    drop_from_add,
    drop_mul_ones,
    drop_zero_add,
    einsum_flatten_bans_noop,
    eliminate_zeros,
    explicit_reduce,
    explicit_squeeze,
    extract_add,
    extract_add_by_match,
    extract_input_diags,
    extract_output_diags,
    factor_add_of_mul_to_mul_of_add,
    flatten_adds,
    fuse_einsum_permute,
    fuse_einsum_rearrange,
    fuse_einsum_single,
    fuse_permute_einsum,
    fuse_rearrange,
    fuse_single_einsum,
    multiply_axes_by_identity,
    nested_einsum_axes_permute,
    nested_einsum_permute_dups_to_eq,
    permute_to_einsum,
    pull_through_add_concat,
    pull_through_add_index,
    pull_through_add_rearrange,
    push_down_permute_via_einsum,
    rearrange_of_const_to_const,
    remove_empty_einsum,
    remove_noop_rearrange,
    remove_single_concat,
    remove_trivial_index,
    split_einsum_concat,
    split_to_concat_for_batch,
    zero_empty_add,
)

from .util import dedup_with_order, st_Circuit

P = Parser()
po = rc.PrintOptions(tensor_index_literal=True, bijection=False)


def is_zero(c: Circuit):
    return c.is_scalar() and c.cast_scalar().is_zero()


@st.composite
def st_index_groups(draw: st.DrawFn, length: int) -> List[List[int]]:
    # Generate index groups. Subtract from the available positions at every
    # step. Stop when we draw a False boolean or when we have no space left.
    available_space: List[Tuple[int, int]] = [(0, length)]
    index_groups: List[List[int]] = []
    first_iter = True

    # While there is space left, or we may randomly stop
    while first_iter or (len(available_space) > 0 and draw(st.booleans())):
        first_iter = False

        # Choose an available space
        space_idx = draw(st.integers(0, len(available_space) - 1))
        i_start, i_end = available_space.pop(space_idx)

        # Generate group indices from the available space
        group_start = draw(st.integers(i_start, i_end - 1))
        group_end = draw(st.integers(i_start, i_end - 1))
        group_start, group_end = sorted([group_start, group_end])
        group_end += 1

        # Add back the remaining space
        if i_start != group_start:
            available_space.append((i_start, group_start))
        if i_end != group_end:
            available_space.append((group_end, i_end))

        # Put our group in the generated groups, as a collection of contiguous indices
        index_groups.append(list(range(group_start, group_end)))
    return index_groups


@st.composite
def st_index_groups_and_circuit(
    draw: st.DrawFn, must_be_explicitly_computable: bool = True
) -> Tuple[List[List[int]], int, rCircuit]:
    st_shapes = st_np.array_shapes(min_dims=1, max_dims=4, max_side=8)
    st_circuit = st_Circuit(
        st_shapes,
        must_be_explicitly_computable=must_be_explicitly_computable,
        max_growth_steps=10,
        probs_default=CP.kw(all=1),
        probs_per_depth=[
            CP.kw(all=0, Einsum=(1, dict(min_n_children=1))),
            CP.kw(all=0, Concat=40),
        ],
    )
    circuit = draw(st_circuit)
    assert isinstance(circuit, Einsum) and len(circuit.args) > 0

    concat_idxs = [i for i, c in enumerate(circuit.children) if isinstance(c, Concat)]
    hypothesis.assume(len(concat_idxs) > 0, "no concat indices")
    which = concat_idxs[draw(st.integers(min_value=0, max_value=len(concat_idxs) - 1))]

    index_groups_target: Concat = circuit.children[which].cast_concat()
    index_groups = draw(st_index_groups(index_groups_target.num_children))
    return index_groups, which, circuit


@hypothesis.settings(
    max_examples=10,
    suppress_health_check=[hypothesis.HealthCheck.filter_too_much, hypothesis.HealthCheck.too_slow],
    deadline=timedelta(seconds=4),
)
@given(groups_and_circuit=st_index_groups_and_circuit())
@mark_not_interesting_if(NotImplementedError)
def test_auto_split_einsum_concat(groups_and_circuit):
    index_groups, which, circuit = groups_and_circuit
    check_transform_equality(partial(split_einsum_concat, element_index=which, index_groups=index_groups), circuit)


@mark_not_interesting_if(RewriteError)
# use Any for `fn` type to avoid errors
def check_transform_equality(
    fn: Callable[[Any], rCircuit], circuit: Circuit, sample: bool = False, f64: bool = True
) -> Circuit:
    """
    Checks that when we apply the rewrite `fn` to `circuit` the evaluated circuit has the same value

    ..note:: we make sure that enough cases for each rewrite are tested by marking the test example as invalid if the
        rewrite noops.

      Thus, we enforce that rewrites have to raise :class:`NoopRewriteError` whenever they would noop (or sometimes just
      :class:`NotImplementedError`. This is true for all rewrites *except* :func:`rearrange_muls`. In that case, many successful rearranges
      would leave the tree of Einsums equal, and so this doesn't make sense.
    """
    if f64:
        circuit = rc.cast_circuit(circuit, rc.TorchDeviceDtypeOp(dtype="float64"))
    trans = fn(circuit)

    assert trans.shape == circuit.shape
    assert trans != circuit, "The rewrite should raise a RewriteError instead of nooping."

    if sample:
        sampler = rc.Sampler(rc.RunDiscreteVarAllSpec.create_full_from_circuits(trans, circuit))
        trans_eval = sampler(trans)
        circuit_eval = sampler(circuit)
    else:
        trans_eval = trans
        circuit_eval = circuit

    hypothesis.note(circuit_eval.repr(po))
    hypothesis.note(trans_eval.repr(po))
    actual, expected = (trans_eval.evaluate(), circuit_eval.evaluate())
    target_diff(actual.type(expected.dtype), expected)  # , evaluator=evaluator)
    return trans


@hypothesis.settings(deadline=None)
@given(
    circuit=st_Circuit(
        st_np.array_shapes(min_dims=0),
        must_be_explicitly_computable=True,
        max_growth_steps=10,
        # Sample more relevant nodes at depth 0 and more zeros at depth 1
        probs_default=CP.kw(all=1, Scalar=(5, dict(values=[0.0], also_any=True))),
        probs_per_depth=[CP.kw(all=0, Add=10, Einsum=10, Rearrange=10, Index=10)],
    )
)
def test_eliminate_zeros(circuit):
    """
    Check that if the top level is a :class:`Einsum` or :class:`Rearrange` or :class:`Index` or :class:`Add`, it has been
    replaced by a zero (and the shape is still the same). Also exact float equality.
    """
    transformed_circuit = check_transform_equality(eliminate_zeros, circuit)

    assert not any(is_zero(c) for c in transformed_circuit.children)


@given(
    circuit=st_Circuit(
        st_np.array_shapes(min_dims=0),
        must_be_explicitly_computable=True,
        max_growth_steps=10,
        probs_default=CP.kw(all=1),
        probs_per_depth=[CP.kw(all=0, Einsum=1), CP.kw(all=1, Scalar=(20, dict(values=[1.0], also_any=True)))],
    )
)
@hypothesis.settings(deadline=timedelta(milliseconds=400))
def test_drop_mul_ones(circuit):
    check_transform_equality(drop_mul_ones, circuit)


@given(
    circuit=st_Circuit(
        st_np.array_shapes(min_dims=0),
        must_be_explicitly_computable=True,
        max_growth_steps=3,
        probs_per_depth=[CP.kw(all=0, Rearrange=1), CP.kw(all=0, Scalar=(1, dict(values=[0.0, 1.0])))],
    )
)
def test_rearrange_of_const_to_const(circuit):
    check_transform_equality(rearrange_of_const_to_const, circuit)


@given(
    circuit=st_Circuit(
        st_np.array_shapes(min_dims=0),
        must_be_explicitly_computable=True,
        max_growth_steps=10,
        probs_default=CP.kw(all=1, Add=20),
        probs_per_depth=[CP.kw(all=0, Add=20)],
        add_must_have_weight_one=True,
    )
)
def test_flatten_adds(circuit):
    """`
    Check that if the top-most circuit is an Add, and we apply `flatten_adds`
    many times, we can get rid of the Add children.
    """
    circuit.evaluate()
    n_nodes = len(rc.all_children(circuit))  # An upper bound on the number of `flatten_adds` transforms we need

    trans = circuit
    n_iter = 0
    while isinstance(trans, rAdd) and any(isinstance(c, rAdd) for c in trans.children):
        try:
            trans = flatten_adds(trans)
        except ImpossibleRewriteError as e:
            raise RuntimeError(f"There are child adds, should not have raised {e}")
        assert trans.shape == circuit.shape
        torch.testing.assert_close(trans.evaluate(), circuit.evaluate())
        n_iter += 1
        assert n_iter <= n_nodes, "flatten_adds is not getting rid of the `Add`s"


@hypothesis.settings(
    max_examples=10, suppress_health_check=[hypothesis.HealthCheck.filter_too_much, hypothesis.HealthCheck.too_slow]
)
@given(
    circuit=st_Circuit(
        st_np.array_shapes(min_dims=0),
        must_be_explicitly_computable=True,
        max_growth_steps=3,
        probs_default=CP.kw(all=1),
        probs_per_depth=[CP.kw(all=0, Rearrange=(1, dict(do_squeeze=True)), Einsum=0)],
        rust=True,
    )
)
def test_explicit_squeeze(circuit: rc.Rearrange):
    check_transform_equality(explicit_squeeze, circuit)


@hypothesis.settings(
    max_examples=20,
    suppress_health_check=[hypothesis.HealthCheck.filter_too_much, hypothesis.HealthCheck.too_slow],
    deadline=None,
)
@given(
    circuit=st_Circuit(
        st_np.array_shapes(min_dims=0),
        must_be_explicitly_computable=True,
        max_growth_steps=3,
        probs_default=CP.kw(all=1),
        probs_per_depth=[CP.kw(all=0, Rearrange=1, Einsum=1)],
    )
)
def test_remove_noop_rearrange(circuit):
    check_transform_equality(remove_noop_rearrange, circuit)


@given(
    circuit=st_Circuit(
        st_np.array_shapes(min_dims=1),
        must_be_explicitly_computable=True,
        max_growth_steps=3,
        probs_default=CP.kw(all=1),
    ),
    keep_name=st.booleans(),
    axis=st.integers(min_value=0, max_value=5),
)
def test_remove_single_concat(circuit: Circuit, keep_name: bool, axis: int):
    assert circuit.ndim > 0
    add_circuit = Concat(circuit, axis=axis % circuit.ndim)
    trans = check_transform_equality(partial(remove_single_concat, keep_name=keep_name), add_circuit)
    if keep_name:
        assert trans.name == add_circuit.name


@st.composite
def generate_einsum_with_squeeze(draw: st.DrawFn) -> Tuple[int, int, Einsum]:
    ein = draw(
        st_Circuit(
            st_np.array_shapes(min_dims=0, max_dims=7),
            must_be_explicitly_computable=True,
            max_growth_steps=3,
            probs_default=CP.kw(all=1, Rearrange=20),
            probs_per_depth=[CP.kw(all=0, Einsum=(1, dict(min_n_children=1)))],
        )
    ).cast_einsum()
    to_unsqueeze_arg = draw(st.integers(min_value=0, max_value=len(ein.args) - 1))
    # (node, axes), other_args = ein.get_info_by(to_unsqueeze_arg)
    args = ein.args
    node, axes = args[to_unsqueeze_arg]
    to_unsqueeze_axis = draw(st.integers(min_value=0, max_value=len(axes)))

    new_node = node.unsqueeze([to_unsqueeze_axis])
    new_axes = axes[:to_unsqueeze_axis] + (ein.next_axis(),) + axes[to_unsqueeze_axis:]
    assert new_node.shape[to_unsqueeze_axis] == 1
    args[to_unsqueeze_arg] = (new_node, new_axes)

    new_ein = Einsum(*args, out_axes=ein.out_axes, name=ein.name)
    return to_unsqueeze_arg, to_unsqueeze_axis, new_ein


@hypothesis.settings(deadline=None, suppress_health_check=[hypothesis.HealthCheck.filter_too_much])
@given(
    circuit=st_Circuit(
        st_np.array_shapes(min_dims=0, max_dims=1),  # only rank 0 ever produces ident indices
        must_be_explicitly_computable=True,
        max_growth_steps=1,
        probs_default=CP.kw(all=1),
        probs_per_depth=[CP.kw(all=0, Index=1)],
    )
)
def test_remove_trivial_index(circuit: Index):
    check_transform_equality(remove_trivial_index, circuit)


@given(
    circuit=st_Circuit(
        st_np.array_shapes(min_dims=0),
        must_be_explicitly_computable=True,
        max_growth_steps=2,
        probs_default=CP.kw(all=1),
        probs_per_depth=[CP.kw(all=0, Einsum=1)],
    )
)
def test_remove_empty_einsum(circuit: Einsum):
    check_transform_equality(remove_empty_einsum, circuit)


@st.composite
def st_add_and_subset(draw: st.DrawFn) -> Tuple[Add, Set[Circuit]]:
    """
    Sample an Add circuit and a subset of its
    children (to be removed by drop_from_add,
    see test below)
    """

    circuit: Add = draw(
        st_Circuit(
            st_np.array_shapes(min_dims=0),
            must_be_explicitly_computable=True,
            max_growth_steps=1,
            probs_per_depth=[CP.kw(all=0, Add=1)],
            add_must_have_weight_one=True,
        )
    ).cast_add()
    children = circuit.children
    assert len(children) == len(set(children))

    if len(children) == 0:
        subset = []
    else:
        subset = draw(st.lists(elements=st.sampled_from(children), min_size=0, max_size=len(children), unique=True))
    return (circuit, set(subset))


@given(circuit_and_subset=st_add_and_subset())
def test_drop_from_add(circuit_and_subset: Tuple[Add, Set[Circuit]]):
    circuit: Add
    subset: Set[Circuit]
    circuit, subset = circuit_and_subset
    try:
        children = circuit.children
        hypothesis.assume(len(set(children)) == len(children))
        new_circuit = drop_from_add(circuit, subset, noop_error=True)
    except RewriteError:
        hypothesis.reject()

    assert len(subset) > 0

    assert new_circuit.shape == circuit.shape
    assert new_circuit != circuit, "The rewrite should raise ImpossibleRewriteError instead of nooping"

    if isinstance(new_circuit, Rearrange):
        new_children = new_circuit.node.children
    elif is_zero(new_circuit):
        new_children = []
    elif isinstance(new_circuit, Add):
        new_children = new_circuit.children
    else:
        assert False

    assert len(new_children) == circuit.num_children - len(
        subset
    ), f"{len(new_children)} != {circuit.num_children} - {len(subset)}; {new_circuit}"

    for deleted_circuit in subset:
        assert deleted_circuit not in new_children

    old_circuit_with_zeros = Add.from_weighted_nodes(
        *((k, (0.0 if k in subset else v)) for k, v in circuit.to_counts().items())
    )
    old_circuit_with_zeros = rc.cast_circuit(old_circuit_with_zeros, rc.TorchDeviceDtypeOp(dtype="float64"))

    new_out = new_circuit.evaluate()
    torch.testing.assert_close(old_circuit_with_zeros.evaluate().type(new_out.dtype), new_out)


# this only activates if add weight is 0, which is rare, so don't demand many examples
@hypothesis.settings(max_examples=5, suppress_health_check=[hypothesis.HealthCheck.filter_too_much])
@given(
    circuit=st_Circuit(
        st_np.array_shapes(min_dims=0),
        must_be_explicitly_computable=True,
        max_growth_steps=1,
        probs_default=CP.kw(all=1),
        probs_per_depth=[CP.kw(all=0, Add=1)],
    )
)
def test_drop_zero_add(circuit):
    check_transform_equality(drop_zero_add, circuit)


@hypothesis.example(
    circuit=Add(),
)
@given(
    circuit=st_Circuit(
        st_np.array_shapes(min_dims=0),
        must_be_explicitly_computable=True,
        max_growth_steps=1,
        probs_default=CP.kw(all=1),
        probs_per_depth=[CP.kw(all=0, Add=1).add(Add=(10, dict(min_n_children=0, max_n_children=0)))],
    )
)
def test_zero_empty_add(circuit: Add):
    check_transform_equality(zero_empty_add, circuit)


@st.composite
def st_distributed_einsum(draw: st.DrawFn):
    c: Einsum = draw(
        st_Circuit(
            st_np.array_shapes(min_dims=0),
            must_be_explicitly_computable=True,
            max_growth_steps=5,
            probs_default=CP.kw(all=1),
            probs_per_depth=[CP.kw(all=0, Einsum=(1, dict(min_n_children=2, max_n_children=2)))],
        )
    ).cast_einsum()
    assert c.num_children == 2

    ((a, a_axes), (b, b_axes)) = c.args
    out_axes = c.out_axes

    circuits = [c]

    for summand_index in range(1, 5):
        if draw(st.booleans()):
            break
        new_b = draw(
            st_Circuit(
                b.shape,
                must_be_explicitly_computable=True,
                max_growth_steps=5,
            )
        )

        c_p = Einsum((a, a_axes), (new_b, b_axes), out_axes=out_axes)
        assert out_axes == c_p.out_axes
        circuits.append(c_p)

    return Add(*circuits)


@given(einsum_circuit=st_distributed_einsum(), is_lhs=st.booleans())
def test_factor_add_of_mul_to_mul_of_add(einsum_circuit: Add, is_lhs: bool):
    check_transform_equality(partial(factor_add_of_mul_to_mul_of_add, is_lhs=is_lhs), einsum_circuit)


@st.composite
def st_concat_add(draw: st.DrawFn):
    circuit = draw(
        st_Circuit(
            st_np.array_shapes(min_dims=1),
            must_be_explicitly_computable=True,
            max_growth_steps=5,
            probs_per_depth=[
                CP.kw(all=0, Add=1),
            ],
        )
    )

    assert isinstance(circuit, Add)
    childrens_shapes = [child.shape for child in circuit.children]
    adds = [circuit]

    concat_axis = draw(st.integers(min_value=0, max_value=len(circuit.shape) - 1))

    concat_length = draw(st.integers(min_value=1, max_value=5))

    for add_idx in range(1, concat_length):
        children: List[Circuit] = []

        for child_shape in childrens_shapes:
            children.append(
                draw(
                    st_Circuit(
                        child_shape,
                        must_be_explicitly_computable=True,
                        max_growth_steps=5,
                    )
                )
            )

        adds.append(Add.from_weighted_nodes(*((child, draw(st_c.bounded_floats)) for child in children)))

    return Concat(*adds, axis=concat_axis)


# @hypothesis.settings(suppress_health_check=[hypothesis.HealthCheck.filter_too_much, hypothesis.HealthCheck.too_slow])
# @given(circuit=st_concat_add())
# def test_distribute_concat(circuit):
#     summand_to_pull_out = 0
#     check_transform_equality(lambda c: distribute_concat(c, summand_to_pull_out), circuit)


@st.composite
def st_add_concat(draw: st.DrawFn):
    circuit = draw(
        st_Circuit(
            st_np.array_shapes(min_dims=1),
            must_be_explicitly_computable=True,
            max_growth_steps=20,
            probs_per_depth=[
                CP.kw(all=0, Concat=1),
            ],
            add_must_have_weight_one=True,
        )
    )

    assert isinstance(circuit, Concat)
    childrens_shapes = [child.shape for child in circuit.children]
    concats = [circuit]

    sum_length = draw(st.integers(min_value=0, max_value=5))
    if sum_length == 0:
        concats = []

    for concat_idx in range(1, sum_length):
        children: List[Circuit] = []

        for child_shape in childrens_shapes:
            children.append(
                draw(
                    st_Circuit(
                        child_shape,
                        must_be_explicitly_computable=True,
                        max_growth_steps=5,
                    )
                )
            )

        concats.append(
            Concat(
                *children,
                # tuple((child, draw(st_c.bounded_floats)) for child in children),
                axis=circuit.axis,
            )
        )

    return Add.from_weighted_nodes(*[(concat, draw(st_c.bounded_floats)) for concat in concats])


@hypothesis.settings(
    suppress_health_check=[hypothesis.HealthCheck.filter_too_much, hypothesis.HealthCheck.too_slow], deadline=None
)
@given(circuit=st_add_concat())
def test_pull_through_add_concat(circuit):
    check_transform_equality(pull_through_add_concat, circuit)


@given(
    circuit=st_Circuit(
        st_np.array_shapes(min_dims=0),
        must_be_explicitly_computable=True,
        max_growth_steps=10,
        growth_order="breadth_first",
        probs_default=CP.kw(all=1),
        probs_per_depth=[CP.kw(all=0, Add=(1, dict(max_n_children=3))), CP.kw(all=0, Index=1)],
        add_must_have_weight_one=True,
    )
)
@example(circuit=Add(Index(node=Scalar(0.0, (1,)), index=(0,)), Index(node=Scalar(1.0, (1,)), index=(0,))))
@example(
    circuit=Add(
        Index(node=Scalar(0.0, shape=(25, 30)), index=(slice(2, 12), 3)),
        Index(node=Scalar(1.0, shape=(25, 30)), index=(slice(2, 12), 3)),
    )
)
def test_pull_through_add_index(circuit: Add):
    assert all(isinstance(c, Index) for c in circuit.children)
    check_transform_equality(pull_through_add_index, circuit)


@hypothesis.settings(suppress_health_check=[hypothesis.HealthCheck.filter_too_much])
@given(
    circuit=st_Circuit(
        st_np.array_shapes(min_dims=0),
        must_be_explicitly_computable=True,
        max_growth_steps=3,
        probs_default=CP.kw(all=1),
        probs_per_depth=[
            CP.kw(all=0, Add=1),
            CP.kw(all=1, Rearrange=(50, dict(do_squeeze=False))),
        ],
        add_must_have_weight_one=True,
    )
)
def test_pull_through_add_rearrange(circuit):
    check_transform_equality(pull_through_add_rearrange, circuit)


@given(
    circuit=st_Circuit(
        st_np.array_shapes(min_dims=0),
        must_be_explicitly_computable=True,
        max_growth_steps=3,
        probs_per_depth=[
            CP.kw(all=0, Einsum=1),
            CP.kw(all=1, Rearrange=(50, dict(do_split=False, do_unsqueeze=False, do_repeat=False, do_squeeze=False))),
        ],
    )
)
@hypothesis.example(
    circuit=Einsum(
        (
            rc.Rearrange.from_string(Scalar(0.0, shape=(1, 2, 1), name=""), "a:1 c:2 b:1 -> a b c"),
            (0, 0, 1),
        ),
        (Scalar(0.0, shape=(), name=""), ()),
        (Scalar(0.0, shape=(1,), name=""), (0,)),
        out_axes=(0, 1),
        name="given_test",
    ),
)
def test_fuse_einsum_permute(circuit: Einsum):
    check_transform_equality(fuse_einsum_permute, circuit)


@given(
    circuit=st_Circuit(
        st_np.array_shapes(min_dims=0),
        must_be_explicitly_computable=True,
        max_growth_steps=3,
        probs_per_depth=[
            CP.kw(all=0, Einsum=1),
            CP.kw(all=1, Rearrange=(50, dict(do_split=False, do_unsqueeze=True, do_repeat=True))),
        ],
    )
)
def test_fuse_einsum_rearrange(circuit: Einsum):
    check_transform_equality(fuse_einsum_rearrange, circuit)


@given(
    circuit=st_Circuit(
        st_np.array_shapes(min_dims=0),
        must_be_explicitly_computable=True,
        max_growth_steps=5,
        probs_default=CP.kw(all=1),
        probs_per_depth=[CP.kw(all=0, Rearrange=1), CP.kw(all=1, Einsum=50)],
    )
)
@hypothesis.example(
    circuit=rc.Rearrange.from_string(
        Einsum(
            (Scalar(0.0, shape=(2, 1), name=""), (0, 1)),
            out_axes=(0, 1),
        ),
        "b:2 a:1 -> a b",
    ),
)
@mark_not_interesting_if(ImpossibleRewriteError)
def test_fuse_permute_einsum(circuit):
    check_transform_equality(fuse_permute_einsum, circuit)


@given(
    circuit=st_Circuit(
        st_np.array_shapes(min_dims=0),
        must_be_explicitly_computable=True,
        max_growth_steps=5,
        probs_default=CP.kw(all=1),
        probs_per_depth=[
            CP.kw(all=0, Rearrange=1),
            CP.kw(all=0, Rearrange=1),
        ],
    )
)
@mark_not_interesting_if(ImpossibleRewriteError)
def test_fuse_rearrange(circuit):
    check_transform_equality(fuse_rearrange, circuit)


@given(
    circuit=st_Circuit(
        st_np.array_shapes(min_dims=0, max_dims=3),
        must_be_explicitly_computable=True,
        max_growth_steps=3,
        probs_default=CP.kw(all=1),
        probs_per_depth=[CP.kw(all=0, Einsum=(1, dict(min_n_children=1, max_n_children=1))), CP.kw(all=1, Einsum=50)],
    )
)
@mark_not_interesting_if(ImpossibleRewriteError)
def test_fuse_single_einsum(circuit):
    check_transform_equality(fuse_single_einsum, circuit)


@hypothesis.settings(deadline=timedelta(milliseconds=300))
@given(
    circuit=st_Circuit(
        st_np.array_shapes(min_dims=0),
        must_be_explicitly_computable=True,
        max_growth_steps=5,
        growth_order="breadth_first",
        probs_default=CP.kw(all=1),
        probs_per_depth=[
            CP.kw(all=0, Einsum=1),
            CP.kw(all=0, Einsum=1).add(Einsum=(50, dict(min_n_children=1, max_n_children=1))),
            CP.kw(all=1, Einsum=50),
        ],
    )
)
@mark_not_interesting_if(ImpossibleRewriteError)
def test_fuse_einsum_single(circuit: Einsum):
    check_transform_equality(fuse_einsum_single, circuit)


def test_fuse_einsum_single_simple():
    c = rEinsum(
        (rEinsum((rScalar(1.0), ()), out_axes=()), ()),
        (rEinsum((rScalar(1.0, (1,)), (0,)), out_axes=(0,)), (0,)),
        (rEinsum((rScalar(1.0, (1,)), (0,)), (rScalar(0.5, (1,)), (0,)), out_axes=(0,)), (0,)),
        (rEinsum((rScalar(1.0, (1,)), (0,)), (rScalar(0.5, (1,)), (1,)), out_axes=(0, 1)), (0, 1)),
        (rEinsum((rScalar(1.0, (1,)), (0,)), out_axes=(0,)), (1,)),
        out_axes=(1,),
    )
    r = rEinsum(
        (rScalar(1.0), ()),
        (rScalar(1.0, (1,)), (0,)),
        (rEinsum((rScalar(1.0, (1,)), (0,)), (rScalar(0.5, (1,)), (0,)), out_axes=(0,)), (0,)),
        (rEinsum((rScalar(1.0, (1,)), (0,)), (rScalar(0.5, (1,)), (1,)), out_axes=(0, 1)), (0, 1)),
        (rScalar(1.0, (1,)), (1,)),
        out_axes=(1,),
    )
    assert r == fuse_einsum_single(c)


def test_split_einsum_concat():
    a = Array(torch.randn(3, 4, 5), name="a")
    b = Array(torch.randn(3, 5, 7), name="b")
    c = Array(torch.randn(3, 4, 2), name="c")
    d = Array(torch.randn(3, 1, 5), name="d")
    e = Array(torch.randn(3, 2, 5), name="e")
    f = Array(torch.randn(3, 3, 5), name="f")

    # evaluator = MemoizedFn(evaluate_fn(dtype=torch.float64))
    for out in ["x w v y z", "x w v y", "z", "z w", "w", "y w", "y z", "y x"]:
        for concat in [Concat(a, c, axis=-1), Concat(a, f, d, e, axis=1)]:
            v = Einsum.from_einsum_string(f"x y z, x w v -> {out}", concat, b)

            all_groups: Tuple[List[List[int]], ...] = ([[0]], [[1]], [[0], [1]], [[1], [0]])
            if len(concat.children) > 2:
                all_groups += ([[1, 2]], [[3], [1, 2]], [[0], [2]], [[0], [3]])
            for groups in all_groups:
                torch.testing.assert_close(
                    v.evaluate(), split_einsum_concat(v, element_index=0, index_groups=groups).evaluate()
                )

    for out in ["x w y z", "x w y", "z", "z w", "w", "y w", "y z", "y x"]:
        for concat in [Concat(a, c, axis=-1), Concat(a, f, d, e, axis=1)]:
            l = Array(torch.randn(6, *concat.shape[1:]), name="z")
            v = Einsum.from_einsum_string(f"x y z, w y z -> {out}", concat, l)

            all_groups = ([[0]], [[1]], [[0], [1]], [[1], [0]])
            if len(concat.children) > 2:
                all_groups += ([[1, 2]], [[3], [0, 1, 2]], [[0], [2]], [[0], [3]])
            for groups in all_groups:
                torch.testing.assert_close(
                    v.evaluate(), split_einsum_concat(v, element_index=0, index_groups=groups).evaluate()
                )


@hypothesis.settings(
    suppress_health_check=[hypothesis.HealthCheck.filter_too_much, hypothesis.HealthCheck.too_slow],
    deadline=timedelta(seconds=6),
)
@given(
    circuit=st_Circuit(
        st_np.array_shapes(min_dims=0),
        must_be_explicitly_computable=True,
        max_growth_steps=4,
        growth_order="breadth_first",
        probs_default=CP.kw(all=1),
        probs_per_depth=[CP.kw(all=0, Einsum=(1, dict(min_n_children=1))), CP.kw(all=0, Add=1)],
    ),
    element_index=st.integers(0, 8),
)
@hypothesis.example(
    circuit=Einsum(
        (Add(), ()),
        (Add.from_weighted_nodes((Scalar(0.0, (1,)), 0.0)), (0,)),
        out_axes=(0,),
    ),
    element_index=0,
)
def test_distribute(circuit: Einsum, element_index: int):
    assert len(circuit.args) > 0
    check_transform_equality(partial(distribute_old, element_index=element_index), circuit)


@given(
    circuit=st_Circuit(
        st_np.array_shapes(min_dims=0),
        must_be_explicitly_computable=True,
        max_growth_steps=4,
        probs_default=CP.kw(all=1),
        probs_per_depth=[
            CP.kw(all=0, Rearrange=(1, dict(do_split=False, do_unsqueeze=False, do_repeat=False, do_squeeze=False)))
        ],
    )
)
def test_permute_to_einsum(circuit: Rearrange):
    assert circuit.spec.is_permute()
    check_transform_equality(permute_to_einsum, circuit)


@given(
    circuit=st_Circuit(
        st_np.array_shapes(min_dims=0),
        must_be_explicitly_computable=True,
        max_growth_steps=4,
        probs_default=CP.kw(all=1),
        probs_per_depth=[
            CP.kw(all=0, Rearrange=(1, dict(do_split=False, do_unsqueeze=False, do_repeat=False, do_squeeze=False))),
            CP.kw(all=0, Add=1),
        ],
    )
)
@mark_not_interesting_if(NotImplementedError)
def test_push_down_permute_via_einsum(circuit: Rearrange):
    assert circuit.spec.is_permute()
    assert isinstance(circuit.node, Add)
    check_transform_equality(push_down_permute_via_einsum, circuit)


ExplicitReduceArgs = Tuple[Einsum, int, int, Sequence[TorchAxisIndex]]


@st.composite
def st_explicit_reduce_args(draw: st.DrawFn, must_be_explicitly_computable: bool = True) -> ExplicitReduceArgs:
    st_circuit = st_Circuit(
        st_np.array_shapes(min_dims=0),
        must_be_explicitly_computable=must_be_explicitly_computable,
        max_growth_steps=4,
        probs_default=CP.kw(all=1),
        probs_per_depth=[CP.kw(all=0, Einsum=(1, dict(min_n_children=1)))],
    )
    circuit = draw(st_circuit)
    assert isinstance(circuit, Einsum) and len(circuit.args) > 0

    which = draw(st.integers(min_value=0, max_value=len(circuit.args) - 1))
    circ = circuit.children[which]
    if circ.ndim == 0:
        # Attempt the rewrite anyways, should raise ImpossibleRewriteError
        return circuit, 0, which, []

    axis = draw(st.integers(min_value=0, max_value=circ.ndim - 1))

    idxs: List[TorchAxisIndex] = []
    end = 0
    while end != circ.shape[axis]:
        if draw(st.booleans()):
            new_end = draw(st.integers(min_value=end, max_value=circ.shape[axis]))
            idxs.append(slice(end, new_end))
            end = new_end
        else:
            idxs.append(end)
            end += 1

    return circuit, axis, which, idxs


@given(
    circuit=st_Circuit(
        st.one_of(*[st.just(x) for x in [(2, 2), (3, 3, 3), (2, 2, 3, 3), (3, 3, 3, 2)]]),  # upsample diags!
        must_be_explicitly_computable=True,
        max_growth_steps=2,
        probs_default=CP.kw(all=1),
        probs_per_depth=[CP.kw(all=0, Einsum=(1, dict(min_n_children=1)))],
    ),
)
def test_extract_output_diag(circuit: Einsum):
    check_transform_equality(extract_output_diags, circuit)


@st.composite
def st_einsum_with_diag_index(draw: st.DrawFn, must_be_explicitly_computable: bool = True) -> tuple[Einsum, int]:
    circuit = draw(
        st_Circuit(
            st_np.array_shapes(min_dims=0),
            must_be_explicitly_computable=must_be_explicitly_computable,
            max_growth_steps=2,
            probs_default=CP.kw(all=1),
            probs_per_depth=[CP.kw(all=0, Einsum=(1, dict(min_n_children=1)))],
        )
    )
    assert isinstance(circuit, Einsum)

    index_options = [i for i, axes in enumerate(circuit.all_input_axes()) if len(set(axes)) < len(axes)]
    hypothesis.assume(len(index_options) > 0, "we need some duplicate axes")
    index = index_options[draw(st.integers(min_value=0, max_value=len(index_options) - 1))]

    return circuit, index


@given(
    einsum_diag=st_einsum_with_diag_index(must_be_explicitly_computable=True),
)
@hypothesis.settings(suppress_health_check=[hypothesis.HealthCheck.filter_too_much, hypothesis.HealthCheck.too_slow])
def test_extract_input_diag(einsum_diag: Tuple[Einsum, int]):
    einsum, diag_index = einsum_diag

    check_transform_equality(lambda x: extract_input_diags(x, diag_index), einsum)


@given(explicit_reduce_args=st_explicit_reduce_args())
@hypothesis.settings(deadline=None)
@mark_not_interesting_if(NotImplementedError)
def test_explicit_reduce(explicit_reduce_args: ExplicitReduceArgs):
    check_transform_equality(lambda c: explicit_reduce(c, *explicit_reduce_args[1:]), explicit_reduce_args[0])


@given(
    circuit=st_Circuit(
        st_np.array_shapes(min_dims=0),
        must_be_explicitly_computable=True,
        max_growth_steps=4,
        probs_default=CP.kw(all=1),
        probs_per_depth=[CP.kw(all=0, Einsum=1), CP.kw(all=1, Einsum=70)],
    )
)
@example(circuit=Einsum((Einsum(out_axes=()), ()), out_axes=()))
@mark_not_interesting_if(
    ValueError, message="einsum(): subscript in subscript list is not within the valid range [0, 52)"
)
def test_einsum_flatten_bans_noop(circuit: Einsum):
    check_transform_equality(lambda x: einsum_flatten_bans_noop(x), circuit)


ExtractAddArgs = Tuple[Add, Add]


@st.composite
def st_extract_add_args(draw: st.DrawFn, must_be_explicitly_computable: bool = True) -> ExtractAddArgs:
    st_circuit = st_Circuit(
        st_np.array_shapes(min_dims=1),
        must_be_explicitly_computable=must_be_explicitly_computable,
        max_growth_steps=2,
        probs_per_depth=[CP.kw(all=0, Add=1)],
    )
    circuit = draw(st_circuit)
    assert isinstance(circuit, Add)

    all_sub = dedup_with_order(
        draw(
            st.lists(
                elements=st.integers(min_value=0, max_value=len(circuit.children) - 1),
                max_size=len(circuit.children) - 1,
            )
        )
    )

    ch = circuit.children

    return circuit, Add(*(ch[i] for i in all_sub))


@given(extract_add_args=st_extract_add_args())
def test_extract_add(extract_add_args: ExtractAddArgs):
    circuit, sub = extract_add_args

    check_transform_equality(lambda x: extract_add(x, sub), circuit)


@hypothesis.settings(deadline=None)
@given(extract_add_args=st_extract_add_args())
def test_extract_add_by_match(extract_add_args: ExtractAddArgs):
    circuit, sub = extract_add_args
    matcher = Matcher(set(sub.children))

    check_transform_equality(lambda x: extract_add_by_match(x, matcher), circuit)


NestedEinsumAxesPermuteArgs = Tuple[Einsum, int, List[int]]


@st.composite
def st_nested_einsum_axes_permute_args(
    draw: st.DrawFn, must_be_explicitly_computable: bool = True
) -> NestedEinsumAxesPermuteArgs:
    st_circuit = st_Circuit(
        st_np.array_shapes(min_dims=0),
        must_be_explicitly_computable=must_be_explicitly_computable,
        max_growth_steps=2,
        probs_default=CP.kw(all=1),
        probs_per_depth=[CP.kw(all=0, Einsum=(1, dict(min_n_children=2, max_n_children=6))), CP.kw(all=1, Einsum=40)],
    )
    circuit = draw(st_circuit)
    assert isinstance(circuit, Einsum)

    einsums = [(i, x) for i, x in enumerate(circuit.children) if isinstance(x, Einsum)]
    hypothesis.assume(len(einsums) > 0, "no einsums")
    which = draw(st.integers(min_value=0, max_value=len(einsums) - 1))
    idx, einsum = einsums[which]
    perm = draw(st.permutations(range(einsum.ndim)))

    return circuit, idx, perm


@given(nested_einsum_axes_permute_args=st_nested_einsum_axes_permute_args())
@hypothesis.settings(suppress_health_check=[hypothesis.HealthCheck.filter_too_much, hypothesis.HealthCheck.too_slow])
def test_nested_einsum_axes_permute(nested_einsum_axes_permute_args: NestedEinsumAxesPermuteArgs):
    circuit, element_index, permutation = nested_einsum_axes_permute_args

    def wrap_test(x: rEinsum):
        out = nested_einsum_axes_permute(x, element_index=element_index, permutation=permutation)
        if out == x:
            raise ImpossibleRewriteError()
        return out

    check_transform_equality(wrap_test, circuit)


def test_nested_einsum_permute_dups_to_eq_manual():
    x = Tag.new_with_random_uuid(Scalar(0.0, (2, 3)))
    y = Tag.new_with_random_uuid(Scalar(0.0, (4, 5, 3)))
    Tag.new_with_random_uuid(Scalar(0.0, (6, 4, 5)))

    x_y = Einsum((x, (0, 1)), (y, (2, 3, 1)), out_axes=(2, 1, 3, 0))
    x_y_other = Einsum((x, (0, 1)), (y, (2, 3, 1)), out_axes=(0, 1, 3, 2))

    mul = Einsum((x_y, (2, 1, 3, 0)), (x_y_other, (7, 5, 6, 2)), out_axes=(3, 2, 6, 7))

    assert len(set(mul.children)) == 2
    assert len(set(nested_einsum_permute_dups_to_eq(mul).children)) == 1


MultiplyAxesByIdentityArgs = Tuple[Circuit, List[int], List[int]]


@st.composite
def st_multiply_axes_by_identity_args(
    draw: st.DrawFn, must_be_explicitly_computable: bool = True
) -> MultiplyAxesByIdentityArgs:
    st_circuit = st_Circuit(
        st_np.array_shapes(min_dims=1),
        must_be_explicitly_computable=must_be_explicitly_computable,
        max_growth_steps=2,
        probs_per_depth=[CP.kw(all=0, leaves=1)],
    )
    circuit = draw(st_circuit)

    all_axes = dedup_with_order(
        draw(st.lists(elements=st.integers(min_value=0, max_value=circuit.ndim - 1), max_size=circuit.ndim - 1))
    )
    batch_axes = [
        i
        for i in dedup_with_order(
            draw(st.lists(elements=st.integers(min_value=0, max_value=circuit.ndim - 1), max_size=circuit.ndim - 1))
        )
        if i not in all_axes
    ]

    return circuit, all_axes, batch_axes


@given(multiply_axes_by_identity_args=st_multiply_axes_by_identity_args())
def test_multiply_axes_by_identity(multiply_axes_by_identity_args: MultiplyAxesByIdentityArgs):
    circuit, axes, batch_axes = multiply_axes_by_identity_args

    check_transform_equality(lambda x: multiply_axes_by_identity(x, axes, batch_axes=batch_axes), circuit)


SplitToConcatForBatchArgs = Tuple[Circuit, int, int]


@st.composite
def st_split_to_concat_for_batch_args(
    draw: st.DrawFn, must_be_explicitly_computable: bool = True
) -> SplitToConcatForBatchArgs:
    st_circuit = st_Circuit(
        st_np.array_shapes(min_dims=1),
        must_be_explicitly_computable=must_be_explicitly_computable,
        probs_per_depth=[CP.kw(all=0, leaves=1)],
    )
    circuit = draw(st_circuit)

    axis = draw(st.integers(0, circuit.ndim - 1))
    extra_mul = 5 if draw(st.booleans()) else 1
    batch_size = draw(st.integers(1, circuit.shape[axis] * extra_mul))
    return circuit, batch_size, axis


@given(split_to_concat_for_batch_args=st_split_to_concat_for_batch_args())
def test_split_to_concat_for_batch(split_to_concat_for_batch_args: SplitToConcatForBatchArgs):
    circuit, batch_size, axis = split_to_concat_for_batch_args
    check_transform_equality(lambda x: split_to_concat_for_batch(x, batch_size=batch_size, axis=axis), circuit)


def test_apply_in_traversal():
    circ = P(
        """
0 Einsum abc->bca
  1 Add
    2 Add
      3 [2,2,2] Scalar 1.0
    """
    )
    trav = new_traversal(start_depth=0, end_depth=3)
    result = apply_in_traversal(circ, trav, simp)
    result.print()
    assert result == P(
        """
0 Rearrange a b c -> b c a
  1 Add
    2 [2, 2, 2] Scalar 1"""
    )
    replace_outside_traversal_symbols(circ, trav)[0].print()
    replace_outside_traversal_symbols(circ, trav, lambda x: "nameyname")[0].print()
    replace_outside_traversal_symbols(circ, trav, lambda x: None)[0].print()
