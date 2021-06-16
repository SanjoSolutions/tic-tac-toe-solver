from main import play_game, index_to_position
from solve_tic_tac_toe import create_tic_tac_toe_solving_tree, determine_optimal_move_for_player_one, \
    determine_optimal_move_for_player_two

tree = create_tic_tac_toe_solving_tree()
node = tree.root


def choose_next_move(history, state):
    global node
    if len(history) % 2 == 0:
        node = determine_optimal_move_for_player_one(node)
    else:
        node = determine_optimal_move_for_player_two(node)
    return index_to_position(node.value[-1])


choose = [
    choose_next_move,
    choose_next_move
]

history, state, result = play_game(choose)
print('Result:', result)
print('History:', history)
