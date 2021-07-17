import copy
import logging
import math

#import cython

SIZE = 8
piece_types = ("K", "Q", "R", "B", "N", "P")
pieces = (".", "K", "Q", "R", "B", "N", "P", "k", "q", "r", "b", "n", "p")
pieces_index = {pieces[i]: i for i in range(len(pieces))}
pieces_type_map = {p_type: (pieces_index[p_type], pieces_index[p_type.lower()]) for p_type in piece_types}
pieces_ascii = (".", "♔", "♕", "♖", "♗", "♘", "♙", "♚", "♛", "♜", "♝", "♞", "♟")
home_row = ["R", "N", "B", "Q", "K", "B", "N", "R"]
promotion_candidates = ("Q", "R", "B", "N")
game_termination_markers = ["1/2-1/2", "1-0", "0-1", "*"] #draw, white, black, ongoing/abandonded
rook_positions = [(0, 0), (7, 0), (0, 7), (7, 7)]
rook_positions_index = {rook_positions[i]: i for i in range(len(rook_positions))}
king_positions = [(4, 0), (4, 7)]
king_castle_end_positions = [(2, 0, False), (6, 0, False), (2, 7, False), (6, 7, False)]
king_castle_end_positions_index = {king_castle_end_positions[i]: i for i in range(len(king_castle_end_positions))}
rook_castle_end_positions = [(3, 0, False), (5, 0, False), (3, 7, False), (5, 7, False)]
rook_castle_end_positions_index = {rook_castle_end_positions[i]: i for i in range(len(rook_castle_end_positions))}
all_coords = [(i, j) for i in range(SIZE) for j in range(SIZE)]
knight_warps = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2)]
king_warps = [(1, 1), (-1, -1), (1, -1), (-1, 1), (0, 1), (0, -1), (1, 0), (-1, 0)]
pawn_capture_warps = [[(-1, 1), (1, 1)], [(-1, -1), (1, -1)]]
EMPTY, WHITE, BLACK = 0, 1, 2
NORMAL, CHECK, CHECKMATE, STALEMATE, DRAW = 0, 1, 2, 3, 4

def file_to_index(file): return ord(file) - 97
def index_to_file(index): return chr(index + 97)
def rank_file_to_coord(to_rank_file): return (file_to_index(to_rank_file[0]), int(to_rank_file[1]) - 1)
def coord_to_notation(coord): return index_to_file(coord[0]) + str(coord[1]+1)
def in_range(coord): return coord[0] in range(SIZE) and coord[1] in range(SIZE)
def inverse_color(color): return WHITE if color == BLACK else BLACK
def map2(func, vals): return [func(val) for val in vals] #map with side effects
def threatened_str(threatened):
    piece_arr = [str(threatened[coord[1]][SIZE - coord[0] - 1]) for coord in all_coords]
    return "".join([" ".join(piece_arr[i*SIZE:i*SIZE+SIZE])+"\n" for i in range(SIZE)])

class BadMoveException(Exception):
    pass

class BadPromotionException(Exception):
    pass

