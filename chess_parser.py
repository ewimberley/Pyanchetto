from lark import Lark, Transformer, v_args

#TODO: pawn promotions, draw, draw offered, en passant, knight as "S"?, only move available
grammar = """
    start: turn*

    turn: INT "." move move 
            
    move: piece_type capture? coord move_modifiers?
        | rank capture? coord move_modifiers?
        | coord move_modifiers?
        | king_side_castle move_modifiers?
        | queen_side_castle move_modifiers?
        | queen_side_castle move_modifiers?
        
    king_side_castle: "0-0"
    
    queen_side_castle: "0-0-0"
    
    white_win: "1-0"
    
    black_win: "0-1"
            
    capture: "x"
            
    move_modifiers: checks? quality? winning?
    
    checks: "+" -> check | "#" -> checkmate
    
    quality: ("!" | "?")+
    
    winning: "+-" | "+/-" | "+/=" | "=" | "=/+" | "-/+" | "-+"
            
    piece_type: "K" -> king | "Q" -> queen | "R" -> rook | "B" -> bishop | "N" -> knight | "P" -> pawn 
            
    coord: rank | [ rank file ]
            
    rank: "a".."h"
                        
    file: "1".."8"
            
    %import common.INT 
    %import common.WORD   
    %import common.WS
    %ignore WS
"""

parser = Lark(grammar)

def parse_notation(move_string):
    return parser.parse(move_string)
