# Created for BADS 2018
# See README.md for details
# This is python3

"""The Quick3Way module provides static methods for sorting an array using
quicksort with 3-way partitioning."""

from __future__ import annotations

import sys
from random import shuffle
from typing import List, TypeVar, Protocol

T = TypeVar("T", bound="Comparable")


class Comparable(Protocol):
    """Protocol for annotating comparable types."""

    def __lt__(self: T, other: T) -> bool: ...


def sort(a: List[T]) -> None:
    """Rearranges the array in ascending order using the natural order.

    :param a: the array to be sorted.

    """
    shuffle(a)  # Eliminate dependency on input.
    _sort(a, 0, len(a) - 1)


def _sort(a: List[T], lo: int, hi: int) -> None:
    if hi <= lo:
        return
    lt = lo
    i = lo + 1
    gt = hi
    v = a[lo]
    while i <= gt:
        cmp = _compare(a[i], v)
        if cmp < 0:
            _exch(a, lt, i)
            lt += 1
            i += 1
        elif cmp > 0:
            _exch(a, i, gt)
            gt -= 1
        else:
            i += 1
    _sort(a, lo, lt - 1)
    _sort(a, gt + 1, hi)
    assert is_sorted(a)


def _compare(a: T, b: T) -> int:
    return (a > b) - (b > a)


def _less(v: T, w: T) -> bool:
    return _compare(v, w) < 0


def _exch(a: List[T], i: int, j: int) -> None:
    t = a[i]
    a[i] = a[j]
    a[j] = t


def _show(a: List[T]) -> None:
    # Prints the array on a single line
    for item in a:
        print(item, end=" ")
    print()


def is_sorted(a: List[T]) -> bool:
    """Returns true if a is sorted.

    :param a: the array to be checked.
    :returns: True if a is sorted.

    """
    for i in range(1, len(a)):
        if _less(a[i], a[i - 1]):
            return False
    return True


def main():
    """Reads in a sequence of strings from standard input; Shellsorts them; and
    prints them to standard output in ascending order."""
    a = sys.argv[1:]
    sort(a)
    _show(a)


if __name__ == "__main__":
    main()
