from pyanchetto.chess import Chess, NORMAL, CHECK, CHECKMATE, STALEMATE, WHITE, BLACK
from .heuristic import Hueristic

piece_values = (0, 100, 9, 5, 3, 3, 1, 100, 9, 5, 3, 3, 1)

class MaterialHeuristic(Hueristic):
    def __init__(self):
        super().__init__()

    def material(self, board):
        w, b = board.get_player_piece_types()
        white = sum([piece_values[p] for p in w])
        black = sum([piece_values[p] for p in b])
        return white, black

    def compute_heuristic(self, board, player):
        #XXX do below in priority:
        #checkmate
        #check
        #moves that prevent castle
        #castle
        #development
        #linked knights or other reinforcements
        #threats matrix
        #doubled pawns
        w, b = self.material(board)
        if player == WHITE:
            return w - b
        else:
            return b - w