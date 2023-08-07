from __future__ import annotations

from typing import Protocol, Any


class _SupportsLT(Protocol):
    def __lt__(self, other: Any) -> bool:
        ...
