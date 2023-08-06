from typing import Optional
from uuid import UUID

import torch

import rust_circuit.optional as op
from rust_circuit import (
    Circuit,
    GeneralFunction,
    GeneralFunctionShapeInfo,
    GeneralFunctionSpecBase,
    Shape,
    TorchDeviceDtypeOp,
)


@torch.jit.script
def output_scatter_function(output_dirs: torch.Tensor, idx: torch.Tensor, B: int):
    assert idx.shape == (output_dirs.shape[0],)
    return torch.zeros((B, output_dirs.shape[-1]), dtype=output_dirs.dtype, device=output_dirs.device).scatter_add_(
        dim=0, index=idx.unsqueeze(-1).expand_as(output_dirs), src=output_dirs
    )


class OutputScatter(GeneralFunctionSpecBase):
    @property
    def name(self) -> str:
        return "output_scatter"

    def compute_hash_bytes(self) -> bytes:
        return UUID("fe8aaaa8-a2f1-4108-acdb-544e1e45b9bd").bytes

    def function(self, output_dirs: torch.Tensor, idx: torch.Tensor, b_shape_arg: torch.Tensor) -> torch.Tensor:  # type: ignore[override]
        return output_scatter_function(
            output_dirs.reshape(-1, output_dirs.shape[-1]), idx.view(-1), b_shape_arg.numel()
        ).view(*b_shape_arg.shape, output_dirs.shape[-1])

    def get_shape_info(self, *shapes: Shape) -> GeneralFunctionShapeInfo:
        assert len(shapes) == 3

        assert len(shapes[0]) >= 1
        # assert shapes[0][:-1] == shapes[1]

        return GeneralFunctionShapeInfo((*shapes[2], shapes[0][-1]), len(shapes[2]) + 1, [False, False, False])

    def get_device_dtype_override(self, *device_dtypes: TorchDeviceDtypeOp) -> Optional[TorchDeviceDtypeOp]:
        devices = set(dd.device for dd in device_dtypes[:-1] if dd.device is not None)
        assert len(devices) in [0, 1]
        assert device_dtypes[0].dtype in ["bfloat16", "float32", None]
        assert device_dtypes[1].dtype in ["int64", None]

        return TorchDeviceDtypeOp(
            next(iter(devices)) if len(devices) > 0 else None, dtype=op.unwrap_or(device_dtypes[0].dtype, "float32")
        )

    @classmethod
    def new(
        cls,
        proj_out: Circuit,
        idx: Circuit,
        b_shape_arg: Circuit,
        name: Optional[str] = None,
    ):
        """convenience function"""
        return GeneralFunction(proj_out, idx, b_shape_arg, spec=cls(), name=name)

    @property
    def path(self) -> str:
        return "rust_circuit.generalfuncs.mlp_topk:OutputScatter"


# @torch.jit.ignore
# def kth_smallest_value(x: torch.Tensor, k: torch.Tensor):
#     return torch.kthvalue(x, k=int(k.item()), dim=-1).values


@torch.jit.script
def kth_largest_value(x: torch.Tensor, k: torch.Tensor):
    # NOTE: topk is *way* faster than kthvalue in my benchmarks
    # in theory it should be possible to be quite a bit faster than this...
    return torch.topk(x.detach(), k=int(k.item()), dim=-1, sorted=True).values[..., -1]


class KthLargestValue(GeneralFunctionSpecBase):
    @property
    def name(self) -> str:
        return "kth_largest_value"

    def compute_hash_bytes(self) -> bytes:
        return UUID("1d7733e3-d172-4929-bbcf-aa1ca0c92277").bytes

    def function(self, *args: torch.Tensor) -> torch.Tensor:  # type: ignore[override]
        return kth_largest_value(*args)

    def get_shape_info(self, *shapes: Shape) -> GeneralFunctionShapeInfo:
        assert len(shapes) == 2

        assert len(shapes[0]) >= 1
        assert len(shapes[1]) == 0

        return GeneralFunctionShapeInfo(shapes[0][:-1], 0, [True, False])

    def get_device_dtype_override(self, *device_dtypes: TorchDeviceDtypeOp) -> Optional[TorchDeviceDtypeOp]:
        k_dtype = device_dtypes[1].get_torch_dtype()
        assert k_dtype is None or (not k_dtype.is_floating_point)

        return device_dtypes[0]

    @classmethod
    def new(
        cls,
        x: Circuit,
        k: Circuit,
        name: Optional[str] = None,
    ):
        """convenience function"""
        return GeneralFunction(x, k, spec=cls(), name=name)

    @property
    def path(self) -> str:
        return "rust_circuit.generalfuncs.mlp_topk:KthLargestValue"


@torch.jit.script
def sampled_index(values: torch.Tensor, sampled_idx: torch.Tensor):
    return values[torch.arange(values.shape[0], device=sampled_idx.device)[:, None], sampled_idx]


class SampledIndex(GeneralFunctionSpecBase):
    @property
    def name(self) -> str:
        return "sampled_index"

    def compute_hash_bytes(self) -> bytes:
        return UUID("b388f6e7-ddb3-4dc8-8be0-8e5b123aa1c2").bytes

    def function(self, *args) -> torch.Tensor:  # type: ignore[override]
        return sampled_index(*args)

    def get_shape_info(self, *shapes: Shape) -> GeneralFunctionShapeInfo:
        assert len(shapes) == 2

        values_shape, sampled_idxs_shape = shapes

        O, _ = values_shape
        (O_, C) = sampled_idxs_shape
        # assert O ==  O_, (O, O_)

        return GeneralFunctionShapeInfo((O, C), 2, [False, False])

    def get_device_dtype_override(self, *device_dtypes: TorchDeviceDtypeOp) -> Optional[TorchDeviceDtypeOp]:
        devices = set(dd.device for dd in device_dtypes if dd.device is not None)
        assert len(devices) in [0, 1]
        assert device_dtypes[1].dtype in ["int64", None]

        return TorchDeviceDtypeOp(next(iter(devices)) if len(devices) > 0 else None, dtype=device_dtypes[0].dtype)

    @classmethod
    def new(
        cls,
        values: Circuit,
        sampled_idx: Circuit,
        name: Optional[str] = None,
    ):
        """convenience function"""
        return GeneralFunction(values, sampled_idx, spec=cls(), name=name)

    @property
    def path(self) -> str:
        return "rust_circuit.generalfuncs.mlp_topk:SampledIndex"
