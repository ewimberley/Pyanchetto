import sys
import pickle
import shelve

from chess import *
from ai.ai_player import *
from ai.material_heuristic import *

def main(args):
    #move_dict = pickle.load(open('ai/2000elo.dict', "rb"))
    move_dict = shelve.open('ai/2000elo.dict', flag='r')
    white = AIPlayer(WHITE, MaterialHeuristic(), move_dict)
    black = AIPlayer(BLACK, MaterialHeuristic(), move_dict)
    board = Chess(white_agent=white, black_agent=black)
    state = board.game_state()
    print(board)
    while state == NORMAL or state == CHECK:
        board.agent_move()
        print(board)
    move_dict.close()

if __name__ == '__main__':
    main(sys.argv)