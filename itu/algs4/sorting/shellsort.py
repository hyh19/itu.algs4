# Created for BADS 2018
# See README.md for details
# This is python3
"""The Shellsort module provides static methods for sorting an array using
shellsort with Knuth's increment sequence (1, 4, 13, 40, ...)."""

from __future__ import annotations

import sys
from typing import List, TypeVar, Protocol

T = TypeVar("T", bound="Comparable")


class Comparable(Protocol):
    """Protocol for annotating comparable types."""

    def __lt__(self: T, other: T) -> bool:
        ...


def sort(a: List[T]) -> None:
    """Rearranges the array in ascending order using the natural order.

    :param a: the array to be sorted.

    """
    N = len(a)
    h = 1
    while h < int(N / 3):
        h = (3 * h) + 1
    while h >= 1:
        # h-sort the array
        for i in range(h, N):
            # Insert a[i] among a[i-h], a[i-2*h], a[i-3*h]...
            for j in range(i, h - 1, -h):
                if not _less(a[j], a[j - h]):
                    break
                _exch(a, j, j - h)
        h = int(h / 3)


def _less(v: T, w: T) -> bool:
    return v < w


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
    assert is_sorted(a)
    _show(a)


if __name__ == "__main__":
    main()
