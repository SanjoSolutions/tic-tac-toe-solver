import pickle
from solve_tic_tac_toe import create_tic_tac_toe_solving_tree

tree = create_tic_tac_toe_solving_tree()
with open('solving_tree.pickle', 'wb') as file:
    pickle.dump(tree, file, pickle.HIGHEST_PROTOCOL)
