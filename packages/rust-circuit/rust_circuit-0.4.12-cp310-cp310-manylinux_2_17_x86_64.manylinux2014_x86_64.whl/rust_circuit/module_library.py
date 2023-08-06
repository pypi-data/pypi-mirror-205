from __future__ import annotations

import functools
import json
import math
import random
from copy import copy
from typing import Any, Callable, Dict, List, Literal, Optional, Tuple, TypeVar, Union, cast
from uuid import UUID, uuid4

import cattrs
import torch
from attrs import frozen
from cattrs.preconf.json import make_converter as make_json_converter

import rust_circuit.optional as op

from ._rust import (
    Add,
    Array,
    Circuit,
    Einsum,
    GeneralFunction,
    Matcher,
    MatcherIn,
    Module,
    ModuleArgSpec,
    ModuleSpec,
    Parser,
    PrintOptions,
    Scalar,
    Size,
    Symbol,
    TorchDeviceDtypeOp,
    all_children,
    deep_module_remove_unused_inputs,
    get_free_symbols,
    module_new_bind,
    simp,
)
from .py_utils import I

P = Parser()


# WARNING: Not tested for correctness!

# naming convention: module 'spec_circuit' has name 'x' while children are 'x.y'
# weights are 'x.w.y' ('w' isn't a placeholder). Constants are 'x.c.y'.
# then, callers can do 'z.x' or 'x.call' (or similar)


def to_name_dict(*circs: Circuit, allow_dup: bool = False):
    out = {c.name: c for c in circs}
    assert allow_dup or len(out) == len(circs)
    return out


def add_new_circs(s: str, circs: Dict[str, Circuit], parser: Optional[Parser] = None):
    parser = op.unwrap_or(parser, Parser())
    parser.reference_circuits = {**parser.reference_circuits, **circs}

    return {**circs, **to_name_dict(*parser.parse_circuits(s))}


def make_spec(
    body: Circuit,
    order: List[Circuit] = [],
    exclude: Union[Callable[[Symbol], bool], MatcherIn] = lambda _: False,
):
    exclude_matcher = Matcher(cast(MatcherIn, exclude))
    return ModuleSpec(
        body,
        [
            ModuleArgSpec(x)
            for x in sorted(
                get_free_symbols(body),
                key=lambda c: order.index(c) if c in order else -1,
            )
            if not exclude_matcher(x)
        ],
    )


@frozen
class ModuleLibraryRet:
    circs: Dict[str, Circuit]
    body: Circuit
    spec: ModuleSpec
    name: str

    @classmethod
    def mk(cls, circs: Dict[str, Circuit], name: str) -> ModuleLibraryRet:
        body = circs[name]
        spec = make_spec(body, order=list(circs.values()))
        return cls(circs=circs, body=body, spec=spec, name=name)


def scalar_input(circs: Dict[str, Circuit], to_scalar: str, is_zero_or_one: bool = True):
    return to_name_dict(
        *(
            # we could make this faster if we needed
            deep_module_remove_unused_inputs(
                simp(c.update(to_scalar, lambda x: Scalar(0.0 if is_zero_or_one else 1.0, shape=())))
            ).update(True, lambda x: x.rename(x.name.removesuffix(" rem_unused")))
            for s, c in circs.items()
            if s != to_scalar
        ),
        allow_dup=True,
    )


def zero_input(circs: Dict[str, Circuit], to_zero: str):
    return scalar_input(circs, to_scalar=to_zero, is_zero_or_one=True)


def one_input(circs: Dict[str, Circuit], to_one: str):
    return scalar_input(circs, to_scalar=to_one, is_zero_or_one=False)


layernorm_str = f"""
'ln.y' Einsum h,->h
  'ln.mean_subbed' Add
    'ln.input' [?] Symbol 981b4d2a-711b-4a9d-a11c-d859c311e80c
    'ln.neg_mean' Einsum h,z,->z # z is padding dim for add
      'ln.input'
      'ln.neg' [1] Scalar -1
      'ln.c.recip_hidden_size' GeneralFunction reciprocal
        'ln.c.hidden_size' GeneralFunction last_dim_size
          'ln.input'
  'ln.rsqrt' GeneralFunction rsqrt
    'ln.var_p_eps' Add
      'ln.c.eps' [] Scalar 1e-5
      'ln.var' Einsum h,h,->
        'ln.mean_subbed'
        'ln.mean_subbed'
        'ln.c.recip_hidden_size'

'ln.input'

'ln' Add
  'ln.w.bias' [?] Symbol 621c7792-0177-45ab-87c5-7ff1c3bec487
  'ln.y_scaled' Einsum h,h->h
    'ln.y'
    'ln.w.scale' [?] Symbol 0fa341c3-34b3-4699-847f-08674808b28a

'ln.w.bias'
'ln.w.scale'
"""

layernorm_circs = add_new_circs(layernorm_str, {})
layernorm = ModuleLibraryRet.mk(layernorm_circs, "ln")

batchnorm_str = f"""
'bn.y' Einsum h,h->h
  'bn.mean_subbed' Add
    'bn.input' [?] Symbol cfe0aa25-1214-4d3e-ad53-417fedbb9b7b
    'bn.neg_mean' Einsum h,->h
      'bn.mean' [?] Symbol 217403c9-03b6-4444-8f72-de03b95229d0
      'neg_one' [] Scalar -1
  'bn.rsqrt' GeneralFunction rsqrt
    'bn.var_p_eps' Add
      'bn.c.eps' [] Scalar 1e-5
      'bn.var' [?] Symbol c4e41ca7-e3ab-429e-81b6-25bb14423fb4

'bn.input'
'bn.mean'
'bn.var'

# same as ln above, we could dedudup if we wanted
'bn' Add
  'bn.w.bias' [?] Symbol 3e861c08-9a74-4348-87df-3752a8557aea
  'bn.y_scaled' Einsum h,h->h
    'bn.y'
    'bn.w.scale' [?] Symbol ccbac7e0-c931-422b-9724-1e24ab6e9c63

'bn.w.bias'
'bn.w.scale'
"""

batchnorm_circs = add_new_circs(batchnorm_str, {})
batchnorm = ModuleLibraryRet.mk(batchnorm_circs, "bn")

not_mask_str = """
'not_mask' Add
  'one' [] Scalar 1.
  'not_mask.neg_mask' Einsum ,->
    'not_mask.input' [] Symbol b46f6370-11e1-4535-aabc-94554c234673
    'neg_one' [] Scalar -1.

'neg_one'
'not_mask.input'
"""

not_mask_circs = add_new_circs(not_mask_str, {})
not_mask = ModuleLibraryRet.mk(not_mask_circs, "not_mask")

raw_attention_str = f"""
'a.head' Einsum sV,dV->sd
  'a.comb_v' Einsum qk,kV->qV
    'a.attn_probs' GeneralFunction softmax
      'a.attn_scores' Add
        'a.attn_scores_raw' [?, ?] Einsum qc,kc,,qk->qk
          'a.q_p_bias' [?, ?] Add
            'a.q' Einsum qd,cd->qc
              'a.q.input' [?, ?] Symbol 4f80d1a1-86a4-4e44-94f7-909ec7089061
              'a.w.q_h' [?, ?] Symbol 665efa60-d86c-40d5-92b2-b96d11686a8b
            'a.w.q_bias_h' [?] Symbol 7d531f53-6cce-4bf3-82db-5fe8b2eef974
          'a.k_p_bias' [?, ?] Add
            'a.k' Einsum kd,cd->kc
              'a.k.input' [?, ?] Symbol 664bddee-28ca-47e7-9fb7-9a718de06619
              'a.w.k_h' [?, ?] Symbol 41177709-446d-4588-b9e5-c2bbf59d53a0
            'a.w.k_bias_h' [?] Symbol a891aae4-3c24-4713-afc7-8b954c6fc1b5
          'a.c.div_head_size' GeneralFunction rsqrt
            'a.c.head_size' GeneralFunction last_dim_size
              'a.c.bias_for_head_size' [?] Einsum jk->j # size on this line is just asserted
                'a.w.k_h' [?, ?]
          # mask is true at where positions *are* allowed. (This differs from old pos_mask code)
          'a.mask' [?, ?] Symbol ccfe5bc9-b402-42dd-a5e1-191e6fb7c268
        'a.score_neg_inf_bias' Einsum qk,->qk
          'a.not_mask' Module
            'not_mask'
            'a.mask' ! 'not_mask.input'
          'a.neg_inf' [] Scalar -10_000.0
    'a.v_p_bias' Add
      'a.v' Einsum kd,Vd->kV
        'a.v.input' [?, ?] Symbol 8fd4c632-7f28-49ee-84cc-3dde997e0693
        'a.w.v_h' [?, ?] Symbol 79b6ebff-f9d0-411a-bcdc-530cc13e1524
      'a.w.v_bias_h' [?] Symbol dfb2c4ec-9378-40ee-a360-7d58f2b96954
  'a.w.o_h' [?, ?] Symbol 11a116cb-2168-4725-a06f-1b61a8ca6797

'a.q.input'
'a.k.input'
'a.v.input'
'a.mask'
'a.w.q_h'
'a.w.q_bias_h'
'a.w.k_h'
'a.w.k_bias_h'
'a.w.v_h'
'a.w.v_bias_h'
'a.w.o_h'


'a.head.on_inp' Module
  'a.head'
  'a.qk_input' Add ! 'a.q.input'
    'a.input' [?, ?] Symbol f9eabd07-e2ab-4ed4-8b4a-c9c039d61835
    'a.pos_input' [?, ?] Symbol eab8313e-d910-4174-8dbe-c612954eec34
  'a.qk_input' ! 'a.k.input'
  'a.input' ! 'a.v.input'

'a.input'
'a.pos_input'

'a.p_bias' Add
  'a' Einsum hsd->sd # reduce head dim
    # batch over head
    'a.heads' Module
      'a.head.on_inp'
      'a.w.q' [?, ?, ?] Symbol cf8f9c58-1875-45b0-8007-66b66b8a405a ! 'a.w.q_h'
      'a.w.q_bias' [?, ?] Symbol e896a43e-ba35-43d5-97e7-e189caf3278b ! 'a.w.q_bias_h'
      'a.w.k' [?, ?, ?] Symbol c342f1cd-71e6-4848-86b4-1c3ffdd46753 ! 'a.w.k_h'
      'a.w.k_bias' [?, ?] Symbol 13465b29-c28a-4d55-8a27-22c26cc01c69 ! 'a.w.k_bias_h'
      'a.w.v' [?, ?, ?] Symbol a90db69c-f4ad-47d6-8b76-faa4b107dacd ! 'a.w.v_h'
      'a.w.v_bias' [?, ?] Symbol ea64ee26-2438-4aa9-b777-0ef4f5f70e74 ! 'a.w.v_bias_h'
      'a.w.o' [?, ?, ?] Symbol 24e0e5cf-8b68-4bf2-b198-17237523b237 ! 'a.w.o_h'
  'a.w.o_bias' [?] Symbol 61d54061-63e2-4a5d-9c7a-15c1ecc53b95

'a.w.q'
'a.w.q_bias'
'a.w.k'
'a.w.k_bias'
'a.w.v'
'a.w.v_bias'
'a.w.o'
'a.w.o_bias'


# We split into two pieces so we can apply rotary positional embeddings to only the first.
# Also, we use HALF_ROTARY_DIM to enforce that the rotary dim is even.
'qk_with_rot' [?, ?] Rearrange q s:2 e:2 rh -> q (s:2 e:2 rh)
  'qk_with_rot.cat' [?, 2, 2, ?] Concat 1
    'qk_with_rot.q_rot' Rearrange q e rh -> q 1 e rh
      'qk_rot' [?, 2, ?] GeneralFunction apply_rotary_pos_emb at rust_circuit.generalfuncs.rotary_pos_emb:ApplyRotaryPosEmb
        'qk_rot.inp' Index [:, 0]
          'qk_split' [?, 2, 2, ?] Rearrange q (s:2 e:2 rh) -> q s:2 e:2 rh
            # q or k
            'qk' [?, ?] Symbol 442c7d04-1948-4904-b96a-5c0acf22f19c
    'qk_with_rot.q_pass' Index [:, 1:]
      'qk_split'

# Most of the below is copied from a.head; could factor into a module but backcompat is annoying

'a_rope.head' Einsum sV,dV->sd
  'a_rope.comb_v' Einsum qk,kV->qV
    'a_rope.attn_probs' GeneralFunction softmax
      'a_rope.attn_scores' Add
        'a_rope.attn_scores_raw' Einsum qc,kc,,qk->qk
          'a_rope.q' Module
            'qk_with_rot'
            'a.q_p_bias' ! 'qk'
          'a_rope.k' Module
            'qk_with_rot'
            'a.k_p_bias' ! 'qk'
          'a.c.div_head_size'
          'a.mask'
        'a.score_neg_inf_bias'
    'a.v_p_bias'
  'a.w.o_h'

'a_rope.head.on_inp' Module
  'a_rope.head'
  'a.qk_input' ! 'a.q.input'
  'a.qk_input' ! 'a.k.input'
  'a.input' ! 'a.v.input'

'a_rope.p_bias' Add
  'a_rope' Einsum hsd->sd # reduce head dim
    # batch over head
    'a_rope.heads' Module
      'a_rope.head.on_inp'
      'a.w.q' ! 'a.w.q_h'
      'a.w.q_bias' ! 'a.w.q_bias_h'
      'a.w.k' ! 'a.w.k_h'
      'a.w.k_bias' ! 'a.w.k_bias_h'
      'a.w.v' ! 'a.w.v_h'
      'a.w.v_bias' ! 'a.w.v_bias_h'
      'a.w.o' ! 'a.w.o_h'
  'a.w.o_bias'
"""
raw_attention_circs = add_new_circs(raw_attention_str, not_mask_circs)


