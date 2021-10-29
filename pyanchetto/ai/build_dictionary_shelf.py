import os, sys, logging, traceback, pickle, shelve

from pyanchetto.chess import Chess
from pyanchetto.pgn_interpreter import ChessInterpreter
from pyanchetto.pgn_parser import parse_notation

def collapse_fen(fen):
    parts = fen.split(' ')
    return " ".join([parts[0], parts[1]])

def new_game(file_name, move_dictionary):
    with open(file_name, 'r') as f:
        pgn = f.read()
        board = Chess()
        parser = parse_notation(pgn)
        tree = parser.tree
        #print(tree.pretty())
        #print("*"*50)
        interpreter = ChessInterpreter(board)
        interpreter.execute(tree, False, metadata_only=True)
        date_str = interpreter.metadata_map["Date"]
        date_str = date_str.replace('??', '01')
        event = interpreter.metadata_map["Event"]
        pgn_result = interpreter.metadata_map["Result"]
        if pgn_result == '1-0':
            result = 2
            winner = 1
        elif pgn_result == '0-1':
            result = 2
            winner = 2
        else:
            result = 4
            winner = 0
        #FIXME stalemate?
        eco = interpreter.metadata_map["ECO"]
        white_player = interpreter.metadata_map["White"]
        white_elo = interpreter.metadata_map["WhiteElo"]
        white_elo = 0 if white_elo == '?' else white_elo
        black_player = interpreter.metadata_map["Black"]
        black_elo = interpreter.metadata_map["BlackElo"]
        black_elo = 0 if black_elo == '?' else black_elo
        ply = int(interpreter.metadata_map["PlyCount"])
        if int(white_elo) > 1800 and int(black_elo) > 1800:
            board_result = interpreter.board.game_state()
            #print(f"{white_player}: {white_elo}\t{black_player}:{black_elo}")
            interpreter.execute(tree, False)
            board_result = interpreter.board.game_state()
            for i in range(1, len(interpreter.fens)-1):
                fen = collapse_fen(interpreter.fens[i])
                #next = collapse_fen(interpreter.fens[i+1])
                move = interpreter.moves[i-1]
                if fen not in move_dictionary:
                    move_dictionary[fen] = {}
                fen_moves = move_dictionary[fen]
                if move not in fen_moves:
                    fen_moves[move] = 1
                    move_dictionary.sync()
                else:
                    fen_moves[move] += 1
                    move_dictionary[fen] = fen_moves
                    move_dictionary.sync()
            return True
        else:
            return False


def ingest(path):
    on_file = 0
    success = 0
    last_success = 0
    fail = 0
    failures = []
    #move_dictionary = {}
    move_dictionary = shelve.open('2000elo.dict')
    for filename in os.listdir(path):
        #if on_file == 80000:#200000:#1000000:
        #    break
        if (success % 100) == 0 and success != last_success:
            print(f"File number: {on_file}\tSuccesses: {success}")
            move_dictionary.sync()
            last_success = success
        if success == 5000:
            break
        try:
            on_file += 1
            if filename.endswith(".pgn"):
                #print(f"{on_file}: {filename}")
                used_game = new_game(path + '/' + filename, move_dictionary)
                if used_game:
                    success += 1
        except Exception as e:
            print(f"Failed to execute PGN file {filename}")
            failures.append(filename)
            logging.error(traceback.format_exc())
            fail += 1
    print(f"Successes: {success}\t Failures: {fail}")
    print(f"Keys: {len(move_dictionary.keys())}")
    #pickle.dump(move_dictionary, open("2000elo.dict", "wb"))
    keylist = list(move_dictionary.keys())
    for i in range(40):
        frm = keylist[i]
        print(f"{frm}: {move_dictionary[frm]}")
    print(failures)
    move_dictionary.close()

def main(args):
    path = args[1]
    ingest(path)

if __name__ == '__main__':
    main(sys.argv)