# Created for BADS 2018
# See README.md for details
# Python 3

from __future__ import annotations

from typing import List, Optional, TypeVar, Protocol

"""
This module provides functions for sorting an array using mergesort.

For additional documentation, see Section 2.2 of Algorithms, 4th Edition
by Robert Sedgewick and Kevin Wayne.
"""

T = TypeVar("T", bound="Comparable")


class Comparable(Protocol):
    """Protocol for annotating comparable types."""

    def __lt__(self: T, other: T) -> bool: ...


def _is_sorted(a: List[T], lo: int = 0, hi: Optional[int] = None) -> bool:
    # If hi is not specified, use whole array
    if hi is None:
        hi = len(a)

    # check if sublist is sorted
    for i in range(lo + 1, hi):
        if a[i] < a[i - 1]:
            return False
    return True


# stably merge a[lo .. mid] with a[mid+1 ..hi] using aux[lo .. hi]
def _merge(a: List[T], aux: List[T], lo: int, mid: int, hi: int) -> None:
    # precondition: a[lo .. mid] and a[mid+1 .. hi] are sorted subarrays
    assert _is_sorted(a, lo, mid)
    assert _is_sorted(a, mid + 1, hi)

    # copy to aux[]
    for k in range(lo, hi + 1):
        aux[k] = a[k]

    # merge back to a[]
    i, j = lo, mid + 1
    for k in range(lo, hi + 1):
        if i > mid:
            a[k] = aux[j]
            j += 1
        elif j > hi:
            a[k] = aux[i]
            i += 1
        elif aux[j] < aux[i]:
            a[k] = aux[j]
            j += 1
        else:
            a[k] = aux[i]
            i += 1

    # postcondition: a[lo .. hi] is sorted
    assert _is_sorted(a, lo, hi)

    # mergesort a[lo..hi] using auxiliary array aux[lo..hi]


def _sort(a: List[T], aux: List[T], lo: int, hi: int) -> None:
    if hi <= lo:
        return
    mid = lo + (hi - lo) // 2
    _sort(a, aux, lo, mid)
    _sort(a, aux, mid + 1, hi)
    _merge(a, aux, lo, mid, hi)


def sort(a: List[T]) -> None:
    """Rearranges the array in ascending order, using the natural order.

    :param a: the array to be sorted

    """
    aux = a.copy()
    _sort(a, aux, 0, len(a) - 1)
    assert _is_sorted(a)


# Reads in a sequence of strings from standard input or a file
# supplied as argument to the program; mergesorts them;
# and prints them to standard output in ascending order.
if __name__ == "__main__":
    import sys

    from itu.algs4.stdlib import stdio

    #  Sorts a sequence of strings from standard input using mergesort

    if len(sys.argv) > 1:
        try:
            sys.stdin = open(sys.argv[1])
        except IOError:
            print("File not found, using standard input instead")

    a = stdio.readAllStrings()
    sort(a)
    assert _is_sorted(a)
    for elem in a:
        print(elem)