def get_attention(bias: bool = False, pos: bool = False, rope: bool = False):
    circs = copy(raw_attention_circs)
    if not bias:
        for weight in ["a.w.q_bias", "a.w.k_bias", "a.w.v_bias", "a.w.o_bias"]:
            circs = zero_input(circs, weight + "_h")
            circs = zero_input(circs, weight)

    if not pos:
        circs = zero_input(circs, "a.pos_input")

    circ = "a"
    if rope:
        circ += "_rope"
    if bias:
        circ += ".p_bias"
    return ModuleLibraryRet.mk(circs, circ)


# we could make faster, but should be free
# Note, this is random utility from some prior code
def random_perm_no_self(
    n: int, device: Union[None, torch.device, str] = None, generator: Optional[torch.Generator] = None
):
    assert n > 1
    x = torch.randperm(n, device=device, generator=generator)
    idxs = (x == torch.arange(x.shape[0], device=device)).nonzero().squeeze(-1)
    if idxs.shape[0] == 0:
        return x
    if idxs.shape[0] == 1:
        idxs = torch.concat([idxs, (idxs + 1) % n])  # any other idx will work

    x[idxs] = x.clone()[torch.roll(idxs, shifts=1)]

    assert not (x == torch.arange(x.shape[0], device=device)).any()

    return x


m_input = Symbol((None,), UUID("13ec4cdc-5f25-4969-870b-0bfa2300187b"), name="m.input")
m_base_circs: Dict[str, Circuit] = {"m.input": m_input}


raw_bilinear_mlp_str = f"""
'm.p_bias' Add
  'm' Einsum h,h,oh->o
    'm.pre0' Index [0,:]
      'm.fold_pre' Rearrange (a:2 b) -> a:2 b
        'm.pre_p_bias' Add
          'm.pre' Einsum i,hi->h
            'm.input'
            'm.w.proj_in' [?, ?] Symbol c171d519-8793-4a8b-ac5e-d550347f30a6
          'm.w.in_bias' [?] Symbol 886b5425-cd19-4db4-871a-c46cb1a23114
    'm.pre1' Index [1,:]
      'm.fold_pre'
    'm.w.proj_out' [?, ?] Symbol e61637eb-9f17-4325-b2c2-5eb2518026cf
  'm.w.out_bias' [?] Symbol 7efddf2e-20af-492c-a94e-1d19468f333f

'm.w.proj_in'
'm.w.in_bias'
'm.w.proj_out'
'm.w.out_bias'
"""

raw_bilinear_mlp_circs = add_new_circs(raw_bilinear_mlp_str, m_base_circs)


@functools.cache
def get_bilinear_mlp(output_bias: bool = False):
    if output_bias:
        circs = raw_bilinear_mlp_circs
    else:
        circs = zero_input(raw_bilinear_mlp_circs, "m.w.out_bias")

    return ModuleLibraryRet.mk(circs, "m.p_bias" if output_bias else "m")


@functools.cache
def get_pointwise_mlp(function_str: str = "gelu", output_bias: bool = False):
    s = f"""
    'm.p_bias' Add
      'm' Einsum h,oh->o
        'm.act' GeneralFunction {function_str}
          'm.pre' Add
            'm.pre_mul' Einsum i,hi->h
              'm.input'
              'm.w.proj_in' [?, ?] Symbol 5217f963-0cdb-460e-bb1f-f82f7fbb3cd9
            'm.w.in_bias' [?] Symbol c870ec00-8c6f-4080-907c-703ea85dde48
        'm.w.proj_out' [?, ?] Symbol fdefa9af-a7d6-4a38-a7ed-5ce816c6efe7
      'm.w.out_bias' [?] Symbol 113c30ba-fa88-4f34-a301-ea7912e03064

    'm.input'
    'm.w.proj_in'
    'm.w.in_bias'
    'm.w.proj_out'
    'm.w.out_bias'
    """
    circs = add_new_circs(s, m_base_circs)
    if not output_bias:
        circs = zero_input(circs, "m.w.out_bias")

    return ModuleLibraryRet.mk(circs, "m.p_bias" if output_bias else "m")


def get_m_topk(samp_count_per_block: int):
    m_topk_str = f"""
    'm_topk.weight_input_p_bias' Add
      'm_topk.weight_input' Einsum bsd,od->bso
        'm_topk.input' [?, ?, ?] Symbol 1de78873-b738-4c05-b41e-8eeab03b0db6
        'm_topk.w.proj_weight' [?, ?] Symbol 7ad722eb-5fd9-4386-8604-14e48c529692
      'm_topk.w.weight_bias' [?] Symbol 77d0791f-cb55-4687-9371-0c84320bc0c0

    'm_topk.weight' Einsum bso,bso->obs
      'm_topk.soft_weight' GeneralFunction softmax
        'm_topk.weight_input_p_bias'
      'm_topk.sig_weight' GeneralFunction sigmoid
        'm_topk.sig_weight_input_p_bias' Add
          'm_topk.sig_weight_input' Einsum bso,o->bso
            'm_topk.weight_input_p_bias'
            'm_topk.w.sig_weight_slope' [?] Symbol 0dcb8f33-da57-40b8-91ef-9a6b9917e2f1
          'm_topk.w.sig_weight_bias' [?] Symbol 742f4ec7-79a7-4004-8bee-252304c59d58

    'm_topk.top_k_items' GeneralFunction top_k_[{samp_count_per_block}]
      'm_topk.weight.flat' Rearrange o b s -> o (b s)
        'm_topk.weight'

    'm_topk.top_k_weights' GeneralFunction sampled_index at rust_circuit.generalfuncs.mlp_topk:SampledIndex
      'm_topk.weight.flat'
      'm_topk.top_k_items'

    'm_topk.output_dirs' Einsum dcv,dc->dcv
      'm_topk.output_dirs_unweighted' Einsum dvp,dcp->dcv
        'm_topk.w.proj_out_inner' [?, ?, ?] Symbol d6382457-2eaf-4f0d-849f-310ee2f17e60
        'm_topk.act_inner' GeneralFunction gelu
          'm_topk.projed_inner' Einsum dpv,dcv->dcp
            'm_topk.w.proj_in_inner' [?, ?, ?] Symbol 4c103dff-c3f3-47d9-8776-652766437872
            'm_topk.input.idxed' GeneralFunction gen_index_at_-2_c
              'm_topk.input.flat' Rearrange b s v -> (b s) v
                'm_topk.input'
              'm_topk.top_k_items'
      'm_topk.top_k_weights'

    'm_topk.raw' GeneralFunction output_scatter at rust_circuit.generalfuncs.mlp_topk:OutputScatter
      'm_topk.output_dirs'
      'm_topk.top_k_items'
      'm_topk.input.summed_v' Einsum b s v, -> b s
        'm_topk.input'
        'm_topk.filler_zero' [] Scalar 0

    # TODO: try scale per group and see if this is better
    # maybe try to fuse some of these adds
    'm_topk' Einsum b s d, -> b s d
      'm_topk.raw'
      'm_topk.w.scale' [] Symbol d980c7a3-afac-4304-b86e-651b29f48ef1


    'm_topk.input'
    'm_topk.w.proj_weight'
    'm_topk.w.weight_bias'
    'm_topk.w.sig_weight_slope'
    'm_topk.w.sig_weight_bias'
    'm_topk.w.proj_in_inner'
    'm_topk.w.proj_out_inner'
    'm_topk.w.scale'
    """

    m_topk_circs = add_new_circs(m_topk_str, not_mask.circs)
    return ModuleLibraryRet.mk(m_topk_circs, "m_topk")


