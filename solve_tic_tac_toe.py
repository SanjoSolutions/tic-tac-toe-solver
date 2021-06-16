from generate_tic_tac_toe_tree import generate_tic_tac_toe_tree
from main import history_to_state, determine_result, Result


def create_tic_tac_toe_solving_tree():
    tree = generate_tic_tac_toe_tree()
    calculate_percentages_of_loose_outcomes_recursion(tree.root)
    return tree


def calculate_percentages_of_loose_outcomes_recursion(node):
    history = node.value
    state = history_to_state(history)
    result = determine_result(state)
    if result is not None:
        percentage_of_loose_outcomes_for_player_one = 1.0 if result == Result.PlayerTwoWon else 0.0
        percentage_of_loose_outcomes_for_player_two = 1.0 if result == Result.PlayerOneWon else 0.0
        node.percentage_of_loose_outcomes_for_player_one = percentage_of_loose_outcomes_for_player_one
        node.percentage_of_loose_outcomes_for_player_two = percentage_of_loose_outcomes_for_player_two
        return percentage_of_loose_outcomes_for_player_one, percentage_of_loose_outcomes_for_player_two
    else:
        percentages_of_loose_outcomes_for_player_one = []
        percentages_of_loose_outcomes_for_player_two = []
        for child in node.children:
            percentage_of_loose_outcomes_for_player_one, percentage_of_loose_outcomes_for_player_two = \
                calculate_percentages_of_loose_outcomes_recursion(child)
            percentages_of_loose_outcomes_for_player_one.append(percentage_of_loose_outcomes_for_player_one)
            percentages_of_loose_outcomes_for_player_two.append(percentage_of_loose_outcomes_for_player_two)
        percentage_of_loose_outcomes_for_player_one = sum(percentages_of_loose_outcomes_for_player_one) / \
            float(len(percentages_of_loose_outcomes_for_player_one))
        percentage_of_loose_outcomes_for_player_two = sum(percentages_of_loose_outcomes_for_player_two) / \
            float(len(percentages_of_loose_outcomes_for_player_two))
        node.percentage_of_loose_outcomes_for_player_one = percentage_of_loose_outcomes_for_player_one
        node.percentage_of_loose_outcomes_for_player_two = percentage_of_loose_outcomes_for_player_two
        return percentage_of_loose_outcomes_for_player_one, percentage_of_loose_outcomes_for_player_two


def determine_optimal_move_for_player_one(node):
    return find_child_node_with_lowest_percentage_of_loose_outcomes(node, determine_percentage_of_loose_outcomes_for_player_one)


def determine_optimal_move_for_player_two(node):
    return find_child_node_with_lowest_percentage_of_loose_outcomes(node, determine_percentage_of_loose_outcomes_for_player_two)


def find_child_node_with_lowest_percentage_of_loose_outcomes(node, get_chance_to_loose):
    return find_node_with_lowest_percentage_of_loose_outcomes(node.children, get_chance_to_loose)


def find_node_with_lowest_percentage_of_loose_outcomes(nodes, get_chance_to_loose):
    return min(nodes, key=get_chance_to_loose)


def determine_percentage_of_loose_outcomes_for_player_one(node):
    return node.percentage_of_loose_outcomes_for_player_one


def determine_percentage_of_loose_outcomes_for_player_two(node):
    return node.percentage_of_loose_outcomes_for_player_two
