class ListNode[T]:
    def __init__(self, data: T, next: "ListNode[T] | None" = None):
        self.data = data
        self.next = next

    def __eq__(self, other: object) -> bool:
        # Production code requires isinstance checks for __eq__
        if not isinstance(other, ListNode):
            return False

        a: ListNode[T] | None = self
        b: ListNode[T] | None = other

        while a and b:
            if a.data != b.data:
                return False
            a, b = a.next, b.next

        return a is None and b is None

    def __repr__(self) -> str:
        node: ListNode[T] | None = self
        visited: set[int] = set()
        first = True
        result = ''

        while node:
            if first:
                first = False
            else:
                result += ' -> '

            # Cycle detection
            if id(node) in visited:
                if node.next is not node:
                    result += str(node.data)
                    result += ' -> ... -> '
                result += str(node.data)
                result += ' -> ...'
                break
            else:
                result += str(node.data)
                visited.add(id(node))

            node = node.next

        return result

    def __str__(self) -> str:
        return self.__repr__()


def list_size[T](node: ListNode[T] | None) -> int:
    result = 0
    visited: set[int] = set()

    while node is not None and id(node) not in visited:
        result += 1
        visited.add(id(node))
        node = node.next

    return result