def get_m_topk_sparse(
    samp_count_per_block: int,
    disable_inner_sig: bool = False,
    use_linear_inner: bool = False,
    topk_with_act: bool = False,
    use_weighting_inner: bool = True,
    act_function_str: str = "gelu",
    use_same_weights_for_both: bool = False,
):
    m_topk_str = f"""
    'm_topk.weight_input_p_bias' Add
      'm_topk.weight_input' Einsum bsd,od->bso
        'm_topk.input' [?, ?, ?] Symbol 97aba244-71da-4cd2-8882-d595d46af882
        'm_topk.w.proj_weight' [?, ?] Symbol 64126b31-cc5f-41cd-890e-b56c4904f6b1
      'm_topk.w.weight_bias' [?] Symbol 96269dc6-308a-45c6-a17c-8d82c7410b40

    'm_topk.weight' Einsum bso,bso->obs
      'm_topk.soft_weight' GeneralFunction softmax
        'm_topk.weight_input_p_bias'
      'm_topk.sig_weight' GeneralFunction sigmoid
        'm_topk.sig_weight_input_p_bias' Add
          'm_topk.sig_weight_input' Einsum bso,o->bso
            'm_topk.weight_input_p_bias'
            'm_topk.w.sig_weight_slope' [?] Symbol 74412ead-285d-43db-9d75-a5ff8ed50554
          'm_topk.w.sig_weight_bias' [?] Symbol 46aef4ee-0c5a-4dec-92d2-a10c6c71011c

    'm_topk.top_k_items' GeneralFunction top_k_[{samp_count_per_block}]
      'm_topk.weight.flat' Rearrange o b s -> o (b s)
        'm_topk.weight'

    'm_topk.top_k_weights' GeneralFunction sampled_index at rust_circuit.generalfuncs.mlp_topk:SampledIndex
      'm_topk.weight.flat'
      'm_topk.top_k_items'

    'm_topk.projed_inner' Einsum idpv,dcv->idcp
      'm_topk.w.proj_in_inner' [{'1' if use_same_weights_for_both else '2'}, ?, ?, ?] Symbol 28b5f550-b26d-44c9-85f8-a9c758631737
      'm_topk.input.idxed' GeneralFunction gen_index_at_-2_c
        'm_topk.input.flat' Rearrange b s v -> (b s) v
          'm_topk.input'
        'm_topk.top_k_items'

    'm_topk.inner_weight_input_p_bias' Add
      'm_topk.inner_weight_input' Index [0]
        'm_topk.projed_inner'
      'm_topk.w.inner_weight_bias_unsq' Rearrange d p -> d 1 p
        'm_topk.w.inner_weight_bias' [?, ?] Symbol 16668d6f-fc50-4fec-86b9-1af146676c01

    'm_topk.inner_weight' Einsum dcp,dc->dcp
      'm_topk.inner_new_weight' Einsum dcp,dcp->dcp
        'm_topk.inner_soft_weight' GeneralFunction softmax
          'm_topk.inner_weight_input_p_bias'
        'm_topk.inner_sig_weight' GeneralFunction sigmoid
          'm_topk.inner_sig_weight_input_p_bias' Add
            'm_topk.inner_sig_weight_input' Einsum dcp,dp->dcp
              'm_topk.inner_weight_input_p_bias'
              'm_topk.w.inner_sig_weight_slope' [?, ?] Symbol a346fe9e-7b1e-4a4a-8d02-1d10f7cf997a
            'm_topk.w.inner_sig_weight_bias_unsq' Rearrange d p -> d 1 p
              'm_topk.w.inner_sig_weight_bias' [?, ?] Symbol 444344d4-a4a6-434c-bbd7-5987a6f652f9
      'm_topk.top_k_weights'

    'm_topk.apply_threshold' Einsum dcp,dcp->dcp
      'm_topk.to_threshold' [?, {samp_count_per_block}, ?] Symbol 71096f06-cf30-4db3-8484-1a91e736cac3
      'm_topk.to_threshold_mul' GeneralFunction step
        'm_topk.to_threshold_p_neg_thresh' Add
          'm_topk.to_threshold'
          'm_topk.neg_threshold' Einsum ,->
            'm_topk.threshold' GeneralFunction kth_largest_value at rust_circuit.generalfuncs.mlp_topk:KthLargestValue
              'm_topk.to_threshold.flat' Rearrange d c p -> (d c p)
                'm_topk.to_threshold'
              'm_topk.inner_count' [] Symbol 46efa993-07bd-47d5-8ca1-5e51daba8720
            'neg_one'

    'm_topk.inner_weight_final' Module
      'm_topk.apply_threshold'
      'm_topk.inner_weight' ! 'm_topk.to_threshold'

    'm_topk.weighted_act' Einsum dcp,dcp->dcp
      'm_topk.inner_weight_final'
      'm_topk.act' GeneralFunction {act_function_str}
        'm_topk.linear_act' Index [{'0' if use_same_weights_for_both else '1'}]
          'm_topk.projed_inner'

    'm_topk.weighted_act_no_thresh' Einsum dcp,dcp->dcp
      'm_topk.inner_weight'
      'm_topk.act'

    'm_topk.weighted_act_no_thresh_no_inner_weight' Einsum dc,dcp->dcp
      'm_topk.top_k_weights'
      'm_topk.act'


    'm_topk.weighted_act_final' Module
      'm_topk.apply_threshold'
      'm_topk.weighted_act_no_thresh' ! 'm_topk.to_threshold'

    'm_topk.output_dirs' Einsum dvp,dcp->dcv
      'm_topk.w.proj_out_inner' [?, ?, ?] Symbol 52c23eeb-2869-4ace-bc3e-07c675823d34
      'm_topk.weighted_act'

    'm_topk.raw' GeneralFunction output_scatter at rust_circuit.generalfuncs.mlp_topk:OutputScatter
      'm_topk.output_dirs'
      'm_topk.top_k_items'
      'm_topk.input.summed_v' Einsum b s v, -> b s
        'm_topk.input'
        'm_topk.filler_zero' [] Scalar 0

    # TODO: try scale per group and see if this is better
    # maybe try to fuse some of these adds
    'm_topk' Einsum b s d, -> b s d
      'm_topk.raw'
      'm_topk.w.scale' [] Symbol d980c7a3-afac-4304-b86e-651b29f48ef1


    'm_topk.input'
    'm_topk.w.proj_weight'
    'm_topk.w.weight_bias'
    'm_topk.w.sig_weight_slope'
    'm_topk.w.sig_weight_bias'
    'm_topk.w.inner_weight_bias'
    'm_topk.w.inner_sig_weight_slope'
    'm_topk.w.inner_sig_weight_bias'
    'm_topk.inner_count'
    'm_topk.w.proj_in_inner'
    'm_topk.w.proj_out_inner'
    'm_topk.w.scale'
    """

    if not use_weighting_inner:
        assert use_same_weights_for_both
        assert topk_with_act

    m_topk_circs_orig = add_new_circs(m_topk_str, not_mask.circs)

    new_sym = Symbol.new_with_random_uuid((), "new")
    swapped_circs = {s: c.update("m_topk.filler_zero", lambda _: new_sym) for s, c in m_topk_circs_orig.items()}
    if disable_inner_sig:
        swapped_circs = one_input(swapped_circs, "m_topk.inner_sig_weight")
    if use_linear_inner:
        swapped_circs = {
            s: c.update("m_topk.act", lambda x: x.get_unique("m_topk.linear_act").rename(x.name))
            for s, c in swapped_circs.items()
        }
    if topk_with_act:
        swapped_circs = {
            s: c.update("m_topk.weighted_act", lambda _: swapped_circs["m_topk.weighted_act_final"])
            for s, c in swapped_circs.items()
        }
    if not use_weighting_inner:
        swapped_circs = {
            s: c.update(
                "m_topk.weighted_act_no_thresh",
                lambda _: swapped_circs["m_topk.weighted_act_no_thresh_no_inner_weight"],
            )
            for s, c in swapped_circs.items()
        }
    m_topk_circs = {
        s: c.update(new_sym, lambda _: Scalar(0.0, name="m_topk.filler_zero")) for s, c in swapped_circs.items()
    }

    return ModuleLibraryRet.mk(m_topk_circs, "m_topk")


count_a_topk_proj = 3  # q,k,v
count_a_topk_pos_proj = 2  # q mul, q base, k mul, k base

a_topk_str = f"""
'a_topk.all_projed' Einsum bsd,haod->abhso
  'a_topk.input' [?, ?, ?] Symbol c489c6e2-299e-4a9e-b5e5-29273dd337df
  'a_topk.w.proj_in' ["head":?, {count_a_topk_proj}, ?, ?] Symbol a5224b72-2dc5-4751-ad96-315037322c18

'a_topk.all_pos_projed' Einsum sd,haod->ahso
  'a_topk.pos_input' [?, ?] Symbol d2becb85-2009-4dee-a720-f04380864a76
  'a_topk.w.pos_proj_in' ["head":?, {count_a_topk_pos_proj}, ?, ?] Symbol 19c5e06f-0f75-4656-943f-20c79d0a79ea

'a_topk.raw_scores' Einsum qc,kc,->qk
  'a_topk.q_inner' [?, ?] Symbol 0491b7b4-1d2d-4220-9545-df22430346b1
  'a_topk.k_inner' [?, ?] Symbol d2d439b4-6164-4f7f-80ea-00f4d2d45f1c
  'a_topk.c.div_head_size' GeneralFunction rsqrt
    'a_topk.c.head_size' GeneralFunction last_dim_size
      'a_topk.q_inner_sum' Einsum s d -> d
        'a_topk.q_inner'

'a_topk.inner_scores_raw' Module
  'a_topk.raw_scores'
  'a_topk.q' Index [0] ! 'a_topk.q_inner'
    'a_topk.all_projed'
  'a_topk.k' Index [1] ! 'a_topk.k_inner'
    'a_topk.all_projed'

'a_topk.pos_scores_raw' Module
  'a_topk.raw_scores'
  'a_topk.pos_q' Index [0] ! 'a_topk.q_inner'
    'a_topk.all_pos_projed'
  'a_topk.pos_k' Index [1] ! 'a_topk.k_inner'
    'a_topk.all_pos_projed'

'a_topk.inner_act_pre_thresh' Einsum bhqk,bqk->hbqk
  'a_topk.inner_act_raw' GeneralFunction relu
    'a_topk.inner_scores_raw'
  'a_topk.mask' [?, ?, ?] Symbol 122965a0-5226-4796-ab93-dd37cc0e1159

'a_topk.inner_act' Einsum hbqk,hbqk->bhqk
  'a_topk.inner_act_pre_thresh'
  'a_topk.to_threshold_mul' GeneralFunction step
    'a_topk.to_threshold_p_neg_thresh' Add
      'a_topk.inner_act_pre_thresh'
      'a_topk.neg_threshold_unsq' Rearrange h -> h 1 1 1
        'a_topk.neg_threshold' Einsum h,->h
          'a_topk.threshold' GeneralFunction kth_largest_value at rust_circuit.generalfuncs.mlp_topk:KthLargestValue
            'm_topk.inner_act_pre_thresh.flat' Rearrange h b q k -> h (b q k)
              'a_topk.inner_act_pre_thresh'
            'a_topk.inner_count' [] Symbol cc50bdf4-74ad-46f9-9264-86580b7aa27a
          'neg_one'

'a_topk.attn_scores' Add
  'a_topk.attn_scores_masked' Einsum bhqk,bqk->hbqk
    'a_topk.attn_scores_raw' Add
      'a_topk.inner_act'
      'a_topk.pos_scores_raw'
    'a_topk.mask'
  'a_topk.score_neg_inf_bias' Einsum bqk,->bqk
    'a_topk.not_mask' Module
      'not_mask'
      'a_topk.mask' ! 'not_mask.input'
    'a_topk.neg_inf' [] Scalar -10_000.0

'a_topk.v' Index [2]
  'a_topk.all_projed'

'a_topk' Einsum bhsV,hdV->bsd
  'a_topk.comb_v' Einsum hbqk,bhkV->bhqV
    'a_topk.attn_probs' GeneralFunction softmax
      'a_topk.attn_scores'
    'a_topk.v'
  'a_topk.w.o' [?, ?, ?] Symbol 8b71cfce-80be-4a1a-91ba-7039853a3241

'a_topk.input'
'a_topk.pos_input'
'a_topk.mask'
'a_topk.inner_count'
'a_topk.w.proj_in'
'a_topk.w.pos_proj_in'
'a_topk.w.o'
"""

