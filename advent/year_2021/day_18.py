"""
"""

from __future__ import annotations

from advent.tools import *


def _sum(lines):
    prev = lines[0]
    for line in lines[1:]:
        prev = [prev, line]
    return prev


@dc.dataclass
class Node:
    depth: int
    val: t.Optional[int | t.List[int]] = None
    left: t.Optional[Node] = None
    right: t.Optional[Node] = None
    parent: t.Optional[Node] = None

    def _root(self):
        root = self
        while root.parent:
            root = root.parent
        return root

    def _inorder_successor(self):
        p = self.parent
        n = self
        if n.right is not None:
            return self._min(n.right)
        while p is not None:
            if n != p.right:
                break
            n = p
            p = p.parent
        return p

    def _inorder_predecessor(self):
        p = self.parent
        n = self
        if n.left is not None:
            return self._max(n.left)
        while p is not None:
            if n != p.left:
                break
            n = p
            p = p.parent
        return p

    def _min(self, node):
        cur = node
        while cur is not None:
            if cur.left is None:
                break
            cur = cur.left
        return cur

    def _max(self, node):
        cur = node
        while cur is not None:
            if cur.right is None:
                break
            cur = cur.right
        return cur

    def explode(self):
        if isinstance(self.val, int):
            return
        if (
            isinstance(self.left.val, int)
            and isinstance(self.right.val, int)
            and self.depth >= 4
        ):
            if node := self.right._inorder_successor():
                self._min(node.right).val += self.right.val
            if node := self.left._inorder_predecessor():
                self._max(node.left).val += self.left.val
            self.val = 0
            self.right = self.left = None
            return True
        return self.left.explode() or self.right.explode()

    def split(self):
        if not isinstance(self.val, int):
            return self.left.split() or self.right.split()
        if self.val < 10:
            return
        val = self.val
        self.val = None
        l, r = _split(val)
        self.left = Node(val=l, depth=self.depth + 1, parent=self)
        self.right = Node(val=r, depth=self.depth + 1, parent=self)
        print("split")
        return True


def _split(val):
    return [val // 2, math.ceil(val / 2)]


def _parse(pair, depth=0, parent=None):
    node = Node(depth=depth, parent=parent)
    if isinstance(pair, int):
        node.val = pair
        return node
    left = _parse(pair[0], depth + 1, node)
    right = _parse(pair[1], depth + 1, node)
    node.left = left
    node.right = right
    return node


def _dumps(node):
    if isinstance(node.val, int):
        return node.val
    return [_dumps(node.left), _dumps(node.right)]


def _pt1(lines):
    expr = _sum(lines)
    node = _parse(expr)
    for _ in range(2):
        if not (node.explode() or node.split()):
            break
    if 0:
        ppbtree.print_tree(
            node,
            nameattr="val",
            last="updown",
            left_child="right",
            right_child="left",
        )
    return _dumps(node)


def _pt2(lines):
    pass


TEST = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
"""
# [[[[1, 1], [2, 2]], [3, 3]], [4, 4]]
TEST2 = """[1,1]
[2,2]
[3,3]
[4,4]
"""
TEST3 = """[[[[[9,8],1],2],3],4]
"""
TEST4 = """[7,[6,[5,[4,[3,2]]]]]
"""
TEST5 = """[[6,[5,[4,[3,2]]]],1]
"""
TEST6 = """[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]
"""
TEST7 = """[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]
"""
TEST8 = """[[[[0,7],4],[15,[0,13]]],[1,1]]
"""
# step 2 of hw assignment
TEST9 = """[[[[[[[[[[[[0, [[9, 7], [9, 6]]], [[4, [1, 2]], [[1, 4], 2]]], [[[5, [2, 8]], 4], [5, [[9, 9], 0]]]], [6, [[[6, 2], [5, 6]], [[7, 6], [4, 7]]]]], [[[6, [0, 7]], [0, 9]], [4, [9, [9, 0]]]]], [[[7, [6, 4]], [3, [1, 3]]], [[[5, 5], 1], 9]]], [[6, [[7, 3], [3, 2]]], [[[3, 8], [5, 7]], 4]]], [[[[5, 4], [7, 7]], 8], [[8, 3], 8]]], [[9, 3], [[9, 9], [6, [4, 9]]]]], [[2, [[7, 7], 7]], [[5, 8], [[9, 3], [0, 2]]]]], [[[[5, 2], 5], [8, [3, 7]]], [[5, [7, 5]], [4, 4]]]]]
"""
ANSWERS = None


def main():
    assert _split(13) == [6, 7]
    assert _split(15) == [7, 8]

    return afs.input_lines(
        tests=[TEST9],
        parts=[_pt1],
        run_input=False,
        transform_line=eval,
    )
