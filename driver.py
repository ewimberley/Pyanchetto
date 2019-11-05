import sys
import logging
import argparse
from chess import Chess

ENCODE_IN = 'utf-8'

def parse_args():
    """Parse arguments from the command line."""
    parser = argparse.ArgumentParser(description="A cube solver in python.")
    parser.add_argument('-i', '--input', type=str, help="An input file containing cube state.", required=False)
    parser.add_argument('-o', '--output', type=str, help="An output file to save the steps required to solve the cube.")
    parser.add_argument('-v', '--verbose', help="Set verbose to true", action='store_const', const=logging.DEBUG, default=logging.WARNING, required=False)
    return parser.parse_args()

def main():
    #args = parse_args()
    #logging.basicConfig(level=args.verbose)
    print("*"*50)
    print("Deep Fianchetto.")
    print("*"*50)
    board = Chess()
    print(board)
    print(board.hash())
    board.move(('a',1),('a',2))
    print(board)

if __name__ == "__main__":
    main()