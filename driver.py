import sys
import logging
import argparse
from chess import Chess
from pgn_interpreter import ChessInterpreter
from chess_parser import parse_notation

ENCODE_IN = 'utf-8'

def parse_args():
    """Parse arguments from the command line."""
    parser = argparse.ArgumentParser(description="A cube solver in python.")
    parser.add_argument('-p', '--pgn', type=str, help="An input file containing cube state.", required=False)
    parser.add_argument('-v', '--verbose', help="Set verbose to true", action='store_const', const=logging.DEBUG, default=logging.WARNING, required=False)
    return parser.parse_args()

def main():
    args = parse_args()
    logging.basicConfig(level=args.verbose)
    print("*"*50)
    print("Deep Fianchetto.")
    print("*"*50)

    board = Chess()
    #TODO handle metadata
    with open(args.pgn) as pgnfile:
        pgn = pgnfile.read()
    tree = parse_notation(pgn)
    #print(tree.pretty())
    #print("*"*50)
    interpreter = ChessInterpreter(board)
    interpreter.execute(tree)

if __name__ == "__main__":
    main()