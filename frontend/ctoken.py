from enum import Enum

class TokenType(Enum):
    IDENTIFIER=1
    NUMBER=3
    STRING=20

    LET_KEYWORD=4
    FUNC_KEYWORD=5
    EXTERN_KEYWORD=15
    
    
    EQUAL=2
    PAREN_OPEN=7
    PAREN_CLOSE=8
    CURLY_OPEN=9
    CURLY_CLOSE=10
    PLUS=11
    MINUS=12
    STAR=13
    FORWARD_SLASH=14
    COLON=16
    COMMA=17
    DOT=18
    EXPANSION_OPERATOR=19
 
    
    

    UNKNOWN=6



class Token:
    def __init__(self,type:TokenType,value:str,line:int,cols:int):
        self.type = type
        self.value=value
        self.line= line
        self.cols=cols
        
    def display(self):
        print(f"TokenType:{self.type.name} Value:{self.value}  Line:{self.line} Cols:{self.cols}")


    