a_topk_circs = add_new_circs(a_topk_str, not_mask.circs)
a_topk = ModuleLibraryRet.mk(a_topk_circs, "a_topk")

count_a_sep_proj = 3  # q,k,v
count_a_sep_pos_proj = 2  # q mul, q base, k mul, k base

a_sep_str = f"""
'a_sep.all_projed' Einsum sd,aod->aso
  'a_sep.input' [?, ?] Symbol 6d294966-c1f8-40e6-91eb-989d876a1da5
  'a_sep.w.proj_in_h' [{count_a_sep_proj}, ?, ?] Symbol 1c682d8a-d1a9-4127-a63a-98ffc4fe8943

'a_sep.all_pos_projed' Einsum sd,aod->aso
  'a_sep.pos_input' [?, ?] Symbol 2149f2e1-d638-4a27-8405-dc0debe03a1e
  'a_sep.w.pos_proj_in_h' [{count_a_sep_pos_proj}, ?, ?] Symbol aa3dfdd3-30cf-4f71-8ab0-dfb85609bffc

'a_sep.raw_scores' Einsum qc,kc,->qk
  'a_sep.q_inner' [?, ?] Symbol bb9d97df-a65e-49cf-8f45-1cc1e7235c7a
  'a_sep.k_inner' [?, ?] Symbol 7d5975ab-97bb-40b1-a023-95419087f5a6
  'a_sep.c.div_head_size' GeneralFunction rsqrt
    'a_sep.c.head_size' GeneralFunction last_dim_size
      'a_sep.q_inner_sum' Einsum s d -> d
        'a_sep.q_inner'

'a_sep.inner_scores_raw' Module
  'a_sep.raw_scores'
  'a_sep.q' Index [0] ! 'a_sep.q_inner'
    'a_sep.all_projed'
  'a_sep.k' Index [1] ! 'a_sep.k_inner'
    'a_sep.all_projed'

'a_sep.pos_scores_raw' Module
  'a_sep.raw_scores'
  'a_sep.pos_q' Index [0] ! 'a_sep.q_inner'
    'a_sep.all_pos_projed'
  'a_sep.pos_k' Index [1] ! 'a_sep.k_inner'
    'a_sep.all_pos_projed'

'a_sep.attn_scores' Add
  'a_sep.attn_scores_masked' Einsum qk,qk->qk
    'a_sep.attn_scores_raw' Add
      'a_sep.inner_scores_raw'
      'a_sep.pos_scores_raw'
    'a.mask' [?, ?] Symbol 7e55489b-1653-413b-95fd-2dca863c7cdd
  'a_sep.score_neg_inf_bias' Einsum qk,->qk
    'a_sep.not_mask' Module
      'not_mask'
      'a.mask' ! 'not_mask.input'
    'a_sep.neg_inf' [] Scalar -10_000.0

'a_sep.v' Index [2]
  'a_sep.all_projed'

'a_sep.head' Einsum sV,dV->sd
  'a_sep.comb_v' Einsum qk,kV->qV
    'a_sep.attn_probs' GeneralFunction softmax
      'a_sep.attn_scores'
    'a_sep.v'
  'a_sep.w.o_h' [?, ?] Symbol b55f8650-61e9-4f32-ac72-34dee3ed385f

'a_sep' Einsum hsd->sd # reduce head dim
  'a_sep.heads' Module
    'a_sep.head'
    'a_sep.w.proj_in' [?, {count_a_sep_proj}, ?, ?] Symbol 302ec171-11ca-4be7-8842-e2755b843e90 ! 'a_sep.w.proj_in_h'
    'a_sep.w.pos_proj_in' [?, {count_a_sep_pos_proj}, ?, ?] Symbol a1f957c7-ae4e-4888-b221-6a2c1b69e035 ! 'a_sep.w.pos_proj_in_h'
    'a_sep.w.o' [?, ?, ?] Symbol 8c3ab566-dcd6-4f29-b7c6-e8e6f7b057c5 ! 'a_sep.w.o_h'


'a_sep.input'
'a_sep.pos_input'
'a.mask'
'a_sep.w.proj_in'
'a_sep.w.pos_proj_in'
'a_sep.w.o'
"""

a_sep_circs = add_new_circs(a_sep_str, not_mask.circs)
a_sep = ModuleLibraryRet.mk(a_sep_circs, "a_sep")

sparse_indexed_mlp_common_settings_names = [
    "thresh",
    "penalty_scale",
    "penalty_log_mul",
    "penalty_negative_max",
    "noise_penalty_mul",
    "scale_exponential_by_val",
    "balancing_weight",
    "balancing_min_frac_activ",
    "balancing_min_clamp",
    "balancing_max_clamp",
    "balancing_biased_ema_frac_activ",
    "balancing_ema_beta",
    "penalty_weight",
]


def get_sparse_indexed_mlp(count_weights: int, interp_mode: bool = False):
    s = f"""
    'm_i' GeneralFunction sparse_indexed_mlp at interp.circuit.projects.train_update.sparse_indexed_mlp_rust_circuit:SparseIndexedMLP{'Interp' if interp_mode else ''}
      'm_i.key' [] Symbol e565b3e9-1502-4b76-a613-4957ce58455a
      'm_i.input' [?] Symbol 81c88d2a-866a-4519-98bc-dae443c89b15
      'm_i.w.proj_in' [?, ?, ?] Symbol 448da89a-0bce-48f2-ae24-7f3dbbe2e199
      'm_i.w.proj_out' [?, ?, ?] Symbol d0267677-66d1-4fc0-95f2-3e5ac4efea31
      'm_i.w.scale' [] Symbol c23b0483-1852-4902-be57-7b136ad86032
      'm_i.ema_iters' [] Symbol 82f12001-d048-441e-9ead-a679e7474999
    """
    rd = random.Random()
    rd.seed(2384728)

    def get_uuid():
        return UUID(int=rd.getrandbits(128)).hex

    def get_common_settings_str(p: str):
        prefix = """
        """
        prefix = prefix[1:][:-2]
        out = "\n" + "\n".join(
            f"{prefix}'{p}.{suff}' [{f'{180+i}s' if suff == 'balancing_biased_ema_frac_activ' else ''}] Symbol {get_uuid()}"
            for suff in sparse_indexed_mlp_common_settings_names
        )
        return out

    for i in range(count_weights):
        p = f"m_i.weight{i}"
        s += f"""
      '{p}.w.proj' [{100+i}s, 2, {120+i}s, ?] Symbol {get_uuid()}
      """
        s += get_common_settings_str(p)
        s += f"""
      '{p}.topk_limit_frac' [] Symbol {get_uuid()}
      '{p}.padding_multiplier' [] Symbol {get_uuid()}
        """
    s += f"""
      'm_i.act_block.count' [] Symbol cf700ad8-c2d5-4ab5-b66f-7c188b5b66c3
      'm_i.act_block.size' [] Symbol 50d7b817-44b9-43f3-8d2f-adf09b6dfc0d
    """
    for item in ["act_block", "neuron"]:
        p = f"m_i.{item}"
        s += get_common_settings_str(p)

    if interp_mode:
        assert count_weights == 2
        s += f"""
      'm_i.weight0.mask' [141s] Symbol 75a19d77-04c7-454d-913a-0d96bc81a831
      'm_i.weight1.mask' [142s] Symbol f4a41388-ea8c-4d9d-ab5d-ba1ae685a45f
      'm_i.act_block.mask' [143s] Symbol a41eaf17-7c89-456d-9278-6602e97b026b
      'm_i.neuron.mask' [144s] Symbol 83464098-f52d-4ffa-a566-a278442a1eb2
        """

    print(s)
    sparse_idxed_circs = add_new_circs(s, {})
    sparse_idxed_circs = to_name_dict(*{c for cs in [all_children(c) for c in sparse_idxed_circs.values()] for c in cs})
    return ModuleLibraryRet.mk(sparse_idxed_circs, "m_i")


def get_norm_bind(
    prefix: str,
    uuids: List[UUID],
    norm_type: Literal["ln", "bn"],
    has_batch_seq: bool = False,
):
    uuids = copy(uuids)
    p = prefix
    nt = norm_type
    bind_str = f"""
    '{p}.norm' Module
      '{nt}'
      '{p}.norm.input' [{"?, " if has_batch_seq else ""}?, ?] Symbol {uuids.pop(4)} ! '{nt}.input'"""

    if norm_type == "bn":
        bind_str += f"""
      '{p}.{nt}.mean' [?] Symbol {uuids.pop(3)} ! '{nt}.mean'
      '{p}.{nt}.var' [?] Symbol {uuids.pop(2)} ! '{nt}.var'"""

    bind_str += f"""
      '{p}.{nt}.w.bias' [?] Symbol {uuids.pop(1)} ! '{nt}.w.bias'
      '{p}.{nt}.w.scale' [?] Symbol {uuids.pop(0)} ! '{nt}.w.scale'

    '{p}.norm.input'"""

    if norm_type == "bn":
        bind_str += f"""
    '{p}.{nt}.mean'
    '{p}.{nt}.var'"""

    bind_str += f"""
    '{p}.{nt}.w.bias'
    '{p}.{nt}.w.scale'
    """
    circs = add_new_circs(bind_str, layernorm_circs if norm_type == "ln" else batchnorm_circs)
    return ModuleLibraryRet.mk(circs, f"{p}.norm")


def print_uuid_list_repr(n: int):
    """utility for writing this code"""
    print("[")
    for _ in range(n):
        print(repr(uuid4()) + ",")
    print("]")