class Chess:

    def __init__(self, other=None):
        if other is not None:
            self.board = [[other.board[row][col] for col in range(SIZE)] for row in range(SIZE)]
            self.rooks_moved = copy.deepcopy(other.rooks_moved)
            self.kings_moved = copy.deepcopy(other.kings_moved)
            self.kings_castled = copy.deepcopy(other.kings_castled)
            self.current_player = other.current_player
            self.move_list = copy.deepcopy(other.move_list)
            self.pgn_str = copy.deepcopy(other.pgn_str)
            self.captured_pieces = copy.deepcopy(other.captured_pieces)
            self.promoted_pieces = copy.deepcopy(other.promoted_pieces)
            self.player_pieces_list = copy.deepcopy(other.player_pieces_list)
        else:
            self.board = [[0 for col in range(SIZE)] for row in range(SIZE)]
            self.rooks_moved, self.kings_moved, self.kings_castled = [-1, -1, -1, -1], [-1, -1], [-1, -1]
            self.current_player = 1
            self.move_list, self.pgn_str = [], []
            self.captured_pieces, self.promoted_pieces = {}, {}
            self.__set_row(0, home_row)
            self.__set_row(1, ["P"] * 8)
            self.__set_row(6, ["p"] * 8)
            self.__set_row(7, [p.lower() for p in home_row])
            self.init_player_pieces()


    def __set_row(self, row, row_pieces):
        for col in range(SIZE):
            self.set_coord((col, row), pieces_index[row_pieces[col]])
        #map2(lambda col: self.coord((col, row), pieces_index[row_pieces[col]]), [col for col in range(SIZE)])


    def init_player_pieces(self):
        self.player_pieces_list = [{c for c in all_coords if self.color(c) == color} for color in (WHITE, BLACK)]


    def set_coord(self, coord: tuple, piece):
        self.board[coord[1]][coord[0]] = piece


    def get_coord(self, coord: tuple):
        return self.board[coord[1]][coord[0]]


    def color(self, coord: tuple):
        """Returns the color of the piece at a location (or the EMPTY color if no piece is at that location)."""
        piece_type = self.board[coord[1]][coord[0]]
        if piece_type == EMPTY:
            return EMPTY
        return WHITE if piece_type < 7 else BLACK


    def is_type(self, coord: tuple, piece_type: str):
        """Returns true if the piece at a location is the given type of piece."""
        return pieces[self.board[coord[1]][coord[0]]].lower() == piece_type.lower()


    def player_pieces_of_type(self, piece_type, player):
        """Get all pieces of a certain type for a player."""
        for coord in self.player_pieces_list[player - 1]:
            if self.board[coord[1]][coord[0]] in pieces_type_map[piece_type]:
                yield coord


    def player_pieces(self, player):
        """Return a list of all pieces that belong to a player."""
        return self.player_pieces_list[player - 1]


    def game_state(self):
        #FIXME cache the result of this and invalidate the cache when a move is made
        #TODO threefold repetition and fifty move rule?
        #FIXME check for impossible checkmate (king/king, king/bishop, king/knight, king/bishop v king/bishop of same color
        piece_moves = self.valid_moves_for_player(self.current_player, True)
        has_next_move = False
        for piece in piece_moves:
            has_next_move = has_next_move or (next(piece_moves[piece], None) is not None)
        check = self.check_check(self.current_player)
        if not has_next_move:
            return CHECKMATE if check else STALEMATE
            # check for sufficient material
            white_set = set(self.player_pieces(WHITE))
            black_set = set(self.player_pieces(BLACK))
            if white_set == set({1}) and black_set == set({7}):  # king v king
                return DRAW
            if white_set == set({1, 4}) and black_set == set({7, 10}):  # king bishop v king bishop
                return DRAW
            if white_set == set({1}) and black_set == set({7, 10}):  # king v king bishop
                return DRAW
            if white_set == set({1, 4}) and black_set == set({7}):  # king bishop v king
                return DRAW
            if white_set == set({1, 5}) and black_set == set({7, 11}):  # king knight v king knight
                return DRAW
            if white_set == set({1}) and black_set == set({7, 11}):  # king v king knight
                return DRAW
            if white_set == set({1, 5}) and black_set == set({7}):  # king knight v king
                return DRAW
            if white_set == set({1, 5}) and black_set == set({7, 10}):  # king knight v king bishop
                return DRAW
            if white_set == set({1, 4}) and black_set == set({7, 11}):  # king bishop v king knight
                return DRAW
        return CHECK if check else NORMAL


    def valid_moves(self):
        threats = self.compute_threat_matrix(self.current_player)
        moves = self.valid_moves_for_player(self.current_player, True, threats)
        return moves


    def valid_moves_for_player(self, player, validate=True, threats=None):
        pieces = [p for p in self.player_pieces(player)]
        return {piece: self.valid_piece_moves(piece, validate, threats) for piece in pieces}


    def valid_piece_moves(self, p, validate=True, threats=None):
        p_type = self.board[p[1]][p[0]]
        p_type = p_type - 6 if p_type > 6 else p_type
        funcs = [lambda: [], self.king, self.queen, self.rook, self.bishop, self.knight, self.pawn]
        moves = funcs[p_type](p[0], p[1], threats) if p_type == 1 else funcs[p_type](p[0], p[1])
        if validate:
            player = self.current_player
            for move in moves: #simulate to prevent moving into check
                try:
                    self.move(p, move, False, False)
                    if not self.check_check(player):
                        self.__undo_last_move()
                        yield move
                    else:
                        self.__undo_last_move()
                except Exception as e:
                    logging.exception("Failure occurred during move simulation to look for check condition.")
                    raise e
        else:
            for move in moves:
                yield move


    def compute_threat_matrix(self, player, coord=None, max_threats=1000):
        """
        Computes a matrix that represents the number of pieces threatening each square on the board.
        A coordinate and maximum number of threats can be specified if the focus is a specific coordinate. This allows
        for early return of the method as an optimization if the querying function only needs to know whether or not a
        particular coordinate is threatened.

        Parameters
        ----------
        player: int
            The player being threatened (usually the current player).
        coord: tuple
            Return early if the threat to this coordinate is greater than max_threats.
        max_threats: int (optional, default 1000)
            Return early if threats to coord are greater than this.

        Returns
        _______
        A matrix indicating the number of threats to each coordinate on the board.
        """
        threatened = [[0 for col in range(SIZE)] for row in range(SIZE)]
        for move in self.__compute_threats(player):
            if move[2]:
                threatened[move[1]][move[0]] += 1
                if coord == move:
                    if threatened[coord[1]][coord[0]] > max_threats:
                        return threatened
        return threatened


    def __compute_threats(self, player):
        pieces = copy.deepcopy(self.player_pieces(inverse_color(player)))
        for piece in pieces:
            for move in self.valid_piece_moves(piece, False):
                if move[2]:
                    yield move
        for pawn in self.player_pieces_of_type("P", inverse_color(player)):
            for threat in self.pawn_threats(pawn[0], pawn[1]):
                yield threat


    def check_check(self, player, threats=None):
        """
        Determines if a player is currently in check.
        A precomputed threat matrix can be provided as an optimization.
        """
        #XXX can we use the optimized threats function to just check the king square?
        threats = self.__compute_threats(player) if threats is None else threats
        king = list(self.player_pieces_of_type("K", player))
        return (king[0][0], king[0][1], True) in threats


    def move(self, fromc, to, validate=True, pgn_gen=True):
        if validate:
            threats = self.compute_threat_matrix(self.current_player) if self.is_type(fromc, "K") else None
            valid_moves = self.valid_piece_moves(fromc, True, threats) if self.color(fromc) == self.current_player else {}
            #below line used for debugging valid moves only
            #valid_moves = list(valid_moves)
        if not validate or to in valid_moves:
            if pgn_gen and validate:
                self.__append_move_to_pgn(fromc, pgn_gen, to, validate)
            if self.is_type(fromc, "R") and fromc in rook_positions_index:
                rook_index = rook_positions_index[fromc]
                if self.rooks_moved[rook_index] == -1:
                    self.rooks_moved[rook_index] = len(self.move_list)
            elif self.is_type(fromc, "K") and fromc in king_positions:
                king_index = king_positions.index(fromc)
                on_move = len(self.move_list)
                if self.kings_moved[king_index] == -1:
                    self.kings_moved[king_index] = on_move
                if to in king_castle_end_positions and self.kings_moved[king_index] == on_move:
                    rook_index = king_castle_end_positions_index[to]
                    rook_position = rook_positions[rook_index]
                    if self.is_type(rook_position, "R") and self.color(rook_position) == self.current_player:
                        self.rooks_moved[rook_index] = on_move
                        self.__move_piece(rook_position, rook_castle_end_positions[rook_index])
                        castle_pos_index = king_castle_end_positions.index(to)
                        self.kings_castled[king_index] = on_move
            self.__move_piece(fromc, to)
            self.move_list.append((fromc, (to[0], to[1])))
            if len(to) == 4:
                self.__handle_special(fromc, to)
            self.current_player = inverse_color(self.current_player)
            if pgn_gen and validate:
                self.__append_game_state_to_pgn()
        else:
            raise BadMoveException("Move is invalid")


    def __append_move_to_pgn(self, fromc, pgn_gen, to, validate):
        pgn_castle, pgn_promotion, file_disambiguation, rank_disambiguation = None, "", "", ""
        if self.is_type(fromc, "K") and fromc in king_positions:
            if to in king_castle_end_positions:
                castle_pos_index = king_castle_end_positions.index(to)
                pgn_castle = "O-O-O " if castle_pos_index == 0 or castle_pos_index == 2 else "O-O "
        to_color = self.color(to)
        capture_str = "x" if to_color != EMPTY else ""
        if pgn_castle is not None:
            pgn = pgn_castle
        else:
            pgn_type = pieces[self.get_coord(fromc)].upper()
            piece_type = self.get_coord(fromc)
            # TODO piece disambiguation if same type of piece can move to to_coord
            for piece in self.__type_in_coords(self.player_pieces_list[self.current_player - 1], piece_type):
                if self.board[piece[1]][piece[0]] == piece_type and piece != fromc:
                    for move in self.valid_piece_moves(piece):
                        if move == to:
                            if piece[0] == fromc[0]:
                                rank_disambiguation = str(fromc[1] + 1)
                            else:
                                file_disambiguation = index_to_file(fromc[0])
            notation_coord = coord_to_notation(to)
            if pgn_type == "P":
                if len(to) == 4 and to[3] != 6 and to[3] != 12:
                    pgn_promotion = "=" + to[3].upper()
                if capture_str != "":
                    pgn = index_to_file(fromc[0]) + capture_str + notation_coord + pgn_promotion
                else:
                    pgn = notation_coord + pgn_promotion
            else:
                pgn = pgn_type + file_disambiguation + rank_disambiguation + capture_str + notation_coord
        if self.current_player == WHITE:
            self.pgn_str.append(str(self.__get_full_move_clock()) + ".")
        self.pgn_str.append(pgn)


    def __append_game_state_to_pgn(self):
        """
        Append information related to game state to the PGN move list, including
        move annotations and game termination markers.
        Preconditions: a move has just been made and current_player has been updated to the next player.
        """
        state = self.game_state()
        modifier = None
        if state == CHECK:
            modifier = "+"
        elif state == CHECKMATE:
            modifier = "#"
        if modifier is not None:
            self.pgn_str[-1] += modifier
            if state == CHECKMATE:
                self.pgn_str.append(game_termination_markers[inverse_color(self.current_player)])
            if state == STALEMATE:
                self.pgn_str.append(game_termination_markers[0])


    def __move_piece(self, fromc, to):
        from_color = self.color(fromc)
        to_color = self.color(to)
        if to_color != EMPTY:
            captured = (to[0], to[1])
            self.captured_pieces[len(self.move_list)] = (self.board[to[1]][to[0]], captured)
            self.player_pieces_list[to_color - 1].remove(captured)
        self.player_pieces_list[from_color - 1].remove(fromc)
        self.player_pieces_list[from_color - 1].add((to[0], to[1]))
        self.board[to[1]][to[0]] = self.board[fromc[1]][fromc[0]]
        self.board[fromc[1]][fromc[0]] = EMPTY


    def __undo_last_move(self):
        last_move = self.move_list.pop()
        last_move_type = self
        last_move_index = len(self.move_list)
        captured = self.captured_pieces.pop(last_move_index, None)
        self.current_player = inverse_color(self.current_player)
        if self.is_type(last_move[1], "R") and last_move[0] in rook_positions:
            if self.rooks_moved[rook_positions_index[last_move[0]]] == last_move_index:
                self.rooks_moved[rook_positions_index[last_move[0]]] = -1
        elif self.is_type(last_move[1], "K") and last_move[0] in king_positions:
            if self.kings_moved[king_positions.index(last_move[0])] == last_move_index:
                self.kings_moved[king_positions.index(last_move[0])] = -1
                king_pos = (last_move[1][0], last_move[1][1], False)
                #if king_pos in king_castle_end_positions: #XXX use self.king_castled instead
                if last_move_index in self.kings_castled: #undo castle
                    rook_index = king_castle_end_positions_index[king_pos]
                    king_index = self.current_player - 1
                    rook_pos = rook_castle_end_positions[rook_index]
                    self.__move_piece((rook_pos[0], rook_pos[1]), rook_positions[rook_index])
                    self.rooks_moved[rook_index] = -1
                    self.kings_castled[king_index] = -1
        elif last_move_index in self.promoted_pieces:
            self.board[last_move[1][1]][last_move[1][0]] = 6 if self.current_player == WHITE else 12
            self.promoted_pieces.pop(last_move_index)
        self.__move_piece(last_move[1], last_move[0])
        if captured is not None:
            self.board[captured[1][1]][captured[1][0]] = captured[0]
            self.player_pieces_list[self.color(captured[1]) - 1].add(captured[1])

    def __handle_special(self, fromc, to):
        """Handles one-off move types like en pessant and pawn promotion when applying a move."""
        if to[3] == 6 or to[3] == 12: #en pessant
            captured = (to[0], fromc[1])
            captured_color = self.color(captured)
            self.captured_pieces[len(self.move_list) - 1] = (self.board[captured[1]][captured[0]], captured)
            self.board[captured[1]][captured[0]] = EMPTY
            self.player_pieces_list[captured_color - 1].remove(captured)
        else: #promotion
            promotion_type = to[3]
            if promotion_type.upper() in promotion_candidates and self.is_type(to, "P"):
                if self.current_player == WHITE and to[1] == 7:
                    self.board[to[1]][to[0]] = pieces_index[promotion_type.upper()]
                elif self.current_player == BLACK and to[1] == 0:
                    self.board[to[1]][to[0]] = pieces_index[promotion_type.lower()]
                else:
                    raise BadPromotionException("Cannot promote from this position")
                self.promoted_pieces[len(self.move_list)-1] = (self.board[to[1]][to[0]], to)
            else:
                raise BadPromotionException("Invalid promotion")


    def pawn_threats(self, f, r):
        color = self.color((f, r))
        for threat in self.__warps([], (f, r), pawn_capture_warps[color - 1], (color,)):
            yield threat


    def pawn(self, f, r):
        """Returns all valid moves for a pawn at file f and rank r including en pessant and valid promotions."""
        color = self.color((f, r))
        warps = [[(0, 1), (0, 2)] if r == 1 and self.color((f, r + 1)) == EMPTY else [(0, 1)]]
        warps.append([(0, -1), (0, -2)] if r == 6 and self.color((f, r - 1)) == EMPTY else [(0, -1)])
        moves = self.__warps([], (f, r), warps[color - 1], (WHITE, BLACK), False)
        for move in self.__warps(moves, (f, r), pawn_capture_warps[color - 1], (EMPTY, color)):
            if color == WHITE and move[1] == 7:
                for promotion in promotion_candidates:
                    yield (move[0], move[1], move[2], promotion)
            elif color == BLACK and move[1] == 0:
                for promotion in promotion_candidates:
                    yield (move[0], move[1], move[2], promotion.lower())
            else:
                yield move
        if len(self.move_list) > 0: #en pessant - check that last move was a double pawn advance
            last_move = self.move_list[-1]
            piece_type = self.board[last_move[1][1]][last_move[1][0]]
            if (piece_type == 6 or piece_type == 12) and self.color(last_move[1]) == inverse_color(color):
                if abs(last_move[1][1] - last_move[0][1]) == 2 and abs(last_move[0][0] - f) == 1 and last_move[1][1] == r:
                    if color == 2:
                        yield (last_move[0][0], r - 1, False, self.board[r][f])
                    else:
                        yield (last_move[0][0], r + 1, False, self.board[r][f])


    def rook(self, f, r):
        """Returns all valid moves for a rook at file f and rank r."""
        return self.__orthogonal([], f, r)


    def bishop(self, f, r):
        """Returns all valid moves for a bishop at file f and rank r."""
        return self.__diagonal([], f, r)


    def knight(self, f, r):
        """Returns all valid moves for a knight at file f and rank r."""
        return self.__warps([], (f, r), knight_warps, (self.color((f, r)),))


    def queen(self, f, r):
        """Returns all valid moves for a queen at file f and rank r."""
        return self.__orthogonal(self.__diagonal([], f, r), f, r)


    def king(self, f, r, threats=None):
        """Returns all valid moves for a king at file f and rank r including castling (does not allow king to move into check or checkmate)."""
        color = self.color((f, r))
        castle_moves = []
        if self.kings_moved[color - 1] == -1:
            #if self.rooks_moved[0 if color == WHITE else 2] == -1 and self.positions_clear([(1, r), (2, r), (3, r)], threats): #king does not move through (1, r)?
            if self.rooks_moved[0 if color == WHITE else 2] == -1 and self.positions_clear([(2, r), (3, r)], threats):
                    castle_moves.append((2, r, False))
            if self.rooks_moved[1 if color == WHITE else 3] == -1 and self.positions_clear([(5, r), (6, r)], threats):
                castle_moves.append((6, r, False))
        for move in self.__warps(castle_moves, (f, r), king_warps, (color,)):
            yield move


    def positions_clear(self, coords, threats=None):
        """
        Determines if all coordinates in coords list are clear of both pieces and threats.

        Parameters
        ----------
        coords: list of tuples
            A list of coordinates to check for pieces and threats
        threats: matrix object
            A board matrix containing the number of threats per square

        Returns
        _______
        True if none of the coords contain a piece or are threatened, False otherwise.
        """
        for coord in coords:
            status = 0 if threats is None else threats[coord[1]][coord[0]]
            if self.board[coord[1]][coord[0]] != 0 or status != 0:
                return False
        return True


    def __warps(self, moves, coord, relative_warps, excluded, threat=True):
        #Warps can result in capturing the piece at the destination, so threat is True
        for move in moves:
            yield move
        for w in relative_warps:
            warp = (coord[0] + w[0], coord[1] + w[1], threat)
            if warp[0] < 8 and warp[0] >= 0 and warp[1] < 8 and warp[1] >= 0 and self.color(warp) not in excluded:
                yield warp


    def __orthogonal(self, moves, f, r):
        """
        Compute move set for a piece that has orthogonal (horizontal and vertical) movement.

        Parameters
        ----------
        moves: list of tuples
            A set of moves to append diagonal moves to.
        f: int
            The current file of the piece.
        r: int
            The current rank of the piece.
            
        Returns
        _______
        moves: list of tuples
            The input list of moves with orthogonal moves appended to it.
        """
        return self.__vectors(moves, f, r, [(1, 0), (-1, 0), (0, 1), (0, -1)])


    def __diagonal(self, moves, f, r):
        """
        Compute move set for a piece that has orthogonal (horizontal and vertical) movement.

        Parameters
        ----------
        moves: list of tuples
            A set of moves to append diagonal moves to.
        f: int
            The current file of the piece.
        r: int
            The current rank of the piece.
            
        Returns
        _______
        moves: list of tuples
            The input list of moves with diagonal moves appended to it.
        """
        return self.__vectors(moves, f, r, [(1, 1), (-1, -1), (1, -1), (-1, 1)])
    

    def __vectors(self, moves, f, r, offsets_list):
        """
        Generates moves going in a list of vectors from a starting position until
        either the edge of the board or another piece is encountered.

        Parameters
        ----------
        moves: list of tuples
            A set of moves to append moves to.
        f: int
            The current file of the piece.
        r: int
            The current rank of the piece.

        offsets_list: list of tuples
            A list of vectors to travel in (e.g. if start is (0,0) and vector is (1,1)
            move set will be (0,0), (1,1), (2,2), (3,3), etc.
            
        Returns
        _______
        moves: list of tuples
            The input list of moves with vectored moves appended to it.
        """
        for move in moves:
            yield move
        color = self.color((f, r))
        inv_color = inverse_color(color)
        for offset in offsets_list:
            coord = (f + offset[1], r + offset[0], True)
            while coord[0] < 8 and coord[0] >= 0 and coord[1] < 8 and coord[1] >= 0 and self.color(coord) in (inv_color, EMPTY):
                yield coord
                if self.color(coord) == inv_color:
                    break
                coord = (offset[1] + coord[0], offset[0] + coord[1], coord[2])


    def __type_in_coords(self, coords, type):
        for coord in coords:
            if self.board[coord[1]][coord[0]] == type:
                yield coord


    def __str__(self):
        piece_arr = [pieces_ascii[self.get_coord((coord[1], SIZE - coord[0] - 1))] for coord in all_coords]
        return "".join([" ".join(piece_arr[i*SIZE:i*SIZE+SIZE])+"\n" for i in range(SIZE)])


    def fen(self):
        """Return the FEN hash string for the current state of the game."""
        hash = []
        for i, coord in enumerate(all_coords):
            p_type = self.get_coord((coord[1], SIZE - coord[0] - 1))
            if i % 8 == 0 and i > 0:
                hash.append("/")
            if p_type == EMPTY:
                if len(hash) > 0 and hash[-1] in ("1", "2", "3", "4", "5", "6", "7", "8"):
                    hash[-1] = str(int(hash[-1]) + 1)
                else:
                    hash.append("1")
            else:
                hash.append(pieces[p_type])
        hash.append(" w " if self.current_player == WHITE else " b ")
        hash_len = len(hash)
        if self.kings_moved[0] == -1:
            if self.rooks_moved[0] == -1:
                hash.append("K")
            if self.rooks_moved[1] == -1:
                hash.append("Q")
        if self.kings_moved[1] == -1:
            if self.rooks_moved[2] == -1:
                hash.append("k")
            if self.rooks_moved[3] == -1:
                hash.append("q")
        if len(hash) == hash_len: #nothing new appeneded for castling
            hash.append("-")
        if len(self.move_list) > 0:
            last_move = self.move_list[-1]
            if self.is_type(last_move[1], "P") and abs(last_move[1][1] - last_move[0][1]) == 2: #en pessant target
                behind_rank = last_move[1][1] - (-1 if self.current_player == WHITE else 1) #reversed for opponents pawn
                hash.append(" " + coord_to_notation((last_move[1][0], behind_rank)) + " ")
            else:
                hash.append(" - ")
        else:
            hash.append(" - ")
        hash.append(str(self.__get_half_move_clock()))
        full_moves = self.__get_full_move_clock()
        hash.append(" " + str(full_moves))
        return "".join(hash)


    def __get_full_move_clock(self):
        return math.floor(len(self.move_list) / 2) + 1


    def __get_half_move_clock(self):
        move_index = len(self.move_list)
        if move_index > 0:
            last_cap_or_pawn = move_index
            while last_cap_or_pawn:
                if (last_cap_or_pawn - 1) in self.captured_pieces:
                    break
                if self.is_type(self.move_list[last_cap_or_pawn - 1][1], "P"):
                    break
                last_cap_or_pawn -= 1
            return move_index - last_cap_or_pawn
        else:
            return 0


    def pgn(self):
        """Return the PGN string for the current state of the game."""
        return " ".join(self.pgn_str)


    def get_captured_pieces(self):
        """Get the types of all captured pieces."""
        capture_pieces = []
        for move_num in range(len(self.move_list)):
            if move_num in self.captured_pieces:
                capture_pieces.append(self.captured_pieces[move_num][0])
        return capture_pieces