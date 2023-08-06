from time import perf_counter
from typing import Generic, Iterable, List, Mapping, NoReturn, Optional, Tuple, TypeVar, Union

import torch

from ._rust import TorchAxisIndex


def assert_never(x: NoReturn) -> NoReturn:
    raise AssertionError(f"Invalid value: {x!r}")


def check_cast(cls, c, exception=TypeError):
    if isinstance(c, cls):
        return c
    else:
        raise exception(f"Requested type {repr(cls)} does not match the type of the input, {type(c)}.")


class timed:
    def __init__(self, name, min_to_print=None, extra_print=None):
        self.name = name
        self.min_to_print = min_to_print
        self.extra_print = extra_print

    def __enter__(self):
        self.start = perf_counter()
        return self

    def __exit__(self, type, value, traceback):
        self.time = perf_counter() - self.start
        self.readout = f"{self.name} took {self.time:.4f}"
        if self.min_to_print is None or self.min_to_print < self.time:
            print(self.readout + (self.extra_print if self.extra_print is not None else ""))


TorchIndex = Union[Tuple[TorchAxisIndex, ...], TorchAxisIndex]


class Indexer:
    """Helper for defining slices more easily which always returns tuples
    (instead of sometimes returning just TorchAxisIndex)."""

    def __getitem__(self, idx: TorchIndex) -> Tuple[TorchAxisIndex, ...]:
        if isinstance(idx, tuple):
            return idx
        return (idx,)


class Slicer:
    """Helper for defining slices more easily which always returns slices"""

    def __getitem__(self, idx: slice) -> slice:
        assert isinstance(idx, slice)
        return idx


I = Indexer()
S = Slicer()

KT = TypeVar("KT")
VT = TypeVar("VT")


# Dict is an invariant type by default. We declare FrozenDict to be covariant using Generic.
class FrozenDict(dict, Generic[KT, VT]):
    # TODO: maybe this should actually use frozendict...
    _cached_hash: Optional[int] = None
    _cached_tuple: Optional[Tuple] = None

    def _to_tuple(self):
        if self._cached_tuple is None:
            self._cached_tuple = tuple(sorted(self.items(), key=lambda x: hash(x)))
        return self._cached_tuple

    def __hash__(self):
        if self._cached_hash is None:
            self._cached_hash = hash(("tao's FrozenDict", self._to_tuple()))
        return self._cached_hash

    def __eq__(self, other):
        # Possible hash collisions when sorting the tuple in _to_tuple make the
        # implementation of FrozenDict.__eq__ complicated"
        # TODO use frozendict
        return isinstance(other, FrozenDict) and dict(self) == dict(other)

    def clear_cache(self):
        self._cached_hash = self._cached_tuple = None

    def __repr__(self):
        return f"{self.__class__.__name__}({super().__repr__()})"


def get_slice_list(n: int) -> List[TorchAxisIndex]:
    return [slice(None)] * n


def make_index_at(index: TorchIndex, at: int):
    return make_index_at_many({at: index})


def to_axis_index(idx: TorchIndex) -> TorchAxisIndex:
    if isinstance(idx, tuple):
        assert len(idx) == 1
        return idx[0]
    else:
        return idx


def make_index_at_many(at_idx: Mapping[int, TorchIndex]) -> Tuple[TorchAxisIndex, ...]:
    out = get_slice_list(max(at_idx.keys(), default=-1) + 1)
    for at, idx in at_idx.items():
        out[at] = to_axis_index(idx)

    return tuple(out)