m_norm_uuids = [
    UUID("fe330d51-0164-4b49-a504-81769d550bb1"),
    UUID("771e2d50-3414-459e-87ff-879f83d4a15c"),
    UUID("bf7ea689-c481-4ad4-89d0-0a59cd476739"),
    UUID("cf2adbd9-b04f-42af-86d7-cc5c8890607b"),
    UUID("f63f8838-9d69-4da2-a902-8eaf325f07a7"),
]
a_norm_uuids = [
    UUID("c564149d-e226-4e3d-8e47-7d6e2ceea99e"),
    UUID("2c737289-2702-404c-a22e-ad37c2652620"),
    UUID("33774cb3-f047-4a1e-ac0c-e6f8c93d2bb2"),
    UUID("981982a3-253b-4c0d-8789-c0bc9dcd229b"),
    UUID("6a622698-fd68-4d25-aeee-e8d38e68049e"),
]
final_norm_uuids = [
    UUID("2110aef7-70d5-4f77-a929-044e40c31cbd"),
    UUID("10652dc2-e9a8-4f1e-8bad-99d46804c7b3"),
    UUID("6cfcb4e6-7081-4d2d-bef9-1e9db52d4444"),
    UUID("94e8bc7f-1689-429f-bfec-67d33965aef5"),
    UUID("0851aebd-0d39-4f65-89f9-8a8afaed631a"),
]

m_ln_bind = get_norm_bind("m", m_norm_uuids, "ln")
a_ln_bind = get_norm_bind("a", a_norm_uuids, "ln")
ng_m_ln_bind = get_norm_bind("m", m_norm_uuids, "ln", has_batch_seq=True)
ng_a_ln_bind = get_norm_bind("a", a_norm_uuids, "ln", has_batch_seq=True)
a_topk_ln_bind = get_norm_bind("a", a_norm_uuids, "ln", has_batch_seq=True)
m_topk_ln_bind = get_norm_bind("m", m_norm_uuids, "ln", has_batch_seq=True)
p_ln_bind = get_norm_bind("p", a_norm_uuids, "ln")
m_bn_bind = get_norm_bind("m", m_norm_uuids, "bn")
a_bn_bind = get_norm_bind("a", a_norm_uuids, "bn")
ng_m_bn_bind = get_norm_bind("m", m_norm_uuids, "bn", has_batch_seq=True)
ng_a_bn_bind = get_norm_bind("a", a_norm_uuids, "bn", has_batch_seq=True)
a_topk_bn_bind = get_norm_bind("a", a_norm_uuids, "bn", has_batch_seq=True)
m_topk_bn_bind = get_norm_bind("m", m_norm_uuids, "bn", has_batch_seq=True)
p_bn_bind = get_norm_bind("p", a_norm_uuids, "bn")
final_ln_bind = get_norm_bind("final", final_norm_uuids, "ln")
final_bn_bind = get_norm_bind("final", final_norm_uuids, "bn")


# TODO: should this be a module?
def get_norm_call(
    prefix: str,
    circs: Dict[str, Circuit],
    mod: Optional[str] = None,
    input_use_mod: bool = False,
):
    norm_call_str = f"""
    '{prefix}.norm_call' Module
      '{op.unwrap(mod, prefix)}'
      '{prefix}.norm' ! '{op.unwrap(mod) if input_use_mod else prefix}.input'
    """

    circs = add_new_circs(norm_call_str, circs)
    return ModuleLibraryRet.mk(circs, f"{prefix}.norm_call")


b_input = Symbol((None, None), UUID("5837c4fd-f5ac-4bff-8456-abf3e95bcf36"), name="b.input")


def rename_circs_to_keys(d: Dict[str, Circuit], rename_suffix: str = ""):
    return {s: c.rename(s + rename_suffix) for s, c in d.items()}


T = TypeVar("T")


def apply_prefix(d: Dict[str, T], prefix: str) -> Dict[str, T]:
    return {f"{prefix}.{s}": c for s, c in d.items()}


def add_number(name: str, num: int):
    before, _, after = name.partition(".")
    return f"{before}{num}.{after}"


def dtype_or_default(x: Optional[torch.dtype]):
    return op.unwrap_or(x, torch.get_default_dtype())


def init_weight(w: torch.Tensor, dims: list[int] = [-1], extra_scale: float = 1.0):
    size = math.prod(w.shape[i] for i in dims)
    # print(size)
    bound = 1 / math.sqrt(size)
    torch.nn.init.uniform_(w, a=-bound * extra_scale, b=bound * extra_scale)


def basic_linear_array(
    *size: int,
    dims: list[int] = [-1],
    device_dtype: TorchDeviceDtypeOp = TorchDeviceDtypeOp(),
    extra_scale: float = 1.0,
):
    out = torch.empty(
        *size,
        device=device_dtype.device,
        dtype=dtype_or_default(device_dtype.get_torch_dtype()),
    )
    init_weight(out, dims, extra_scale=extra_scale)
    return Array(out)


def full_array(
    *size: int,
    fill: float,
    device_dtype: TorchDeviceDtypeOp = TorchDeviceDtypeOp(),
    garbage: bool = False,
):
    if garbage:
        return Array.randn(*size, device_dtype=device_dtype)

    return Array(
        torch.full(
            (*size,),
            fill,
            device=device_dtype.device,
            dtype=dtype_or_default(device_dtype.get_torch_dtype()),
        )
    )


MlpActType = Literal["gelu", "gelu_new", "relu", "bilinear"]
SoftmaxType = Literal["softmax"]
PosEncType = Literal["gpt", "shortformer", "none"]


