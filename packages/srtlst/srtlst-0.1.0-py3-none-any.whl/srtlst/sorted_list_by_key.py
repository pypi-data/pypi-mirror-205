from __future__ import annotations

from typing import Generic, Iterable, Callable, SupportsIndex, TypeVar

from srtlst.sorted_list import SortedList
from srtlst.protocols import _SupportsLT

_T = TypeVar("_T")
_S = TypeVar("_S", bound=_SupportsLT)


class SortedListByKey(SortedList[_T], Generic[_T]):  # type:ignore[type-var]
    def __init__(self, seq: Iterable[_T] = (), /, *, key: Callable[[_T], _S]):
        self._list = list(sorted(seq, key=key))
        self._key = key

    def __getitem__(
        self, item: SupportsIndex | slice
    ) -> SortedListByKey[_T] | _T:  # type:ignore[override]
        found = self._list[item]
        if isinstance(found, list):
            return SortedListByKey(found, key=self._key)
        else:
            return found

    def __copy__(self) -> SortedListByKey[_T]:
        return SortedListByKey(self._list, key=self._key)
