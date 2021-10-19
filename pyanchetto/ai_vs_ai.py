import sys

from chess import *
from ai.ai_player import *
from ai.material_heuristic import *

def main(args):
    white = AIPlayer(WHITE, MaterialHeuristic())
    black = AIPlayer(BLACK, MaterialHeuristic())
    board = Chess(white_agent=white, black_agent=black)
    state = board.game_state()
    print(board)
    while state == NORMAL or state == CHECK:
        board.agent_move()
        print(board)

if __name__ == '__main__':
    main(sys.argv)