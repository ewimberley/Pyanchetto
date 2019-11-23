import sys
from multiprocessing import Pool
from functools import partial

from deepfianchetto.chess import Chess
from deepfianchetto.move_tree import MoveTree

#correct[depth] = (nodes, captures, eps, castles, promotions, chks, discovery chks, double chks, chkmates)
correct = {}
correct[0] = (1, 0, 0, 0, 0, 0, 0, 0, 0)
correct[1] = (20, 0, 0, 0, 0, 0, 0, 0, 0)
correct[2] = (400, 0, 0, 0, 0, 0, 0, 0, 0)
correct[3] = (8902, 34, 0, 0, 0, 12, 0, 0, 0)
correct[4] = (197281, 1576, 0, 0, 0, 469, 0, 0, 8)
correct[5] = (4865609, 82719, 258, 0, 0, 27351, 6, 0, 347)

def perft(root, branch, board, depth, max_depth):
    if depth > max_depth:
        return
    moves = board.valid_moves()
    branch.add_moves(moves)
    for child in branch.children:
        clone = Chess(board)
        clone.move(child.move[0], child.move[1])
        perft(root, child, clone, depth + 1, max_depth)

def validate(root, depth, max_depth):
    valid = True

    if root.count_nodes() != correct[depth][0]:
        print("Wrong number of nodes at depth: " + str(depth))
        valid = False
    return valid

def main():
    print("*"*50)
    print("Deep Fianchetto Perft Validator.")
    print("*"*50)
    depth = int(sys.argv[1])

    board = Chess()
    root = MoveTree("Root")
    perft(root, root, board, 1, depth)
    valid = validate(root, 1, depth)
    print(valid)
    print(root.prettyPrint())
    print(root.count_nodes())

if __name__ == "__main__":
    main()