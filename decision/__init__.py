import abc
from typing import Any, Callable, NamedTuple


class INode(metaclass=abc.ABCMeta):
    """Tree node interface."""

    @abc.abstractmethod
    def decide(self, variables: NamedTuple) -> Any:
        pass


class Leaf(INode):
    """Leaf for a tree."""

    def __init__(self, value: Any) -> None:
        self._value = value

    def decide(self, variables: NamedTuple) -> Any:
        return self._value


class Node(INode):
    """Decision node for a tree."""

    def __init__(self, node_true: INode, node_false: INode, decision: Callable[[NamedTuple], bool]) -> None:
        self._node_true = node_true
        self._node_false = node_false
        self._decision = decision

    def decide(self, variables: NamedTuple) -> Any:
        if self._decision(variables):
            return self._node_true.decide(variables)
        else:
            return self._node_false.decide(variables)


class Tree:
    """Binary decision tree."""

    def __init__(self, root: INode) -> None:
        self._root = root

    @classmethod
    def from_dict(cls, tree_dict) -> 'Tree':
        root = cls._node_from_data(tree_dict)
        return Tree(root)

    def decide(self, variables: NamedTuple) -> Any:
        return self._root.decide(variables)

    @classmethod
    def _node_from_data(cls, data: Any) -> INode:
        if (
            isinstance(data, dict) and
            'decision' in data and
            'node_true' in data and
            'node_false' in data
        ):
            node_true = cls._node_from_data(data['node_true'])
            node_false = cls._node_from_data(data['node_false'])
            return Node(node_true, node_false, data['decision'])
        else:
            return Leaf(data)

