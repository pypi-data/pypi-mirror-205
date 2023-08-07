"""
This module contains knowledge about the types we use.

Policy
~~~~~~

If any of the following statements is true, move the type to this file:

- if type is used in multiple files
- if type is complex enough it has to be documented
- if type is very important for the public API

"""

import datetime
import typing as t
from decimal import Decimal

__all__ = [
    "CallableSchema",
    "Date",
    "DateTime",
    "FieldCache",
    "JSON",
    "Key",
    "Keywords",
    "Matrix",
    "MissingSeed",
    "Seed",
    "Time",
    "Timestamp",
]

JSON = t.Dict[str, t.Any]

DateTime = datetime.datetime

Time = datetime.time

Date = datetime.date

Timestamp = t.Union[str, int]


class _MissingSeed:
    """We use this type as a placeholder for cases when seed is not set."""


MissingSeed: t.Final = _MissingSeed()
Seed = t.Union[None, int, float, str, bytes, bytearray, _MissingSeed]

Keywords = t.Union[t.List[str], t.Set[str], t.Tuple[str, ...]]

Matrix = t.Union[
    t.List[int],
    t.List[float],
    t.List[complex],
    t.List[Decimal],
]

CallableSchema = t.Callable[[], JSON]

Key = t.Optional[t.Callable[[t.Any], t.Any]]

FieldCache = t.Dict[str, t.Callable[[t.Any], t.Any]]
