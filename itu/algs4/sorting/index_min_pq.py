# Created for BADS 2018
# See README.md for details
# Python 3

from __future__ import annotations
from typing import TypeVar, Protocol, List, Optional, Generic, Iterator
from itu.algs4.errors.errors import IllegalArgumentException
from itu.algs4.errors.errors import NoSuchElementException

Key = TypeVar("Key", bound="Comparable")


class Comparable(Protocol):
    """Protocol for annotating comparable types."""

    def __lt__(self: Key, other: Key) -> bool:
        ...


class IndexMinPQ(Generic[Key]):
    """The IndexMinPQ class represents an indexed priority queue of generic
    keys. It supports the usual insert and delete-the-minimum operations, along
    with delete and change-the-key methods. In order to let the client refer to
    the keys on the priority queue,

    an integer between 0 and maxN - 1
    is associated with each key-the client uses this integer to specify
    which key to delete or change.
    It also supports methods for peeking at the minimum key,
    testing if the priority queue is empty, and iterating through
    the keys.
    This implementation uses a binary heap along with an array to associate
    keys with integers, in the given range.
    The insert, delete-the-minimum, delete, change-key, decrease-key, and increase-key
    operations take logarithmic time.
    The is-empty, size, min-index, min-key, and key-of operations take constant time.
    Construction takes time proportional to the specified capacity.

    """

    def __init__(self, max_n: int) -> None:
        """Initializes an empty indexed priority queue with indices between 0.

        and max_n - 1.
        :param max_n: the keys on this priority queue are indices from 0 to max_n - 1
        :raises IllegalArgumentException: if max_n < 0

        """
        self._max_n = max_n
        self._n = 0
        self._pq = [0] * (max_n + 1)
        self._qp = [-1] * (max_n + 1)
        self._keys: List[Optional[Key]] = [None] * (max_n + 1)

    def insert(self, i: int, key: Key) -> None:
        """Associates key with index i.

        :param i: an index
        :param key: the key to associate with index i
        :raises IllegalArgumentException: unless 0 <= i < max_n
        :raises IllegalArgumentException: if there already is an item associated with index i

        """
        if i < 0 or i >= self._max_n:
            raise IllegalArgumentException("index is not within range")
        if self.contains(i):
            raise IllegalArgumentException("index is already in the priority queue")
        self._n += 1
        self._qp[i] = self._n
        self._pq[self._n] = i
        self._keys[i] = key
        self._swim(self._n)

    def contains(self, i: int) -> bool:
        """Is i an index on this priority queue?

        :param i: an index
        :return: True if i is an index on this priority queue False otherwise
        :rtype: bool
        :raises IllegalArgumentException: unless 0 <= i < max_n

        """
        if i < 0 or i >= self._max_n:
            raise IllegalArgumentException("index is not within range")
        return self._qp[i] != -1

    def change_key(self, i: int, key: Key) -> None:
        """Change the key associated with index i to the specified value.

        :param i: the index of the key to change
        :param key: change the key associated with index i to this key
        :raises IllegalArgumentException: unless 0 <= i < max_n
        :raises NoSuchElementException: if no key is associated with index i

        """
        if i < 0 or i >= self._max_n:
            raise IllegalArgumentException("index is not within range")
        if not self.contains(i):
            raise NoSuchElementException("index is not in the priority queue")
        self._keys[i] = key
        self._swim(self._qp[i])
        self._sink(self._qp[i])

    def decrease_key(self, i: int, key: Key) -> None:
        """Decrease the key associated with index i to the specified value.

        :param i: the index of the key to decrease
        :param key: decrease the key associated with index i to this key
        :raises IllegalArgumentException: unless 0 <= i < max_n
        :raises IllegalArgumentException: if key >= key_of(i)
        :raises NoSuchElementException: if no key is associated with index i

        """
        if i < 0 or i >= self._max_n:
            raise IllegalArgumentException("index is not within range")
        if not self.contains(i):
            raise IllegalArgumentException("index is not in the priority queue")
        if self._keys[i] <= key:
            raise IllegalArgumentException(
                "calling decrease_key() with given argument would not strictly decrease the key"
            )
        self._keys[i] = key
        self._swim(self._qp[i])

    def increase_key(self, i: int, key: Key) -> None:
        """Increase the key associated with index i to the specified value.

        :param i: the index of the key to increase
        :param key: increase the key associated with index i to this key
        :raises IllegalArgumentException: unless 0 <= i < max_n
        :raises IllegalArgumentException: if key <= key_of(i)
        :raises NoSuchElementException: if no key is associated with index i

        """
        if i < 0 or i >= self._max_n:
            raise IllegalArgumentException("index is not within range")
        if not self.contains(i):
            raise NoSuchElementException("index is not in the priority queue")
        if self._keys[i] >= key:
            raise IllegalArgumentException(
                "calling increase_key() with given argument would not strictly increase the key"
            )
        self._keys[i] = key
        self._sink(self._qp[i])

    def delete(self, i: int) -> None:
        """Remove the key associated with index i.

        :param i: the index of the key to remove
        :raises IllegalArgumentException: unless 0 <= i < max_n
        :raises NoSuchElementException: if no key is associated with index i

        """
        if i < 0 or i >= self._max_n:
            raise IllegalArgumentException("index is not in range")
        if not self.contains(i):
            raise NoSuchElementException("index is not in the priority queue")
        index = self._qp[i]
        self._exch(index, self._n)
        self._n -= 1
        self._sink(index)
        self._keys[i] = None
        self._qp[i] = -1

    def min_index(self) -> int:
        """
        Returns an index associated with a minimum key.
        :return: an index associated with a minimum key
        :rtype: int
        :raises NoSuchElementException: if this priority queue is empty
        """
        if self._n == 0:
            raise NoSuchElementException("Priority queue underflow")
        return self._pq[1]

    def min_key(self) -> Key:
        """
        Returns a minimum key.
        :return: a minimum key
        :raises NoSuchElementException: if this priority queue is empty
        """
        if self._n == 0:
            raise NoSuchElementException("Priority queue underflow")
        key = self._keys[self._pq[1]]
        assert key is not None
        return key

    def del_min(self) -> int:
        """
        Removes a minimum key and returns its associated index.
        :return: an index associated with a minimum key
        :raises NoSuchElementException: if this priority queue is empty
        :rtype: int
        """
        if self._n == 0:
            raise NoSuchElementException("Priority queue underflow")
        min_index = self._pq[1]
        self._exch(1, self._n)
        self._n -= 1
        self._sink(1)
        self._qp[min_index] = -1
        self._keys[min_index] = None
        self._pq[self._n + 1] = -1
        return min_index

    def is_empty(self) -> bool:
        """Returns True if this priority queue is empty.

        :return: True if this priority queue is empty False otherwise
        :rtype: bool

        """
        return self._n == 0

    def size(self) -> int:
        """Returns the number of keys on this priority queue.

        :return: the number of keys on this priority queue
        :rtype: int

        """
        return self._n

    def __len__(self) -> int:
        return self.size()

    def key_of(self, i: int) -> Key:
        """Returns the key associated with index i.

        :param i: the index of the key to return
        :return: the key associated with index i
        :raises IllegalArgumentException: unless 0 <= i < max_n
        :raises NoSuchElementException: if no key is associated with index i

        """
        if i < 0 or i >= self._max_n:
            raise IllegalArgumentException("index is out of range")
        if not self.contains(i):
            raise IllegalArgumentException("index is not on the priority queue")
        key = self._keys[i]
        assert key is not None
        return key

    def _exch(self, i: int, j: int) -> None:
        """Exchanges the position of items at index i and j on the heap.

        :param i: index of the first item
        :param j: index of the second item

        """
        self._pq[i], self._pq[j] = self._pq[j], self._pq[i]
        self._qp[self._pq[i]] = i
        self._qp[self._pq[j]] = j

    def _greater(self, i: int, j: int) -> bool:
        """Returns True if key at index i on the heap is greater than key at
        index j.

        :param i: index of the first item
        :param j: index of the second item
        :return: True if key at index i on the heap is greater than key at index j
        :rtype: bool

        """
        return self._keys[self._pq[i]] > self._keys[self._pq[j]]

    def _swim(self, k: int) -> None:
        """Moves item at index k up to a legal position on the heap.

        :param k: Index of the item on the heap to be moved

        """
        while k > 1 and self._greater(k // 2, k):
            self._exch(k, k // 2)
            k = k // 2

    def _sink(self, k: int) -> None:
        """Moves item at index k down to a legal position on the heap.

        :param k: Index of the item on the heap to be moved

        """
        while 2 * k <= self._n:
            j = 2 * k
            if j < self._n and self._greater(j, j + 1):
                j += 1
            if not self._greater(k, j):
                break
            self._exch(k, j)
            k = j

    def __iter__(self) -> Iterator[int]:
        """Iterates over all the items in this priority queue in ascending
        order."""
        copy: IndexMinPQ[Key] = IndexMinPQ(len(self._pq) - 1)
        for i in range(1, self._n + 1):
            key = self._keys[self._pq[i]]
            assert key is not None
            copy.insert(self._pq[i], key)
        while not copy.is_empty():
            yield copy.del_min()


def main():
    """Inserts a bunch of strings to an indexed priority queue, deletes and
    prints them, inserts them again, and prints them using an iterator."""
    strings = ["it", "was", "the", "best", "of", "times", "it", "was", "the", "worst"]
    pq = IndexMinPQ(len(strings))
    for i in range(len(strings)):
        pq.insert(i, strings[i])
    while not pq.is_empty():
        i = pq.del_min()
        print("{} {}".format(i, strings[i]))
    print()
    for i in range(len(strings)):
        pq.insert(i, strings[i])
    for i in pq:
        print("{} {}".format(i, strings[i]))
    while not pq.is_empty():
        pq.del_min()


if __name__ == "__main__":
    main()
