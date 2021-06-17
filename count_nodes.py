import itertools


def count_nodes(tree):
    count = 0
    nodes = [tree.root]
    while len(nodes) >= 1:
        count += len(nodes)
        nodes = list(itertools.chain.from_iterable(node.children for node in nodes))
    return count
