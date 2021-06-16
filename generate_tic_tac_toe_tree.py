from main import history_to_state, has_won, Player, BOARD_SIZE
from tree import Tree, Node


def generate_tic_tac_toe_tree():
    tree = Tree()
    tree.root = Node([])
    all_empty_fields = set(range(BOARD_SIZE))
    nodes = [tree.root]
    while len(nodes) >= 1:
        next_nodes = []
        for node in nodes:
            empty_fields = all_empty_fields - set(node.value)
            for empty_field in empty_fields:
                history = node.value + [empty_field]
                child = Node(history)
                node.children.append(child)
                if not has_someone_won(history):
                    next_nodes.append(child)
        nodes = next_nodes
    return tree


def has_someone_won(history):
    state = history_to_state(history)
    return has_won(state, Player.One) or has_won(state, Player.Two)