@frozen
class TransformerBlockParams:
    norm_type: Optional[Literal["ln", "bn"]] = "ln"
    attn_bias: bool = False
    attn_pos: bool = False
    use_mlp: bool = True
    mlp_act_type: MlpActType = "gelu"
    mlp_output_bias: bool = False
    use_parallel_residual: bool = False  # currently implies only one shared norm
    use_rope: bool = False
    use_m_topk: bool = False
    use_m_topk_sparse: bool = False
    m_topk_samp_count_per_neuron_block: Optional[int] = None
    m_topk_sparse_disable_inner_sig: bool = False
    m_topk_sparse_use_linear_inner: bool = False
    m_topk_sparse_topk_with_act: bool = False
    m_topk_sparse_use_weighting_inner: bool = True
    m_topk_sparse_act_function_str: str = "gelu"
    m_topk_sparse_use_same_weights_for_both: bool = False
    use_a_topk: bool = False
    use_a_sep: bool = False
    use_sparse_indexed_mlp: bool = False
    sparse_indexed_mlp_weight_count: int = 2
    sparse_indexed_mlp_interp_mode: bool = False

    @property
    def batch_size(self):
        # TODO: inference modes?
        if self.use_m_topk or self.use_m_topk_sparse:
            return Size.NONE
        elif self.use_a_topk:
            assert self.use_m_topk or self.use_m_topk_sparse, "todo, fix me as needed"
            return Size.NONE
        return None

    @functools.cache
    def get(self):
        if self.use_m_topk or self.use_m_topk_sparse:
            assert not self.use_sparse_indexed_mlp
            assert not (self.use_m_topk and self.use_m_topk_sparse), "just one"
            assert self.mlp_act_type == "gelu"
            assert not self.mlp_output_bias
            assert not self.use_parallel_residual, "unsupported"
        elif self.use_sparse_indexed_mlp:
            assert self.mlp_act_type == "gelu"
            assert not self.mlp_output_bias

        # order for circs matters
        circs: Dict[str, Circuit] = {}

        mlp = None
        mlp_with_norm = None
        if self.use_mlp:
            if self.use_m_topk:
                mlp = get_m_topk(
                    op.unwrap(self.m_topk_samp_count_per_neuron_block),
                )
            elif self.use_m_topk_sparse:
                mlp = get_m_topk_sparse(
                    samp_count_per_block=op.unwrap(self.m_topk_samp_count_per_neuron_block),
                    disable_inner_sig=self.m_topk_sparse_disable_inner_sig,
                    use_linear_inner=self.m_topk_sparse_use_linear_inner,
                    topk_with_act=self.m_topk_sparse_topk_with_act,
                    use_weighting_inner=self.m_topk_sparse_use_weighting_inner,
                    act_function_str=self.m_topk_sparse_act_function_str,
                    use_same_weights_for_both=self.m_topk_sparse_use_same_weights_for_both,
                )
            elif self.use_sparse_indexed_mlp:
                mlp = get_sparse_indexed_mlp(
                    self.sparse_indexed_mlp_weight_count, interp_mode=self.sparse_indexed_mlp_interp_mode
                )
            elif self.mlp_act_type == "bilinear":
                mlp = get_bilinear_mlp(output_bias=self.mlp_output_bias)
            else:
                mlp = get_pointwise_mlp(function_str=self.mlp_act_type, output_bias=self.mlp_output_bias)

            circs = {**circs, **mlp.circs}

            if self.norm_type is not None:
                if self.use_m_topk or self.use_m_topk_sparse:
                    bind = m_topk_ln_bind if self.norm_type == "ln" else m_topk_bn_bind
                else:
                    bind = m_ln_bind if self.norm_type == "ln" else m_bn_bind
                circs = {**circs, **bind.circs}
                mlp_with_norm = get_norm_call(
                    "m",
                    circs,
                    mod=mlp.name,
                    input_use_mod=self.use_m_topk or self.use_m_topk_sparse or self.use_sparse_indexed_mlp,
                )
                circs = mlp_with_norm.circs
            else:
                mlp_with_norm = mlp

        if self.use_parallel_residual:
            circs = {
                **circs,
                **(p_ln_bind if self.norm_type == "ln" else p_bn_bind).circs,
            }

        if self.use_a_topk:
            attn = a_topk
        elif self.use_a_sep:
            attn = a_sep
        else:
            attn = get_attention(bias=self.attn_bias, pos=self.attn_pos)

        circs = {**circs, **attn.circs}

        if self.norm_type is not None:
            if self.use_a_topk:
                bind = a_topk_ln_bind if self.norm_type == "ln" else a_topk_bn_bind
            else:
                bind = a_ln_bind if self.norm_type == "ln" else a_bn_bind
            circs = {**circs, **bind.circs}
            attn_with_norm = get_norm_call("a", circs, mod=attn.name, input_use_mod=self.use_a_topk or self.use_a_sep)
            circs = attn_with_norm.circs
        else:
            attn_with_norm = attn

        this_b_input = Symbol(
            tuple(op.it(self.batch_size)) + (None, None),
            UUID("635b85b1-ee24-4717-b152-90f6471c3f91"),
            name="b.input",
        )

        circs = {**circs, "b.input": this_b_input}

        if (self.use_m_topk or self.use_m_topk_sparse) and not self.use_a_topk:
            this_b_a_mask = Symbol(
                tuple(op.it(self.batch_size)) + (None, None),
                UUID("dcb8b0e4-b629-477f-90c1-87db245418cb"),
                name="b.a.mask",
            )
            circs = {**circs, "b.a.mask": this_b_a_mask}

        attn_only_str = f"""
        'b.resid.a' Add
          'b.a' Module
            '{attn_with_norm.name}'
            'b.input' ! 'a{'.norm' if self.norm_type is not None else ''}.input'
            {"'b.a.mask' ! 'a.mask'" if (self.use_m_topk or self.use_m_topk_sparse) and not self.use_a_topk else ""}
          'b.input'

        'b.input'
        """

        cur_resid_name = "b.resid.a"

        circs = add_new_circs(attn_only_str, circs)

        if self.use_parallel_residual:
            assert self.use_mlp and self.norm_type is not None
            assert mlp is not None
            block_str = f"""
          'b.add' Add
            'b.a' Module
              '{attn.name}'
              'p.input' [?, ?] Symbol e76c1fd7-a230-4295-9199-17dc8dad79d0 ! 'a.input'
            'b.m' Module
              '{mlp.name}'
              'p.input' ! 'm.input'

          'p.input'
          """
            circs = add_new_circs(block_str, circs)
            circs = get_norm_call("p", circs, mod="b.add").circs
            block_str = """
          'b.resid.p' Add
            'b.p' Module
              'p.norm_call'
              'b.input' ! 'p.norm.input'
            'b.input'
          """
            circs = add_new_circs(block_str, circs)
            cur_resid_name = "b.resid.p"
        elif self.use_mlp:
            assert mlp_with_norm is not None

            mlp_input = cur_resid_name

            m_input_sym = f"m{'.norm' if self.norm_type is not None else ''}.input"

            m_input_line = f"'{mlp_input}' ! '{m_input_sym}'"

            block_str = f"""
            'b.resid.m' Add
              'b.m' Module
                '{mlp_with_norm.name}'
                {m_input_line}
              '{cur_resid_name}'
            """

            cur_resid_name = "b.resid.m"

            circs = add_new_circs(block_str, circs)

        circs["b"] = circs[cur_resid_name].rename("b")

        return ModuleLibraryRet.mk(circs, "b")

    def get_non_weighty_inputs(self):
        non_weighty_inputs = {
            "b.input",
            "a.pos_input",
            "a.mask",
            "b.a.mask",
            "ng_a.pos_input",
            "ng_a.mask",
            "ng_a.shuffle",
            "ng_a.half_x_val",
            "ng_a.tenth_x_val",
            "ng_a.full_noise_x_val",
            "ng_a.linear_penalty_mul",
            "ng_m.shuffle",  # TODO: this should maybe be the same shuffle as for a!
            "ng_m.half_x_val",
            "ng_m.tenth_x_val",
            "ng_m.full_noise_x_val",
            "ng_m.linear_penalty_mul",
            "m_topk.inner_count",
            "a_topk.pos_input",
            "a_topk.mask",
            "a_topk.inner_count",
            "a_sep.pos_input",
            "m_i.act_block.count",
            "m_i.act_block.size",
            "m_i.ema_iters",
        }
        for i in range(self.sparse_indexed_mlp_weight_count):
            p = f"m_i.weight{i}"
            non_weighty_inputs.update(
                {
                    f"{p}.{suff}"
                    for suff in sparse_indexed_mlp_common_settings_names
                    if suff != "balancing_biased_ema_frac_activ"
                }
            )
            non_weighty_inputs.update({f"{p}.topk_limit_frac", f"{p}.padding_multiplier"})
        for item in ["act_block", "neuron"]:
            p = f"m_i.{item}"
            non_weighty_inputs.update(
                {
                    f"{p}.{suff}"
                    for suff in sparse_indexed_mlp_common_settings_names
                    if suff != "balancing_biased_ema_frac_activ"
                }
            )

        non_weighty_inputs.update({s.partition(".")[0] + "_s." + s.partition(".")[2] for s in non_weighty_inputs})

        return non_weighty_inputs

    # add function for rebinding inputs also as needed
    @functools.cache
    def get_rebound_weighty(self, num: int):
        gotten = self.get()

        rd = random.Random()
        rd.seed(num)

        # weighty == different for each layer
        non_weighty_inputs = self.get_non_weighty_inputs()

        circs = copy(gotten.circs)
        spec = make_spec(gotten.body, order=list(gotten.circs.values()), exclude=non_weighty_inputs)

        binds = [
            Symbol(
                arg_spec.symbol.shape,
                UUID(int=rd.getrandbits(128)),
                add_number(arg_spec.symbol.name, num),
            )
            for arg_spec in spec.arg_specs
        ]

        bound = Module.new_flat(spec, *binds, name=f"b{num}")

        assert bound.name not in circs
        circs[bound.name] = bound
        circs = {**circs, **to_name_dict(*binds)}

        return ModuleLibraryRet.mk(circs, bound.name)

    def init_norm_weights(
        self,
        hidden_size: int,
        device_dtype: TorchDeviceDtypeOp = TorchDeviceDtypeOp(),
        garbage: bool = False,
    ):
        """
        if you pass 'garbage=True', then this will initialize non-params
        like bn mean to garbage and ensure all weights are stochastic
        """

        weights: Dict[str, Circuit] = {}
        if self.norm_type is not None:
            if self.norm_type == "bn" and garbage:
                weights.update(
                    {
                        f"{self.norm_type}.mean": Array.randn(hidden_size, device_dtype=device_dtype),
                        f"{self.norm_type}.var": Array(torch.randn(hidden_size).to(device=device_dtype.device) ** 2),
                    }
                )

            weights.update(
                {
                    f"{self.norm_type}.w.bias": full_array(
                        hidden_size,
                        fill=0.0,
                        device_dtype=device_dtype,
                        garbage=garbage,
                    ),
                    f"{self.norm_type}.w.scale": full_array(
                        hidden_size,
                        fill=1.0,
                        device_dtype=device_dtype,
                        garbage=garbage,
                    ),
                }
            )

        return rename_circs_to_keys(weights, rename_suffix="_arr")

    def init_weights(
        self,
        hidden_size: int,
        head_size: int,
        num_heads: int,
        device_dtype: TorchDeviceDtypeOp = TorchDeviceDtypeOp(),
        garbage: bool = False,
        force_num_neurons: Optional[int] = None,
        pos_head_size: Optional[int] = None,
        pos_hidden_size: Optional[int] = None,
        proj_in_proj_out_scale: float = 1.0,
        sig_weight_bias_init: float = 3.0,
        sig_weight_slope_init: float = 0.0,
        m_topk_weight_scale: float = 1.0,
        m_topk_initial_scale: float = 1.0,
        m_topk_block_count: Optional[int] = None,
        m_topk_neurons_per_block: Optional[int] = None,
        m_topk_sparse_inner_weight_scale: float = 1.0,
        sparse_indexed_mlp_softmax_weight_scales: list[float] = [1.0, 1.0],
        sparse_indexed_mlp_sig_weight_scales: list[float] = [1.0, 1.0],
        sparse_indexed_mlp_initial_scale: float = 1.0,
        sparse_indexed_mlp_block_multiplicative_counts: Optional[list[int]] = None,
        sparse_indexed_mlp_neurons_per_block: Optional[int] = None,
        sparse_indexed_mlp_neurons_per_block_out: Optional[int] = None,
    ):
        """
        if you pass 'garbage=True', then this will initialize non-params
        like bn mean to garbage and ensure all weights are stochastic
        """
        weights: Dict[str, Circuit] = {}
        weights.update(
            apply_prefix(
                self.init_norm_weights(hidden_size=hidden_size, device_dtype=device_dtype, garbage=garbage),
                "a",
            )
        )

        if self.use_a_topk:
            assert pos_head_size is not None
            assert pos_hidden_size is not None
            weights.update(
                {
                    "a_topk.w.proj_in": basic_linear_array(
                        num_heads,
                        count_a_topk_proj,
                        head_size,
                        hidden_size,
                        device_dtype=device_dtype,
                        extra_scale=proj_in_proj_out_scale,
                    ),
                    "a_topk.w.pos_proj_in": basic_linear_array(
                        num_heads,
                        count_a_topk_pos_proj,
                        pos_head_size,
                        pos_hidden_size,
                        device_dtype=device_dtype,
                    ),
                    "a_topk.w.o": basic_linear_array(
                        num_heads,
                        hidden_size,
                        head_size,
                        device_dtype=device_dtype,
                        extra_scale=proj_in_proj_out_scale,
                    ),
                }
            )
        elif self.use_a_sep:
            assert pos_head_size is not None
            assert pos_hidden_size is not None
            weights.update(
                {
                    "a_sep.w.proj_in": basic_linear_array(
                        num_heads,
                        count_a_sep_proj,
                        head_size,
                        hidden_size,
                        device_dtype=device_dtype,
                        extra_scale=proj_in_proj_out_scale,
                    ),
                    "a_sep.w.pos_proj_in": basic_linear_array(
                        num_heads,
                        count_a_sep_pos_proj,
                        pos_head_size,
                        pos_hidden_size,
                        device_dtype=device_dtype,
                    ),
                    "a_sep.w.o": basic_linear_array(
                        num_heads,
                        hidden_size,
                        head_size,
                        device_dtype=device_dtype,
                        extra_scale=proj_in_proj_out_scale,
                    ),
                }
            )
        else:
            weights.update(
                {
                    "a.w.q": basic_linear_array(num_heads, head_size, hidden_size, device_dtype=device_dtype),
                    "a.w.k": basic_linear_array(num_heads, head_size, hidden_size, device_dtype=device_dtype),
                    "a.w.v": basic_linear_array(num_heads, head_size, hidden_size, device_dtype=device_dtype),
                    "a.w.o": basic_linear_array(num_heads, hidden_size, head_size, device_dtype=device_dtype),
                }
            )

        if self.attn_bias:
            assert not self.use_a_topk
            assert not self.use_a_sep
            weights.update(
                {
                    "a.w.q_bias": full_array(
                        num_heads,
                        head_size,
                        fill=0.0,
                        device_dtype=device_dtype,
                        garbage=garbage,
                    ),
                    "a.w.k_bias": full_array(
                        num_heads,
                        head_size,
                        fill=0.0,
                        device_dtype=device_dtype,
                        garbage=garbage,
                    ),
                    "a.w.v_bias": full_array(
                        num_heads,
                        head_size,
                        fill=0.0,
                        device_dtype=device_dtype,
                        garbage=garbage,
                    ),
                    "a.w.o_bias": full_array(
                        hidden_size,
                        fill=0.0,
                        device_dtype=device_dtype,
                        garbage=garbage,
                    ),
                }
            )

        if self.use_mlp:
            weights.update(
                apply_prefix(
                    self.init_norm_weights(
                        hidden_size=hidden_size,
                        device_dtype=device_dtype,
                        garbage=garbage,
                    ),
                    "m",
                )
            )

            if self.use_m_topk or self.use_m_topk_sparse:
                assert m_topk_block_count is not None
                assert m_topk_neurons_per_block is not None
                proj_weight = basic_linear_array(m_topk_block_count, hidden_size, device_dtype=device_dtype)
                proj_weight_new = Array(proj_weight.value.clone() * m_topk_weight_scale)

                weights.update(
                    {
                        "m_topk.w.proj_weight": proj_weight_new,
                        "m_topk.w.weight_bias": full_array(
                            m_topk_block_count,
                            fill=0.0,
                            device_dtype=device_dtype,
                            garbage=garbage,
                        ),
                        "m_topk.w.sig_weight_slope": full_array(
                            m_topk_block_count,
                            fill=sig_weight_slope_init,
                            device_dtype=device_dtype,
                            garbage=garbage,
                        ),
                        "m_topk.w.sig_weight_bias": full_array(
                            m_topk_block_count,
                            fill=sig_weight_bias_init,
                            device_dtype=device_dtype,
                            garbage=garbage,
                        ),
                        "m_topk.w.proj_in_inner": basic_linear_array(
                            *(
                                [1 if self.m_topk_sparse_use_same_weights_for_both else 2]
                                if self.use_m_topk_sparse
                                else []
                            ),
                            m_topk_block_count,
                            m_topk_neurons_per_block,
                            hidden_size,
                            device_dtype=device_dtype,
                            extra_scale=proj_in_proj_out_scale,
                        ),
                        "m_topk.w.proj_out_inner": basic_linear_array(
                            m_topk_block_count,
                            hidden_size,
                            m_topk_neurons_per_block,
                            device_dtype=device_dtype,
                            extra_scale=proj_in_proj_out_scale,
                        ),
                        "m_topk.w.scale": full_array(fill=m_topk_initial_scale, device_dtype=device_dtype),
                    }
                )
                if self.use_m_topk_sparse:
                    proj_inner_val = weights["m_topk.w.proj_in_inner"].cast_array().value.clone()
                    weights["m_topk.w.proj_in_inner"] = Array(torch.tensor(0.0))
                    # assert proj_inner_val.shape[0] == 2
                    proj_inner_val[0] = proj_inner_val[0] * m_topk_sparse_inner_weight_scale
                    weights["m_topk.w.proj_in_inner"] = Array(proj_inner_val)

                    if self.m_topk_sparse_use_weighting_inner:
                        weights.update(
                            {
                                "m_topk.w.inner_weight_bias": full_array(
                                    m_topk_block_count,
                                    m_topk_neurons_per_block,
                                    fill=0.0,
                                    device_dtype=device_dtype,
                                    garbage=garbage,
                                ),
                            }
                        )

                    if not self.m_topk_sparse_disable_inner_sig:
                        weights.update(
                            {
                                "m_topk.w.inner_sig_weight_slope": full_array(
                                    m_topk_block_count,
                                    m_topk_neurons_per_block,
                                    fill=sig_weight_slope_init,
                                    device_dtype=device_dtype,
                                    garbage=garbage,
                                ),
                                "m_topk.w.inner_sig_weight_bias": full_array(
                                    m_topk_block_count,
                                    m_topk_neurons_per_block,
                                    fill=sig_weight_bias_init,
                                    device_dtype=device_dtype,
                                    garbage=garbage,
                                ),
                            }
                        )

            elif self.use_sparse_indexed_mlp:
                assert sparse_indexed_mlp_block_multiplicative_counts is not None
                assert sparse_indexed_mlp_neurons_per_block is not None

                total_blocks = math.prod(sparse_indexed_mlp_block_multiplicative_counts)

                weights.update(
                    {
                        "m_i.w.proj_in": basic_linear_array(
                            total_blocks,
                            sparse_indexed_mlp_neurons_per_block,
                            hidden_size,
                            device_dtype=device_dtype,
                            extra_scale=proj_in_proj_out_scale,
                        ),
                        "m_i.w.proj_out": basic_linear_array(
                            total_blocks,
                            hidden_size,
                            op.unwrap_or(
                                sparse_indexed_mlp_neurons_per_block_out, sparse_indexed_mlp_neurons_per_block
                            ),
                            device_dtype=device_dtype,
                            extra_scale=proj_in_proj_out_scale,
                        ),
                        "m_i.w.scale": full_array(fill=sparse_indexed_mlp_initial_scale, device_dtype=device_dtype),
                    }
                )
                assert len(sparse_indexed_mlp_softmax_weight_scales) == self.sparse_indexed_mlp_weight_count
                assert len(sparse_indexed_mlp_sig_weight_scales) == self.sparse_indexed_mlp_weight_count
                for i in range(self.sparse_indexed_mlp_weight_count):

                    proj_weight = basic_linear_array(
                        math.prod(sparse_indexed_mlp_block_multiplicative_counts[:i]),
                        2,
                        sparse_indexed_mlp_block_multiplicative_counts[i],
                        hidden_size,
                        device_dtype=device_dtype,
                    )
                    proj_weight = Array(
                        proj_weight.value.clone()
                        * torch.tensor(
                            [sparse_indexed_mlp_softmax_weight_scales[i], sparse_indexed_mlp_sig_weight_scales[i]]
                        )[None, :, None, None].to(proj_weight.value)
                    )

                    weights.update({f"m_i.weight{i}.w.proj": proj_weight})
            else:
                mlp_proj = op.unwrap_or(force_num_neurons, hidden_size * 4)

                weights.update(
                    {
                        "m.w.proj_in": basic_linear_array(
                            mlp_proj,
                            hidden_size,
                            device_dtype=device_dtype,
                            extra_scale=proj_in_proj_out_scale,
                        ),
                        "m.w.in_bias": full_array(
                            mlp_proj,
                            fill=0.0,
                            device_dtype=device_dtype,
                            garbage=garbage,
                        ),
                        "m.w.proj_out": basic_linear_array(
                            hidden_size,
                            mlp_proj // (2 if self.mlp_act_type == "bilinear" else 1),
                            device_dtype=device_dtype,
                            extra_scale=proj_in_proj_out_scale,
                        ),
                    }
                )

            if self.mlp_output_bias:
                assert not self.use_sparse_indexed_mlp
                weights.update(
                    {
                        "m.w.out_bias": full_array(
                            hidden_size,
                            fill=0.0,
                            device_dtype=device_dtype,
                            garbage=garbage,
                        )
                    }
                )

        return rename_circs_to_keys(weights, "_arr")


