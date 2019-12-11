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
1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6 5. O-O  Be7 6. d4 O-O  7. d5 Nb8 8. Qe2 d6 9. c4 Ne8 10. Bc2 f5 11. exf5 Bxf5 12. Bxf5 Rxf5 13. Nc3 Nd7 14. Bd2 Nf8 15. Rae1 Ng6 16. Qd3 Qd7 17. Ne4 Nf4 18. Bxf4 Rxf4 19. Nfg5 Bxg5 20. Nxg5 Qf5 21. Qxf5 Rxf5 22. Ne6 g6 23. f4 exf4 24. Rxf4 Rxf4 25. Nxf4 Kf7 26. Ne6 Rc8 27. Ng5+ Kg7 28. Ne6+ Kg8 29. Nd4 Kf7 30. Re3 Ng7 31. Rb3 b6 32. Rf3+ Kg8 33. Ra3 Re8 34. Kf2 Re4 35. Rd3 g5 36. b3 g4 37. Nc6 Nf5 38. Rd2 Kg7 39. Re2 Rf4+ 40. Kg1 Kf6 41. Nb8 b5 42. Nxa6 bxc4 43. Nxc7 c3 44. Ne6 Rb4 45. Rc2 Ne3 46. Rf2+ Ke5 47. Re2 Re4 48. Ng5 c2 49. Re1 Rd4 50. Rxe3+ Kf5 51. Rc3 Rd1+ 52. Kf2 c1=Q 53. Rxc1 Rxc1 54. Nf7 Rc2+ 55. Kg3 Rxa2 56. Nxd6+ Ke5 57. Nc4+ Kxd5 58. Ne3+ Ke6 59. Kxg4 Rb2 60. Kf4 Rxb3 61. g3 h6 62. Nc2 Kf6 63. Ne3 Rb4+ 64. Kf3 Ra4 65. Ng2 Ra3+ 66. Kg4 Ra2 67. Kh3 Kg5 68. Nh4 Rf2 69. Ng2 h5 70. Nh4 Rf6 71. Ng2 Rf3 72. Nh4 Ra3 73. Ng2 Ra4 74. Nh4 Rxh4+ 75. gxh4+ Kf4
```

## Programmatically running a PGN string
Executing a PGN string can be done in only a few lines of code.

```
from pyanchetto.chess import Chess
from pyanchetto.pgn_interpreter import ChessInterpreter
from pyanchetto.chess_parser import parse_notation
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

rnbqkb1r/ppppp2p/5p2/7Q/8/8/PPPP1PPP/R1B1KBNR b KQkq - 1 5 
```
