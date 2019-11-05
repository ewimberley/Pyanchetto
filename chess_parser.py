from lark import Lark, Transformer, v_args

l = Lark('''?start: turn*

            turn: INT "." move move_modifiers? move move_modifiers?
            
            move: piece_type captures? coord 
                | rank captures? coord 
                | coord 
                | "0-0"  
                | "0-0-0" 
            
            captures: "x"
            
            move_modifiers: ("+" | "#")? "!"+ "?"+
            
            piece_type: ("K" | "Q "| "R" | "B" | "N" | "P") -> piece
            
            coord: rank | [ rank file ]
            
            rank: "a".."h"
                        
            file: "1".."8"
            
            %import common.INT 
            %import common.WORD   
            %import common.WS
            %ignore WS
         ''')

@v_args(inline=True)    # Affects the signatures of the methods
class Tree(Transformer):

    def __init__(self):
        self.moves = []

def parse_notation(move_string):
   return l.parse(move_string)
