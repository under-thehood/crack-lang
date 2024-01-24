from .ctoken import TokenType,Token
from .ckeywords import keywords

class Lexer:
    def __init__(self,data:str):
        self.data:str= data
        self.data_len:int=len(data)
        
        self.line:int=1
        self.line_index:int=0
        
        self.pos:int=-1
        
        self.tokens:[Token]=[]
        
        self.current_character:str|None =None
        
    
    
    def advance(self):
        self.pos= self.pos+1
        self.current_character= self.data[self.pos] if self.pos < self.data_len else None
        
    def peek(self,step:int)->str|None:
        return self.data[self.pos+step] if self.pos+step < self.data_len else None
            

    def tokenize(self):
        strlen= len(self.data)
        self.advance()
        
        while self.current_character != None:
            
            if self.current_character in "\t ":
                self.advance()
                continue
            
            if self.current_character.isalpha() or self.current_character =='_':
                start_index= self.pos
                while self.pos < strlen:
                    if not(self.current_character.isalnum() or self.current_character=='_'):
                        break
                    self.advance()
                
                token_value:str=self.data[start_index:self.pos]
                idtype:TokenType= keywords[token_value] if token_value in keywords else TokenType.IDENTIFIER
                self.tokens.append(Token(idtype,token_value,self.line,start_index))
                continue
            
            if self.current_character.isdigit():
                start_index= self.pos
                while self.pos < strlen:
                    if not self.current_character.isdigit():
                        break
                    self.advance()

                token_value:str=self.data[start_index:self.pos]
                self.tokens.append(Token(TokenType.NUMBER,token_value,self.line,start_index))
                continue
            
            #[TODO: Make symbol matching optimized and extensible]
            match self.current_character:
                case '=':
                    self.tokens.append(Token(TokenType.EQUAL,'=',self.line,self.pos))
                    self.advance()
                case '(':
                    self.tokens.append(Token(TokenType.PAREN_OPEN,'(',self.line,self.pos))
                    self.advance()
                case ')':
                    self.tokens.append(Token(TokenType.PAREN_CLOSE,')',self.line,self.pos))
                    self.advance()
                case '{':
                    self.tokens.append(Token(TokenType.CURLY_OPEN,'{',self.line,self.pos))
                    self.advance()
                case '}':
                    self.tokens.append(Token(TokenType.CURLY_CLOSE,'}',self.line,self.pos))
                    self.advance()
                case '\n':
                    self.line = self.line+1
                    self.line_index =self.pos+1
                    self.advance()
                case '+':
                    self.tokens.append(Token(TokenType.PLUS,'+',self.line,self.pos))
                    self.advance()
                case '-':
                    self.tokens.append(Token(TokenType.MINUS,'-',self.line,self.pos))
                    self.advance()
                case '*':
                    self.tokens.append(Token(TokenType.STAR,'*',self.line,self.pos))
                    self.advance()
                case '/':
                    self.tokens.append(Token(TokenType.FORWARD_SLASH,'/',self.line,self.pos))
                    self.advance()
                case ':':
                    self.tokens.append(Token(TokenType.COLON,':',self.line,self.pos))
                    self.advance()
                
                case '.':
                    
                    if self.peek(1) == '.' and self.peek(2) == '.':
                        self.tokens.append(Token(TokenType.EXPANSION_OPERATOR,'...',self.line,self.pos))
                        self.advance()
                        self.advance()
                        self.advance()
                    else:
                        self.tokens.append(Token(TokenType.DOT,'.',self.line,self.pos))
                        self.advance()
                
                case '"':
                    self.advance()
                    start_index= self.pos
                    while self.current_character != '"' and self.current_character != None:
                        self.advance()
                    if self.current_character != '"':
                        self.tokens.append(Token(TokenType.UNKNOWN,self.current_character,self.line,self.pos))
                    else:
                        self.tokens.append(Token(TokenType.STRING,self.data[start_index:self.pos],self.line,start_index))
                    self.advance()      
                case ',':
                    self.tokens.append(Token(TokenType.COMMA,',',self.line,self.pos))
                    self.advance()
                case _:
                    self.tokens.append(Token(TokenType.UNKNOWN,'Unknown Token :'+ self.current_character,self.line,self.pos))
                    self.advance()
        
        
                    
                    
                
                
                
                
                    
        
                    

            


            
