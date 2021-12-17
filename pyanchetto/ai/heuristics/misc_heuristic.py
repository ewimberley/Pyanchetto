from pyanchetto.chess import Chess, NORMAL, CHECK, CHECKMATE, STALEMATE, WHITE, BLACK
from pyanchetto.ai.heuristic import Hueristic

class MiscHeuristic(Hueristic):
    def __init__(self):
        super().__init__()

    def compute_heuristic(self, board, player):
        state = board.game_state()
        if state == CHECKMATE:
            if board.current_player == player:
                return -1000
            else:
                return 1000
        elif state == STALEMATE:
            if board.current_player == player:
                return -500
            else:
                return 500
        elif state == CHECK:
            if board.current_player == player:
                return -5
            else:
                return 5
        else:
            num_moves = len(list(board.valid_moves()))
            if board.current_player == player:
                return num_moves
            else:
                return -num_moves
        #XXX do below in priority:
        #checkmate
        #check
        #moves that prevent castle
        #castle
        #development
        #linked knights or other reinforcements
        #don't go in a loop
        #threats matrix
        #doubled pawns
        w, b = self.material(board)
        if player == WHITE:
            return w - b
        else:
            return b - w