# aka cross entropy, aka log loss
log_likelyhood_str = f"""
'll' GeneralFunction gen_index_at_0_batch_x_c
  'log_probs' GeneralFunction log_softmax
    'll.input' [?] Symbol b9d111e5-b793-4f63-84a0-2f8590b9f39c
  'll.label' [] Symbol 74c503b9-fe2c-4f8b-9350-7351a292c351

'll.input'
'll.label'

'nll' Einsum ,->
  'll'
  'nll.neg' [] Scalar -1
"""

log_likelyhood_circs = add_new_circs(log_likelyhood_str, {})
log_likelyhood = ModuleLibraryRet.mk(log_likelyhood_circs, "ll")
negative_log_likelyhood = ModuleLibraryRet.mk(log_likelyhood_circs, "nll")


# TODO: maybe add more bindings on top of this
@frozen
class TransformerParams:
    block_params: TransformerBlockParams = TransformerBlockParams()
    num_layers: int = 2
    use_norm_output: bool = True
    output_bias: bool = False

    @property
    def norm_type(self):
        return self.block_params.norm_type

    @functools.cache
    def get(self):
        blocks = [self.block_params.get_rebound_weighty(i) for i in range(self.num_layers)]
        # keeps right ordering
        circs = dict(x for b in blocks for x in b.circs.items())

        extra_shape = tuple(op.it(self.block_params.batch_size))
        out: Circuit = Symbol(
            extra_shape + (None, None),
            UUID("ece2bb5d-c6d6-4b7a-93a5-32b5ac264888"),
            f"t.input",
        )
        assert "t.input" not in circs
        circs["t.input"] = out
        for i, block in enumerate(blocks):
            out = module_new_bind(block.body, ("b.input", out), name=f"b{i}.call")
            assert out.shape == extra_shape + (None, None), out.shape
            circs[out.name] = out

        if self.norm_type is not None and self.use_norm_output:
            circs = {
                **circs,
                **(final_ln_bind if self.norm_type == "ln" else final_bn_bind).circs,
            }
            final_norm_str = f"""
            'final.call' Module
              'final.norm'
              '{out.name}' ! 'final.norm.input'
            """
            circs = add_new_circs(final_norm_str, circs)
            out = circs["final.call"]

        b = "b" if self.block_params.batch_size is not None else ""
        logits_str = f"""
        't.logits' Einsum {b}sh,vh->{b}sv
          '{out.name}'
          't.w.unembed' [?, ?] Symbol 85d5a05a-ef9e-4910-a967-3f27951f67cf
        't.logits_p_bias' Add
          't.logits'
          't.w.unembed_bias' [?] Symbol 62d9f91a-5df2-4eb8-af75-5bdfb15eb974

        't.w.unembed'
        't.w.unembed_bias'
        """
        circs = add_new_circs(logits_str, circs)
        if not self.output_bias:
            circs = {s: c for s, c in circs.items() if s not in ["t.w.unembed_bias", "t.logits_p_bias"]}

        return ModuleLibraryRet.mk(circs, name="t.logits" + ("_p_bias" if self.output_bias else ""))

    def init_weights(
        self,
        hidden_size: int,
        head_size: int,
        num_heads: int,
        vocab_size: int,
        device_dtype: TorchDeviceDtypeOp = TorchDeviceDtypeOp(),
        garbage: bool = False,
        force_num_neurons: Optional[int] = None,
        pos_head_size: Optional[int] = None,
        pos_hidden_size: Optional[int] = None,
        proj_in_proj_out_base_scale: float = 1.0,
        proj_in_proj_out_scale_by_rsqrt_layer_num: bool = True,
        sig_weight_bias_init: float = 3.0,
        sig_weight_slope_init: float = 0.0,
        add_hoc_unembed_var: float = 0.1,  # TODO: fix this as needed!
        m_topk_weight_scale: float = 1.0,
        m_topk_initial_scale: float = 1.0,
        m_topk_block_count: Optional[int] = None,
        m_topk_neurons_per_block: Optional[int] = None,
        m_topk_sparse_inner_weight_scale: float = 1.0,
        sparse_indexed_mlp_softmax_weight_scales: list[float] = [1.0, 1.0],
        sparse_indexed_mlp_sig_weight_scales: list[float] = [1.0, 1.0],
        sparse_indexed_mlp_initial_scale: float = 1.0,
        sparse_indexed_mlp_block_multiplicative_counts: Optional[list[int]] = None,
        sparse_indexed_mlp_neurons_per_block: Optional[int] = None,
        sparse_indexed_mlp_neurons_per_block_out: Optional[int] = None,
        pipeline_devices_by_layer: Optional[list[str]] = None,
        final_pipeline_device: Optional[str] = None,
    ):
        weights: Dict[str, Circuit] = {}
        pipeline_devices_by_layer_v = op.unwrap_or(pipeline_devices_by_layer, [device_dtype.device] * self.num_layers)
        assert len(pipeline_devices_by_layer_v) == self.num_layers
        for i in range(self.num_layers):
            weights.update(
                {
                    add_number(s, i): c
                    for s, c in self.block_params.init_weights(
                        hidden_size=hidden_size,
                        head_size=head_size,
                        num_heads=num_heads,
                        device_dtype=TorchDeviceDtypeOp(
                            dtype=device_dtype.dtype,
                            device=pipeline_devices_by_layer_v[i],
                        ),
                        garbage=garbage,
                        force_num_neurons=force_num_neurons,
                        pos_head_size=pos_head_size,
                        pos_hidden_size=pos_hidden_size,
                        proj_in_proj_out_scale=proj_in_proj_out_base_scale
                        / (math.sqrt(i + 1) if proj_in_proj_out_scale_by_rsqrt_layer_num else 1.0),
                        sig_weight_bias_init=sig_weight_bias_init,
                        sig_weight_slope_init=sig_weight_slope_init,
                        m_topk_weight_scale=m_topk_weight_scale,
                        m_topk_initial_scale=m_topk_initial_scale,
                        m_topk_block_count=m_topk_block_count,
                        m_topk_neurons_per_block=m_topk_neurons_per_block,
                        m_topk_sparse_inner_weight_scale=m_topk_sparse_inner_weight_scale,
                        sparse_indexed_mlp_softmax_weight_scales=sparse_indexed_mlp_softmax_weight_scales,
                        sparse_indexed_mlp_sig_weight_scales=sparse_indexed_mlp_sig_weight_scales,
                        sparse_indexed_mlp_initial_scale=sparse_indexed_mlp_initial_scale,
                        sparse_indexed_mlp_block_multiplicative_counts=sparse_indexed_mlp_block_multiplicative_counts,
                        sparse_indexed_mlp_neurons_per_block=sparse_indexed_mlp_neurons_per_block,
                        sparse_indexed_mlp_neurons_per_block_out=sparse_indexed_mlp_neurons_per_block_out,
                    ).items()
                }
            )
        out_device_dtype = TorchDeviceDtypeOp(
            dtype=device_dtype.dtype, device=op.unwrap_or(final_pipeline_device, pipeline_devices_by_layer_v[-1])
        )
        if self.use_norm_output:
            weights.update(
                apply_prefix(
                    self.block_params.init_norm_weights(
                        hidden_size=hidden_size,
                        device_dtype=out_device_dtype,
                        garbage=garbage,
                    ),
                    "final",
                )
            )

        weights["t.w.unembed"] = Array(
            Array.randn(vocab_size, hidden_size, device_dtype=out_device_dtype).value
            * torch.sqrt(torch.tensor(add_hoc_unembed_var))
        )

        if self.output_bias:
            weights["t.w.unembed_bias"] = full_array(
                vocab_size, fill=0.0, device_dtype=out_device_dtype, garbage=garbage
            )

        return rename_circs_to_keys(weights, rename_suffix="_arr")

    def init_embeds(
        self,
        hidden_size: int,
        vocab_size: int,
        max_seq_len: int,
        pos_hidden_size: Optional[int] = None,
        device_dtype: TorchDeviceDtypeOp = TorchDeviceDtypeOp(),
        ad_hoc_embed_var: float = 0.1,  # TODO: fix this as needed!
    ):
        return rename_circs_to_keys(
            {
                "t.w.tok_embeds": Array(
                    Array.randn(vocab_size, hidden_size, device_dtype=device_dtype).value
                    * torch.sqrt(torch.tensor(ad_hoc_embed_var))
                ),
                "t.w.pos_embeds": Array(
                    Array.randn(
                        max_seq_len,
                        op.unwrap(pos_hidden_size)
                        if self.block_params.use_a_topk or self.block_params.use_a_sep
                        else hidden_size,
                        device_dtype=device_dtype,
                    ).value
                    * torch.sqrt(torch.tensor(ad_hoc_embed_var))
                ),
            }
        )

    def garbage_call(
        self,
        hidden_size: int = 3,
        head_size: int = 5,
        num_heads: int = 7,
        seq_len: int = 9,
        vocab_size: int = 11,
        batch_shape: Tuple[int, ...] = (13, 2),
        device_dtype: TorchDeviceDtypeOp = TorchDeviceDtypeOp(),
    ):
        """be warned this is not random init, it's GARBAGE, it won't train or behave properly at all"""
        weights = self.init_weights(
            hidden_size=hidden_size,
            head_size=head_size,
            num_heads=num_heads,
            vocab_size=vocab_size,
            device_dtype=device_dtype,
            garbage=True,
        )

        # this could be made faster if we needed
        # seems fine for now
        bound_weights = module_new_bind(self.get().body, *weights.items(), name="t.bind_w")
        inputs = rename_circs_to_keys(
            {
                "t.input": Array.randn(*batch_shape, seq_len, hidden_size),
                "a.mask": Array.randn(seq_len, seq_len, device_dtype=device_dtype),
                **(
                    {"a.pos_input": Array.randn(*batch_shape, seq_len, hidden_size)}
                    if self.block_params.attn_pos
                    else {}
                ),
            },
            rename_suffix="_rand_inp",
        )
        return (
            module_new_bind(bound_weights, *inputs.items(), name="t.call"),
            weights,
            inputs,
        )


