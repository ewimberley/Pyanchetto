# deepfianchetto
A chess engine for deep learning experimentation.

```
board = Chess()
interpreter = ChessInterpreter(board)
game = "1. Nc3 f5 2. e4 fxe4 3. Nxe4 Nf6 4. Nxf6+ gxf6 5. Qh5#"
tree = parse_notation(game)
self.interpreter.execute(tree)

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
```
