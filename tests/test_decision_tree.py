import unittest
from collections import namedtuple

from decision import Tree, Leaf, Node


class TestDecisionTree(unittest.TestCase):

    def test_when_tree_is_a_leaf_then_it_returns_the_results_independently_from_the_variables(self):
        node = Leaf(value=1)
        tree = Tree(root=node)

        result = tree.decide(())
        self.assertEqual(1, result)

    def test_when_tree_has_a_decision_node_then_it_returns_the_right_value(self):
        leaf_true = Leaf(value=10)
        leaf_false = Leaf(value=20)
        root = Node(node_true=leaf_true, node_false=leaf_false, decision=lambda v: v.something)
        tree = Tree(root=root)

        Vars = namedtuple('Vars', 'something')

        result = tree.decide(Vars(True))
        self.assertEqual(10, result)

        result = tree.decide(Vars(False))
        self.assertEqual(20, result)

    def test_when_tree_has_multiple_levels_then_it_returns_the_right_value(self):
        # root ---> (t) leaf_a [10]
        #       \-> (f) node ---> (t) leaf_b [20]
        #                     \-> (f) leaf_c [30]
        leaf_a = Leaf(value=10)
        leaf_b = Leaf(value=20)
        leaf_c = Leaf(value=30)
        node = Node(node_true=leaf_b, node_false=leaf_c, decision=lambda v: v.second_decision)
        root = Node(node_true=leaf_a, node_false=node, decision=lambda v: v.first_decision)

        tree = Tree(root=root)

        Vars = namedtuple('Vars', 'first_decision, second_decision')

        result = tree.decide(Vars(True, True))
        self.assertEqual(10, result)

        result = tree.decide(Vars(True, False))
        self.assertEqual(10, result)

        result = tree.decide(Vars(False, True))
        self.assertEqual(20, result)

        result = tree.decide(Vars(False, False))
        self.assertEqual(30, result)

    def test_when_creating_from_dict_then_it_returns_the_right_value(self):
        # root ---> (t) leaf_a [10]
        #       \-> (f) node ---> (t) leaf_b [20]
        #                     \-> (f) leaf_c [30]
        tree_dict = {
            'decision': lambda v: v.first_decision,
            'node_true': 10,
            'node_false': {
                'decision': lambda v: v.second_decision,
                'node_true': 20,
                'node_false': 30,
            },
        }
        tree = Tree.from_dict(tree_dict)

        Vars = namedtuple('Vars', 'first_decision, second_decision')

        result = tree.decide(Vars(True, True))
        self.assertEqual(10, result)

        result = tree.decide(Vars(True, False))
        self.assertEqual(10, result)

        result = tree.decide(Vars(False, True))
        self.assertEqual(20, result)

        result = tree.decide(Vars(False, False))
        self.assertEqual(30, result)

    def test_when_creating_a_10_depth_tree_then_it_does_not_break(self):
        tree_dict = {
            'decision': lambda v: True,
            'node_true': {
                'decision': lambda v: True,
                'node_true': {
                    'decision': lambda v: True,
                    'node_true': {
                        'decision': lambda v: True,
                        'node_true': {
                            'decision': lambda v: True,
                            'node_true': {
                                'decision': lambda v: True,
                                'node_true': {
                                    'decision': lambda v: True,
                                    'node_true': {
                                        'decision': lambda v: True,
                                        'node_true': {
                                            'decision': lambda v: True,
                                            'node_true': {
                                                'decision': lambda v: True,
                                                'node_true': 100,
                                                'node_false': 10,
                                            },
                                            'node_false': 9,
                                        },
                                        'node_false': 8,
                                    },
                                    'node_false': 7,
                                },
                                'node_false': 6,
                            },
                            'node_false': 5,
                        },
                        'node_false': 4,
                    },
                    'node_false': 3,
                },
                'node_false': 2,
            },
            'node_false': 1,
        }
        tree = Tree.from_dict(tree_dict)

        result = tree.decide(())
        self.assertEqual(100, result)
