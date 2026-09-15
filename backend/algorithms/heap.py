"""Max-heap priority queue for scholarship applicants."""


class MaxHeap:
    """A max heap ordered by applicant priority score."""

    def __init__(self) -> None:
        self._items: list[dict] = []

    @staticmethod
    def _higher_priority(a: dict, b: dict) -> bool:
        a_key = (a.get("priority_score", 0), a.get("need_score", 0))
        b_key = (b.get("priority_score", 0), b.get("need_score", 0))
        return a_key > b_key

    def push(self, applicant: dict) -> None:
        self._items.append(applicant)
        self._sift_up(len(self._items) - 1)

    def pop(self) -> dict:
        if not self._items:
            raise IndexError("Cannot pop from an empty heap")

        root = self._items[0]
        last = self._items.pop()
        if self._items:
            self._items[0] = last
            self._sift_down(0)
        return root

    def peek(self) -> dict:
        if not self._items:
            raise IndexError("Cannot peek at an empty heap")
        return self._items[0]

    def __len__(self) -> int:
        return len(self._items)

    def _sift_up(self, index: int) -> None:
        while index > 0:
            parent = (index - 1) // 2
            if not self._higher_priority(self._items[index], self._items[parent]):
                break
            self._items[index], self._items[parent] = (
                self._items[parent],
                self._items[index],
            )
            index = parent

    def _sift_down(self, index: int) -> None:
        size = len(self._items)
        while True:
            left = 2 * index + 1
            right = left + 1
            largest = index

            if left < size and self._higher_priority(self._items[left], self._items[largest]):
                largest = left
            if right < size and self._higher_priority(self._items[right], self._items[largest]):
                largest = right

            if largest == index:
                break

            self._items[index], self._items[largest] = (
                self._items[largest],
                self._items[index],
            )
            index = largest
