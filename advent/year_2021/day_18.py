"""
"""

from __future__ import annotations
from uuid import uuid4

from advent.tools import *


@dc.dataclass
class Node:
    depth: int
    node_id: str = dc.field(default_factory=lambda: str(uuid4()))
    val: t.Optional[int | t.List[int]] = None
    left: t.Optional[Node] = None
    right: t.Optional[Node] = None
    parent: t.Optional[Node] = None

    def __eq__(self, other):
        return self.node_id == other.node_id

    def magnitude(self):
        if self.is_leaf:
            return self.val
        return self.left.magnitude() * 3 + self.right.magnitude() * 2

    @property
    def is_leaf(self):
        return isinstance(self.val, int)

    def _successor_leaf(self):
        p = self.parent
        s = self
        while p and ((s == p.right) or (not p.right and s == p.left)):
            p, s = p.parent, s.parent
        if not p:
            return
        s = p.right or p.left
        while not isinstance(s.val, int):
            s = s.left or s.right
        return s

    def _predecessor_leaf(self):
        p = self.parent
        s = self
        while p and ((s == p.left) or (not p.left and s == p.right)):
            p, s = p.parent, s.parent
        if not p:
            return
        s = p.left or p.right
        while not s.is_leaf:
            s = s.right or s.left
        return s

    def explode(self):
        if isinstance(self.val, int):
            return
        if self.left.is_leaf and self.right.is_leaf and self.depth >= 4:
            if node := self._successor_leaf():
                node.val += self.right.val
            if node := self._predecessor_leaf():
                node.val += self.left.val
            self.val = 0
            self.right = self.left = None
            return True
        return self.left.explode() or self.right.explode()

    def split(self):
        if not self.is_leaf:
            return self.left.split() or self.right.split()
        if self.val < 10:
            return
        val = self.val
        self.val = None
        l, r = _split(val)
        self.left = Node(val=l, depth=self.depth + 1, parent=self)
        self.right = Node(val=r, depth=self.depth + 1, parent=self)
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
    if node.is_leaf:
        return node.val
    return [_dumps(node.left), _dumps(node.right)]


def _pp(node):
    ppbtree.print_tree(
        node,
        nameattr="val",
        last="updown",
        left_child="right",
        right_child="left",
    )


def _pt1(lines):
    prev = lines[0]
    for expr in lines[1:]:
        node = Node(depth=0)
        l = _parse(prev, depth=node.depth + 1, parent=node)
        r = _parse(expr, depth=node.depth + 1, parent=node)
        node.left, node.right = l, r
        while True:
            if not (node.explode() or node.split()):
                prev = _dumps(node)
                break
    return node.magnitude()


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
TEST2 = """[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
[6,6]
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
TEST10 = """[[[[4,3],4],4],[7,[[8,4],9]]]
[1,1]
"""
TEST11 = """[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]
"""
TEST12 = """[[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]
[[[[4,2],2],6],[8,7]]
"""
ANSWERS = None


def main():
    assert _split(13) == [6, 7]
    assert _split(15) == [7, 8]

    return afs.input_lines(
        tests=[TEST],
        parts=[_pt1],
        run_input=True,
        transform_line=eval,
    )
