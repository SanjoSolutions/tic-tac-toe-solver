from enum import IntEnum

# state: 9-tuple
# 0 1 2
# 3 4 5
# 6 7 8
#
# (0, 1, 2, 3, 4, 5, 6, 7, 8)
#
# history:
# Tuple of indexes where the player has put their token.
# Player 1 starts with the first play.

BOARD_WIDTH = 3
BOARD_HEIGHT = 3
BOARD_SIZE = BOARD_WIDTH * BOARD_HEIGHT
MAX_NUMBER_OF_TURNS = BOARD_SIZE


class Player(IntEnum):
    One = 1
    Two = 2


class Result(IntEnum):
    Draw = 0
    PlayerOneWon = 1
    PlayerTwoWon = 2


def create_game():
    return [0] * 9


def place(state, position, player):
    state = state[:]
    state[position_to_index(position)] = player
    return state


def position_to_index(position):
    return (position[0] - 1) * BOARD_WIDTH + (position[1] - 1)


def index_to_position(index):
    return (
        (index // BOARD_WIDTH) + 1,
        (index % BOARD_WIDTH) + 1
    )


def history_to_state(history):
    state = create_game()
    player = Player.One
    for index in history:
        state[index] = player
        player = next_player(player)
    return state


def next_player(player):
    return Player((player % len(Player)) + 1)


def has_won(state, player):
    return (
        is_player_token_in_positions(state, player, ((1, 1), (1, 2), (1, 3))) or
        is_player_token_in_positions(state, player, ((2, 1), (2, 2), (2, 3))) or
        is_player_token_in_positions(state, player, ((3, 1), (3, 2), (3, 3))) or
        is_player_token_in_positions(state, player, ((1, 1), (2, 1), (3, 1))) or
        is_player_token_in_positions(state, player, ((1, 2), (2, 2), (3, 2))) or
        is_player_token_in_positions(state, player, ((1, 3), (2, 3), (3, 3))) or
        is_player_token_in_positions(state, player, ((1, 1), (2, 2), (3, 3))) or
        is_player_token_in_positions(state, player, ((1, 3), (2, 2), (3, 1)))
    )


def is_player_token_in_positions(state, player, positions):
    return all(is_player_token_in_position(state, player, position) for position in positions)


def is_player_token_in_position(state, player, position):
    return state[position_to_index(position)] == player


def is_board_full(state):
    return all([value != 0 for value in state])


def determine_result(state):
    if has_won(state, Player.One):
        return Result.PlayerOneWon
    elif has_won(state, Player.Two):
        return Result.PlayerTwoWon
    elif is_board_full(state):
        return Result.Draw
    else:
        return None


def play_game(choose):
    player = Player.One
    history = []
    state = create_game()
    result = determine_result(state)
    while result is None:
        position = choose[int(player) - 1](history, state)
        index = position_to_index(position)
        history.append(index)
        state = place(state, position, player)
        result = determine_result(state)
        player = next_player(player)
    return history, state, result
