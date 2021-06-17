import itertools

from a import A
from main import create_game, Player, place, index_to_position, history_to_state, determine_result, Result, next_player
from solve_tic_tac_toe import create_tic_tac_toe_solving_tree, determine_optimal_move_for_player_two
import pickle


# tree = create_tic_tac_toe_solving_tree()
with open('solving_tree.pickle', 'rb') as file:
    tree = pickle.load(file)


class Environment:
    def __init__(self):
        self.tree = tree
        self.state = create_game()
        self.player = Player.One
        self.node = self.tree.root

    def do_action(self, action):
        if self.is_done():
            raise AssertionError(
                '"do_action" was called when environment was done. ' +
                'Please make sure to reset the environment first.'
            )
        index = action
        position = index_to_position(action)
        self.state = place(self.state, position, self.player)
        self.node = next(node for node in self.node.children if node.value[-1] == index)
        self.player = next_player(self.player)
        if not self.is_done():
            self.node = determine_optimal_move_for_player_two(self.node)
            index = self.node.value[-1]
            position = index_to_position(index)
            self.state = place(self.state, position, self.player)
            self.player = next_player(self.player)

    def reset(self):
        self.node = self.tree.root
        self.state = create_game()
        self.player = Player.One

    def is_done(self):
        return len(self.node.children) == 0

    def get_available_actions(self):
        return set(node.value[-1] for node in self.node.children)

    def get_state(self):
        return history_to_state(self.node.value)


class Database:
    def __init__(self):
        self.state_to_explored_actions = dict()
        self.state_and_action_to_state = dict()
        self.state_to_state_and_action_pairs_that_lead_to_it = dict()
        self.state_to_unexplored_actions_count = dict()

    def store(self, state_before_action, action, state_after_action):
        state_before_action = tuple(state_before_action)
        state_after_action = tuple(state_after_action)
        if state_before_action not in self.state_to_explored_actions:
            self.state_to_explored_actions[state_before_action] = set()
        self.state_to_explored_actions[state_before_action].add(action)

        self.state_and_action_to_state[(state_before_action, action)] = \
            state_after_action

        if state_after_action not in self.state_to_state_and_action_pairs_that_lead_to_it:
            self.state_to_state_and_action_pairs_that_lead_to_it[state_after_action] = set()
        self.state_to_state_and_action_pairs_that_lead_to_it[state_after_action].add(
            (state_before_action, action)
        )

    def query_explored_actions(self, state):
        state = tuple(state)
        return self.state_to_explored_actions[state] if state in self.state_to_explored_actions else set()

    def query_action_that_lead_to_state_with_highest_metric_value(self, state, determine_metric_value):
        state = tuple(state)
        explored_actions = self.state_to_explored_actions[state]
        return max(
            determine_metric_value(self.state_and_action_to_state[(state, action)])
            for action
            in explored_actions
        )

    def query_state_with_highest_metric_value(self, determine_metric_value):
        return max(self.state_and_action_to_state.values(), key=lambda state: determine_metric_value(state))

    def query_state_and_action_pairs_which_lead_to_state(self, state):
        state = tuple(state)
        return (
            self.state_to_state_and_action_pairs_that_lead_to_it[state]
            if state in self.state_to_state_and_action_pairs_that_lead_to_it
            else set()
        )

    def store_unexplored_actions_count(self, state, unexplored_actions_count):
        state = tuple(state)
        self.state_to_unexplored_actions_count[state] = unexplored_actions_count

    def query_total_known_unexplored_actions_count(self, state):
        visited_states = set()
        state = tuple(state)
        count = 0
        states = [state]
        while len(states) >= 1:
            next_states = []
            for state in states:
                if state not in visited_states:
                    unexplored_actions_count = self.query_unexplored_actions_count(state)
                    if unexplored_actions_count is not None:
                        count += unexplored_actions_count
                    if state in self.state_to_explored_actions:
                        actions = self.state_to_explored_actions[state]
                        next_states += [self.state_and_action_to_state[(state, action)] for action in actions]
                    visited_states.add(state)
            states = next_states
        return count

    def query_unexplored_actions_count(self, state):
        return (
            self.state_to_unexplored_actions_count[state]
            if state in self.state_to_unexplored_actions_count
            else None
        )

    def query_state(self, state, action):
        state = tuple(state)
        state_and_action_pair = (state, action)
        return (
            self.state_and_action_to_state[state_and_action_pair]
            if state_and_action_pair in self.state_and_action_to_state
            else None
        )


state_to_metric_value = dict()
nodes = [tree.root]
while len(nodes) >= 1:
    children = []
    for node in nodes:
        state = tuple(history_to_state(node.value))
        result = determine_result(state)
        metric_value = 1.0 if result == Result.PlayerOneWon else 0.5 if result == Result.Draw else 0.0
        state_to_metric_value[state] = metric_value
        children += node.children
    nodes = children


def determine_metric_value(state):
    return state_to_metric_value[state]


environment = Environment()
database = Database()
a = A()
a.explore(environment, database, 1000)
print('explored states: ' + str(len(database.state_to_explored_actions)) + ' of ' + str(len(state_to_metric_value)))

environment.reset()
path_to_outcome = a.evaluate(environment, database, determine_metric_value)
print(path_to_outcome)
