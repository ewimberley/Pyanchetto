import sys
import shelve

from ai.ai_player import *
from ai.heuristics.material_heuristic import *
from ai.priority_heuristics.piece_priority_heuristic import *
from ai.priority_heuristics.dict_priority_heuristic import *
from ai.ensemble_priority_heuristic import *
from ai.ensemble_heuristic import *
from ai.heuristics.misc_heuristic import *

def main(args):
    #move_dict = pickle.load(open('ai/2000elo.dict', "rb"))
    move_dict = shelve.open('ai/2000elo.dict', flag='r')
    priority = EnsemblePriorityHeuristic([PiecePriorityHeuristic(), DictPriorityHeuristic(move_dict)], [0.8, 0.2])
    heuristic = EnsembleHeuristic([MaterialHeuristic(), MiscHeuristic()], [0.9, 0.1])
    white = AIPlayer(WHITE, heuristic, priority, move_dict)
    black = AIPlayer(BLACK, heuristic, priority, move_dict)
    board = Chess(white_agent=white, black_agent=black)
    state = board.game_state()
    print(board)
    while state == NORMAL or state == CHECK:
        board.agent_move()
        print(board)
    move_dict.close()

if __name__ == '__main__':
    main(sys.argv)