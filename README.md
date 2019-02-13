# Decision Tree

Basic but flexible binary decision tree. Uses Python3.6


## Usage

The tree will evaluate the decision functions for each node until it reaches a leave to return its value, each decision function is expected to receive a namedtuple and return a boolean value.

```
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

tree.decide(Vars(False, True))
> 20
```

The tree can also be created manually connecting nodes and leaves. This tree is equivalent to the previous one:

```
leaf_a = Leaf(value=10)
leaf_b = Leaf(value=20)
leaf_c = Leaf(value=30)
node = Node(node_true=leaf_b, node_false=leaf_c, decision=lambda v: v.second_decision)
root = Node(node_true=leaf_a, node_false=node, decision=lambda v: v.first_decision)

tree = Tree(root=root)
Vars = namedtuple('Vars', 'first_decision, second_decision')

tree.decide(Vars(False, True))
> 20
```


## Warning

The tree uses recursion to decide and also when it is created from a dict. A tall tree might reach the recursion limit.