@frozen
class TransformerInfo:
    params: TransformerParams
    model_class: str = "GPTBeginEndToks"
    # maybe below 2 shouldn't be optional?
    pos_enc_type: Optional[PosEncType] = "gpt"
    causal_mask: Optional[bool] = True
    extra: Optional[Any] = None

    def dump_model_string(self, *circs: Circuit):
        info_json = make_json_converter().dumps(self)
        assert "\n" not in info_json
        prefix_str = f"# info:{info_json}\n"
        rep = PrintOptions(reference_circuits={c: s for s, c in self.params.get().circs.items()}).repr(
            *circs,
        )

        return prefix_str + rep + "\n"

    def bind_to_input(
        self,
        c: Circuit,
        inp_tok_embeds: Circuit,
        pos_embed_weights: Optional[Circuit] = None,
        inp_mask: Optional[Circuit] = None,
        inp_mask_has_q: bool = False,
        prefix: str = "t",
    ):
        seq_len: int = cast(int, inp_tok_embeds.shape[-2])

        if pos_embed_weights is None:
            pos_embeds = None
        else:
            pos_embeds = pos_embed_weights.index(
                I[
                    None:seq_len,
                ],
                name="t.w.pos_embeds_idxed",
            )
        inp: Circuit
        if self.pos_enc_type == "gpt":
            assert pos_embeds is not None
            inp = Add(inp_tok_embeds, pos_embeds, name=f"{prefix}.inp_tok_pos")
        else:
            inp = inp_tok_embeds

        mask: Circuit
        if self.causal_mask:
            mask = Array(
                (torch.arange(seq_len)[:, None] >= torch.arange(seq_len)[None, :]).to(
                    device=inp_tok_embeds.device,
                    dtype=inp_tok_embeds.torch_dtype or torch.float32,
                ),
                "t.a.c.causal_mask",  # prefix doesn't apply to constants
            )
        else:
            mask = Scalar(1.0, shape=(seq_len, seq_len), name="t.a.c.full_mask")

        if inp_mask is not None:

            class DimNumMaker:
                num: int = 0

                def __call__(self, n: int):
                    out = tuple(range(self.num, self.num + n))
                    self.num += n
                    return out

            m = DimNumMaker()
            [k] = m(1)
            [q] = m(1)
            batch = m(inp_mask.ndim - 1 - (1 if inp_mask_has_q else 0))
            # TODO: simplify out 1 in this case!
            mask = Einsum(
                (inp_mask, batch + ((q, k) if inp_mask_has_q else (k,))),
                (mask, (q, k)),
                out_axes=batch + (q, k),
                name=f"{prefix}.a.mask",
            )

        pairs = [("t.input", inp), ("a.mask", mask)]
        if self.pos_enc_type == "shortformer":
            assert pos_embeds is not None
            pairs.append(("a.pos_input", pos_embeds))

        return module_new_bind(c, *pairs, name=f"{prefix}.call")

    def bind_to_input_tokens(
        self,
        c: Circuit,
        toks: Circuit,
        tok_embed_weights: Circuit,
        pos_embed_weights: Circuit,
        inp_mask: Optional[Circuit] = None,
        inp_mask_has_q: bool = False,
        prefix: str = "t",
    ):
        embedded = GeneralFunction.gen_index(tok_embed_weights, toks, -2)
        return self.bind_to_input(c, embedded, pos_embed_weights, inp_mask, inp_mask_has_q, prefix)

    def bind_to_input_tokens_int16(
        self,
        c: Circuit,
        toks: torch.Tensor,
        tok_embed_weights: Circuit,
        pos_embed_weights: Circuit,
        inp_mask: Optional[Circuit] = None,
        inp_mask_has_q: bool = False,
        prefix: str = "t",
    ):
        tok_array = Array(toks)
        upcasted = Module(
            token_upcast_module,
            "toks_upcasted",
            **{"upcast_toks.int16_toks": tok_array},
        )
        return self.bind_to_input_tokens(
            c,
            upcasted,
            tok_embed_weights,
            pos_embed_weights,
            inp_mask,
            inp_mask_has_q,
            prefix,
        )


def load_transformer_model_string(
    s: str, parser: Optional[Parser] = None
) -> tuple[dict[str, Circuit], Any, TransformerInfo]:
    s = s.strip("\n")
    assert s.startswith("# info:")
    info_s, _, _ = s.partition("\n")

    info = cattrs.structure(json.loads(info_s.removeprefix("# info:")), TransformerInfo)

    circs = info.params.get().circs
    added = add_new_circs(s, circs, parser=parser)

    # copied out of model_loading to work in open source version
    try:
        from interp.model.model_loading import MODEL_CLASS_STR_TO_MODEL_AND_TOKENIZER_FNS

        tokenizer = MODEL_CLASS_STR_TO_MODEL_AND_TOKENIZER_FNS[info.model_class][1]()
    except ImportError:
        if info.model_class in {"GPT", "GPTBeginEndToks"}:
            import transformers

            tokenizer = transformers.GPT2TokenizerFast.from_pretrained("gpt2")
            tokenizer._add_tokens(["[END]"])
            tokenizer.pad_token = "[END]"
            if info.model_class == "GPTBeginEndToks":
                tokenizer._add_tokens(["[BEGIN]"])
                tokenizer.eos_token = "[END]"
        else:
            raise

    return (added, tokenizer, info)


def get_model_path(model_id: str):
    from rust_circuit.rrfs import RRFS_DIR

    # we should plausibly eventually remove current circ_models/ and replace with circ_models3/
    return f"{RRFS_DIR}/circ_models3/{model_id}.circ"


def load_model_id(model_id: str, parser: Optional[Parser] = None) -> tuple[dict[str, Circuit], Any, TransformerInfo]:
    """Returns (circs, tokenizer, info)"""
    with open(get_model_path(model_id)) as f:
        return load_transformer_model_string(f.read(), parser=parser)


token_upcast_module = make_spec(
    P(
        """
'upcast_toks.sub' Add
  'upcast_toks' GeneralFunction cast_from_{device:None,dtype:None}_to_{device:None,dtype:int64}
    'upcast_toks.int16_toks' [] Symbol
  'upcast_toks.signed_int16_min' [] Scalar 32768 # int16 min, torch doesn't support uint16 :(
"""
    ),
    [P("'upcast_toks.int16_toks' [] Symbol")],
)
