# Pyanchetto
A python chess engine.

## Running a PGN file from the command line
Specify a PGN file as input and optionally use -v or --verbose to print out each move.

```
python pyanchetto/driver.py -p examplepgn/1000144.pgn

**************************************************
Pyanchetto - Python Chess Engine.
**************************************************
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . ♟
. . . . . ♚ . ♙
. . . . . . . ♔
. . . . . . . ♙
. . . . . . . .

8/8/8/7p/5k1P/7K/7P/8 w - - 1 76
```

## Programmatically running a PGN string
Executing a PGN string can be done in only a few lines of code.

```
from pyanchetto.chess import Chess
from pyanchetto.pgn_interpreter import ChessInterpreter
from pyanchetto.pgn_parser import parse_notation
board = Chess()
interpreter = ChessInterpreter(board)
game = "1. Nc3 f5 2. e4 fxe4 3. Nxe4 Nf6 4. Nxf6+ gxf6 5. Qh5#"
tree = parse_notation(game)
interpreter.execute(tree, True)
print(board.fen())
print(board.pgn())

♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜
♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙
♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖

Turn: 1
♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜
♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . ♘ . . . . .
♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙
♖ . ♗ ♕ ♔ ♗ ♘ ♖

♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜
♟ ♟ ♟ ♟ ♟ . ♟ ♟
. . . . . . . .
. . . . . ♟ . .
. . . . . . . .
. . ♘ . . . . .
♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙
♖ . ♗ ♕ ♔ ♗ ♘ ♖

Turn: 2
♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜
♟ ♟ ♟ ♟ ♟ . ♟ ♟
. . . . . . . .
. . . . . ♟ . .
. . . . ♙ . . .
. . ♘ . . . . .
♙ ♙ ♙ ♙ . ♙ ♙ ♙
♖ . ♗ ♕ ♔ ♗ ♘ ♖

♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜
♟ ♟ ♟ ♟ ♟ . ♟ ♟
. . . . . . . .
. . . . . . . .
. . . . ♟ . . .
. . ♘ . . . . .
♙ ♙ ♙ ♙ . ♙ ♙ ♙
♖ . ♗ ♕ ♔ ♗ ♘ ♖

Turn: 3
♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜
♟ ♟ ♟ ♟ ♟ . ♟ ♟
. . . . . . . .
. . . . . . . .
. . . . ♘ . . .
. . . . . . . .
♙ ♙ ♙ ♙ . ♙ ♙ ♙
♖ . ♗ ♕ ♔ ♗ ♘ ♖

♜ ♞ ♝ ♛ ♚ ♝ . ♜
♟ ♟ ♟ ♟ ♟ . ♟ ♟
. . . . . ♞ . .
. . . . . . . .
. . . . ♘ . . .
. . . . . . . .
♙ ♙ ♙ ♙ . ♙ ♙ ♙
♖ . ♗ ♕ ♔ ♗ ♘ ♖

Turn: 4
♜ ♞ ♝ ♛ ♚ ♝ . ♜
♟ ♟ ♟ ♟ ♟ . ♟ ♟
. . . . . ♘ . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
♙ ♙ ♙ ♙ . ♙ ♙ ♙
♖ . ♗ ♕ ♔ ♗ ♘ ♖

♜ ♞ ♝ ♛ ♚ ♝ . ♜
♟ ♟ ♟ ♟ ♟ . . ♟
. . . . . ♟ . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
♙ ♙ ♙ ♙ . ♙ ♙ ♙
♖ . ♗ ♕ ♔ ♗ ♘ ♖

Turn: 5
♜ ♞ ♝ ♛ ♚ ♝ . ♜
♟ ♟ ♟ ♟ ♟ . . ♟
. . . . . ♟ . .
. . . . . . . ♕
. . . . . . . .
. . . . . . . .
♙ ♙ ♙ ♙ . ♙ ♙ ♙
♖ . ♗ . ♔ ♗ ♘ ♖

rnbqkb1r/ppppp2p/5p2/7Q/8/8/PPPP1PPP/R1B1KBNR b KQkq - 1 5 
1. Nc3 f5 2. e4 fxe4 3. Nxe4 Nf6 4. Nxf6+ gxf6 5. Qh5#
```
