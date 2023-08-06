from __future__ import annotations

import abc
import inspect
import uuid
from typing import Callable, ClassVar, Optional, Protocol, Self

import torch

from . import _rust as rc


class GeneralFunctionSpecBase(metaclass=abc.ABCMeta):
    __hash_bytes: ClassVar[bytes]
    """
    Inherit from this base class in order to implement an arbitrary new GeneralFunctionSpec.

    See docs for `get_shape_info`, GeneralFunctionShapeInfo, and `function`.
    """

    def __init_subclass__(cls):
        b = bytearray()
        for _, x in inspect.getmembers(cls, inspect.ismethod):
            if hasattr(x, "__code__"):
                b.extend(x.__code__.co_code)
                b.extend(uuid.UUID("6739c5c8-a9ab-421d-a06c-38f356bed339").bytes)
        b.extend(uuid.UUID("c5b1184c-76ae-430a-87cc-d6afc90569ce").bytes)
        b.extend((cls.__module__ + "." + cls.__name__).encode())
        b.extend(uuid.UUID("b199fb64-9ee6-419f-a325-ae4e7106bdd7").bytes)
        cls.__hash_bytes = bytes(b)

    @classmethod
    def new(cls, *xs: rc.Circuit, name: Optional[str] = None) -> rc.GeneralFunction:
        """This should be overridden if your generalfunction has non-Circuit arguments"""
        return rc.GeneralFunction(*xs, spec=cls(), name=name)

    @property
    def name(self) -> str:
        """Only used for auto-naming"""
        return self.__class__.__name__

    @property
    def path(self) -> str:
        """Used for printing & parsing

        The path of this spec relative to RRFS_DIR if this is stored in rrfs.
        Should be of the form /dir/sub_dir/.../file.py:MyCustomSpec, otherwise should be import.path.to.containing.module:MyCustomSpec"""
        cls = self.__class__
        return cls.__module__ + ":" + cls.__name__

    @staticmethod
    def parse_data(s: str) -> GeneralFunctionSpecBase:
        """Parse extra data serialized by serialize_data. Should be implemented if serialize_data is"""
        raise NotImplementedError

    def serialize_data(self) -> Optional[str]:
        """Serialize extra data (that you're storing on `self`) for printing, parsing, and hashing"""
        return None

    def compute_hash_bytes(self) -> bytes:
        """What parts of self should be used for hashing & equality? Important that this is correct, otherwise many things will be wrong!

        Should be arbitrary-length bytes such that `x != y => x.compute_hash_bytes() != y.compute_hash_bytes()`

        should be implemented if you store data on `self` and don't implement serialize_data. otherwise is automatically implemented to change if class code changes (but might not change if only referenced globals change! beware for notebook use)"""
        x = self.serialize_data()
        if x is not None:
            return self.__hash_bytes + x.encode()
        return self.__hash_bytes

    @abc.abstractmethod
    # should be able to do this but mypy says no, maybe try again at some point
    # def function(self, *tensors: Unpack[Tuple[torch.Tensor] | Tuple[torch.Tensor, torch.Tensor] | etc ]) -> torch.Tensor:
    def function(self, *tensors: torch.Tensor) -> torch.Tensor:
        """run the actual function on tensors - these tensors shapes correspond to the shapes in ``get_shape_info``"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_shape_info(self, *shapes: rc.Shape) -> rc.GeneralFunctionShapeInfo:
        """This should error (exception) if the shapes are invalid and otherwise return GeneralFunctionShapeInfo"""
        raise NotImplementedError

    def get_device_dtype_override(self, *device_dtypes: rc.TorchDeviceDtypeOp) -> Optional[rc.TorchDeviceDtypeOp]:
        """Use this to check the validity of input dtypes/devices and set output device/dtype. If this returns None, the output inherits device/dtype from children.
        This can error to signal that inputs have invalid dtypes/devices"""
        return None

    def should_const_fold(self, self_circ: rc.GeneralFunction[Self]) -> bool:
        """Should this function be evaluated if possible during circuit optimization?"""
        return self_circ.rank == 0 and self_circ.num_children == 1 and self_circ.children[0].rank == 0


class MultiOutputGeneralFunctionSpecBase(metaclass=abc.ABCMeta):
    __hash_bytes: ClassVar[bytes]
    """
    Inherit from this base class in order to implement an arbitrary new GeneralFunctionSpec.

    See docs for `get_shape_info`, GeneralFunctionShapeInfo, and `function`.
    """

    def __init_subclass__(cls):
        b = bytearray()
        for _, x in inspect.getmembers(cls, inspect.ismethod):
            if hasattr(x, "__code__"):
                b.extend(x.__code__.co_code)
                b.extend(uuid.UUID("6739c5c8-a9ab-421d-a06c-38f356bed339").bytes)
        b.extend(uuid.UUID("c5b1184c-76ae-430a-87cc-d6afc90569ce").bytes)
        b.extend((cls.__module__ + "." + cls.__name__).encode())
        cls.__hash_bytes = bytes(b)

    @classmethod
    def new(cls, *xs: rc.Circuit, name: Optional[str] = None) -> list[rc.GeneralFunction]:
        """This should be overridden if your generalfunction has non-Circuit arguments"""
        return rc.GeneralFunction.new_multi_output(*xs, spec=cls(), name=name)

    @property
    def name(self) -> str:
        """Only used for auto-naming"""
        return self.__class__.__name__

    @property
    def path(self) -> Optional[str]:
        """Used for printing & parsing

        The path of this spec relative to RRFS_DIR if this is stored in rrfs.
        Should be of the form /dir/sub_dir/.../file.py:MyCustomSpec, otherwise should be import.path.to.containing.module:MyCustomSpec"""
        cls = self.__class__
        return cls.__module__ + ":" + cls.__name__

    @staticmethod
    def parse_data(s: str) -> GeneralFunctionSpecBase:
        """Parse extra data serialized by serialize_data. Should be implemented if serialize_data is"""
        raise NotImplementedError

    def serialize_data(self) -> Optional[str]:
        """Serialize extra data (that you're storing on `self`) for printing, parsing, and hashing"""
        return None

    def compute_hash_bytes(self) -> bytes:
        """What parts of self should be used for hashing & equality? Important that this is correct, otherwise many things will be wrong!

        Should be arbitrary-length bytes such that `x != y => x.compute_hash_bytes() != y.compute_hash_bytes()`

        should be implemented if you store data on `self` and don't implement serialize_data. otherwise is automatically implemented to change if class code changes (but might not change if only referenced globals change! beware for notebook use)"""
        x = self.serialize_data()
        if x is not None:
            return self.__hash_bytes + x.encode()
        return self.__hash_bytes

    @abc.abstractmethod
    def function(self, *tensors: torch.Tensor) -> list[torch.Tensor]:
        """run the actual function on tensors - these tensors shapes correspond to the shapes in ``get_shape_info``"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_shape_info(self, *shapes: rc.Shape) -> list[rc.GeneralFunctionShapeInfo]:
        """This should error (exception) if the shapes are invalid and otherwise return GeneralFunctionShapeInfo"""
        raise NotImplementedError

    def get_device_dtype_override(
        self, *device_dtypes: rc.TorchDeviceDtypeOp
    ) -> Optional[list[Optional[rc.TorchDeviceDtypeOp]]]:
        """Use this to check the validity of input dtypes/devices and set output device/dtype. If this returns None, the output inherits device/dtype from children.
        This can error to signal that inputs have invalid dtypes/devices"""
        return None

    def should_const_fold(self, self_circ: rc.GeneralFunction[Self]) -> bool:
        """Should this function be evaluated if possible during circuit optimization?"""
        return self_circ.rank == 0 and self_circ.num_children == 1 and self_circ.children[0].rank == 0
