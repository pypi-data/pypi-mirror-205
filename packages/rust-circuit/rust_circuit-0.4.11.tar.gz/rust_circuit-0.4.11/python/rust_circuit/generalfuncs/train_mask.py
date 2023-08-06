from typing import Optional
from uuid import UUID

import torch

from rust_circuit import (
    Circuit,
    GeneralFunction,
    GeneralFunctionShapeInfo,
    GeneralFunctionSpecBase,
    GeneralFunctionSpecTester,
    Shape,
    TorchDeviceDtypeOp,
)


@torch.jit.script
def make_train_mask(toks: torch.Tensor):
    """expects int16"""
    END_TOKEN = 50256

    is_end = torch.cumsum(toks == (END_TOKEN - 32768), dim=-1)
    blocks = (is_end[..., :, None] == is_end[..., None, :]).float()

    # if we wanted to, we could make BEGIN token always visible.
    # seems better not to I think.
    # blocks[..., 0] = True

    arange = torch.arange(blocks.shape[-1]).to(blocks)
    causal_blocks = blocks * (arange[:, None] >= arange[None, :])

    return causal_blocks.float()


class TrainMask(GeneralFunctionSpecBase):
    @property
    def name(self) -> str:
        return "train_mask"

    def compute_hash_bytes(self) -> bytes:
        return UUID("0f0e3e67-ed77-4b10-a2a1-2fdbb25d5ac2").bytes

    def function(self, toks: torch.Tensor) -> torch.Tensor:  # type: ignore[override]
        return make_train_mask(toks)

    def get_shape_info(self, *shapes: Shape) -> GeneralFunctionShapeInfo:
        assert len(shapes) == 1
        [shape] = shapes
        return GeneralFunctionShapeInfo(
            (shape[:-1] + (shape[-1], shape[-1])), num_non_batchable_output_dims=2, input_batchability=[True]
        )

    def get_device_dtype_override(self, *device_dtypes: TorchDeviceDtypeOp) -> Optional[TorchDeviceDtypeOp]:
        return TorchDeviceDtypeOp(dtype=torch.float, device=device_dtypes[0].device)

    @classmethod
    def new(cls, toks: Circuit, name: Optional[str] = None):
        """convenience function"""
        return GeneralFunction(toks, spec=cls(), name=name)

    @property
    def path(self) -> str:
        return "rust_circuit.generalfuncs.train_mask:TrainMask"
