from lark import Lark, Transformer, v_args
import os

#TODO: draw, draw offered, en passant, knight as "S"?, only move available
grammar = """
    start: pgn
    
    pgn: metadata* turn*
    
    metadata: "[" WORD ESCAPED_STRING "]" NEWLINE

    turn: " "? INT "." " "? move " "? move? 
            
    move: piece_type disambiguation? capture? coord move_modifiers?
        | file capture? coord move_modifiers?
        | coord promotion? move_modifiers?
        | king_side_castle move_modifiers?
        | queen_side_castle move_modifiers?
        | queen_side_castle move_modifiers?
    
    piece_type: "K" -> k | "Q" -> q | "R" -> r | "B" -> b | "N" -> n | "P" -> p 
    
    disambiguation: file | rank 
            
    coord: file rank
            
    file: "a".."h"
                         
    rank: "1".."8"
                
    king_side_castle: "O-O" | "0-0"
    
    queen_side_castle: "O-O-O" | "0-0-0"
    
    promotion: "=" piece_type
    
    white_win: "1-0"
    
    black_win: "0-1"
            
    capture: "x"
            
    move_modifiers: checks? quality? winning? outcome?
    
    checks: "+" -> check | "#" -> checkmate
    
    quality: ("!" | "?")+
    
    winning: "+-" | "+/-" | "+/=" | "=" | "=/+" | "-/+" | "-+"
    
    outcome: "1-0" -> white_win | "1/2-1/2" -> draw | "0-1" -> black_win
            
    %import common.INT 
    %import common.WORD   
    %import common.WS
    %import common.NEWLINE
    %import common.ESCAPED_STRING
    %ignore WS 
"""

parser = Lark(grammar)

def parse_file(file_name):
    with open(file_name, "r") as file:
        data = file.read()
        return parse_notation(data)

def parse_notation(move_string):
    return parser.parse(move_string)
