import sys
from multiprocessing import Process, Queue

from pyanchetto.chess import Chess, NORMAL, CHECK, CHECKMATE, STALEMATE
from pyanchetto.move_tree import MoveTree

#correct[depth] = (nodes, captures, eps, castles, promotions, chks, discovery chks, double chks, chkmates)
correct = {}
correct[0] = (1, 0, 0, 0, 0, 0, 0, 0, 0)
correct[1] = (20, 0, 0, 0, 0, 0, 0, 0, 0)
correct[2] = (400, 0, 0, 0, 0, 0, 0, 0, 0)
correct[3] = (8902, 34, 0, 0, 0, 12, 0, 0, 0)
correct[4] = (197281, 1576, 0, 0, 0, 469, 0, 0, 8)
correct[5] = (4865609, 82719, 258, 0, 0, 27351, 6, 0, 347)


def perft(root, branch, board, depth, max_depth, child_processes=False, queue=None):
    branch.game_state = board.game_state()
    if len(board.move_list)-1 in board.captured_pieces:
        branch.capture = True
    if depth < max_depth:
        piece_moves = board.valid_moves()
        moves = []
        for piece in piece_moves:
            for move in piece_moves[piece]:
                moves.append((piece, move))
        children = branch.children
        processes = []
        queues = []
        for move in moves:
            clone = Chess(board)
            clone.move(move[0], move[1])
            child = MoveTree(move)
            if child_processes:
                q = Queue()
                p = Process(target=perft, args=(root, child, clone, depth + 1, max_depth, False, q))
                p.start()
                processes.append(p)
                queues.append(q)
            else:
                branch.children.append(child)
                perft(root, child, clone, depth + 1, max_depth, False)
        for i, p in enumerate(processes):
            filled_branch = queues[i].get()
            #for child in filled_branch.children:
            branch.children.append(filled_branch)
            p.join()
        if queue is not None:
            queue.put(branch)
        else:
            return branch


def validate(root, max_depth):
    valid = True
    visiting = [root]
    perft = {}
    for depth in range(max_depth + 1):
        perft[depth] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        to_visit = []
        for node in visiting:
            to_visit.extend(node.children)
            perft[depth][0] += 1
            if node.game_state == CHECK:
                perft[depth][5] += 1
            elif node.game_state == CHECKMATE:
                perft[depth][8] += 1
                perft[depth][5] += 1
            if node.capture:
                perft[depth][1] += 1
        visiting = to_visit
    print(perft)
    return valid


def main():
    print("*"*50)
    print("Pyanchetto Perft Validator.")
    print("*"*50)
    depth = int(sys.argv[1])
    threads = 1

    board = Chess()
    root = MoveTree("Root")
    perft(root, root, board, 0, depth, True)
    valid = validate(root, depth)
    print(valid)
    #print(root.prettyPrint())
    print(root.count_nodes())

if __name__ == "__main__":
    main()