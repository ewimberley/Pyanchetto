# deepfianchetto
A chess engine for deep learning experimentation.

```
from deepfianchetto.chess import Chess
from deepfianchetto.pgn_interpreter import ChessInterpreter
from deepfianchetto.chess_parser import parse_notation
board = Chess()
interpreter = ChessInterpreter(board)
game = "1. Nc3 f5 2. e4 fxe4 3. Nxe4 Nf6 4. Nxf6+ gxf6 5. Qh5#"
tree = parse_notation(game)
interpreter.execute(tree, True)
print(board.fen())

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

rnbqkb1r/ppppp2p/5p2/7Q/8/8/PPPP1PPP/R1B1KBNR b KQkq - 1 
```
