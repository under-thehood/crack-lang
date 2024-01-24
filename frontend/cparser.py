from .ctoken import Token,TokenType
import sys
from .cast import FunctionDeclaration,NumberExpression,VariableExpression,VariableDeclaration,Expression,Statements,AST,FunctionProtoType,BinaryExpression,VariableProtoType,External,StringExpression,FunctionCallExpression
from backend.codegen import CodeGenerator



class Parser:
    def __init__(self,tokens:[Token]) -> None:
        self.tokens:[Token]= tokens
        self.tokens_len:int= len(tokens)
        self.pos:int = -1
        
        self.current_token: Token| None= None
        
    def advance(self):
        self.pos= self.pos+1
        self.current_token= self.tokens[self.pos] if self.pos < self.tokens_len else None
    
    def match(self,tokentype:TokenType)->bool:
        return self.current_token.type == tokentype
    
    def expect(self,tokentype:TokenType,expected_tok_name:str=None):
        if self.current_token == None:
            raise Exception(f"[ERROR] Expected {tokentype.name} before EOF")
        else:
            if not self.match(tokentype):
                raise Exception(f"[ERROR] {tokentype.name} but found {self.current_token.type.name}")
    
    
    def parse_primary_expression(self)->Expression:

        match self.current_token.type:
            case TokenType.NUMBER:
                number= int(self.current_token.value)
                self.advance()
                return NumberExpression(number=number)
            
            case TokenType.IDENTIFIER:
                variable_name = self.current_token.value
                self.advance()
                return VariableExpression(variable_name) 
            
            case TokenType.STRING:
                string= self.current_token.value
                self.advance()
                return StringExpression(string)
            case _:
                raise Exception(f"[ERROR] Expected Expression but found {self.current_token.type.name}")
                
                
    def get_precedence(self)->int:
        match self.current_token.type:
            case TokenType.PLUS | TokenType.MINUS:
                return 1
            case TokenType.STAR | TokenType.FORWARD_SLASH:
                return 2
            
            case _:
                return -1
                
    
    def stack_eval(self,exp_stack:list[Expression],operator_stack:list[Token]):
        
        while operator_stack:
            op1= exp_stack.pop()
            op2= exp_stack.pop()
        
            operator= operator_stack.pop()
        
            match operator.type:
                case TokenType.PLUS:
                    exp_stack.append(BinaryExpression(op1,op2,'+'))  
                case TokenType.MINUS:
                    exp_stack.append(BinaryExpression(op1,op2,'-'))
                case TokenType.STAR:
                    exp_stack.append(BinaryExpression(op1,op2,'*'))
                case TokenType.FORWARD_SLASH:
                    exp_stack.append(BinaryExpression(op1,op2,'/'))
                
       
        
        
    def parse_expression(self)->Expression:
        
        operator_stack:list[Token] = []
        result_stack:list[Expression]=[]
        prev_precedence= 0
        try:
            while prev_precedence != -1:
                pexp= self.parse_primary_expression()
            
                result_stack.append(pexp)
            
                curr_precedence= self.get_precedence()
                if curr_precedence == -1:
                    break

                if prev_precedence <= curr_precedence:
                    operator_stack.append(self.current_token)
                    prev_precedence = curr_precedence
                else:
                    while len(operator_stack)!= 0:
                        self.stack_eval(result_stack,operator_stack)

                self.advance()
                
            self.stack_eval(result_stack,operator_stack)
                
            
            
            return result_stack[0]     
        except Exception as error:
            raise error
    def parse_variable_proto_type(self)->VariableProtoType:
        try:
            self.expect(TokenType.IDENTIFIER)
            variable_name= self.current_token.value
            self.advance()
            self.expect(TokenType.COLON)
            self.advance()
            self.expect(TokenType.IDENTIFIER)
            variable_type= self.current_token.value
            self.advance()
            return VariableProtoType(variable_name,variable_type)
        except Exception as error:
            raise error
    
    def parse_variable_declaration(self)->Statements | None:
        try:
            variable_proto= self.parse_variable_proto_type()
            print("Variable ProtoType is not none") if variable_proto != None else print("Variable ProtoType is none")
            
            self.expect(tokentype=TokenType.EQUAL)
            self.advance()
            expression=self.parse_expression()
            print("Variable Expression is not none") if expression != None else print("Variable expression is none")
            
            return VariableDeclaration(variable_proto,expression=expression)
        except Exception as error:
            print(error)
            return None
            
    def parse_statements(self)->list:
        statements_list=[]
        while True:
            match self.current_token.type:
                case TokenType.LET_KEYWORD:
                        self.advance()
                        var_ast=self.parse_variable_declaration()
                        print("Variable Declaration is not none") if var_ast != None else print("Variable declaration is none")
                        statements_list.append(var_ast)
                    
                case TokenType.CURLY_CLOSE:
                    return statements_list
                case TokenType.IDENTIFIER:
                    func_name=self.current_token.value
                    self.advance()
                    self.expect(TokenType.PAREN_OPEN)
                    self.advance()
                    
                    self.expect(TokenType.STRING)
                    string= self.current_token.value
                    self.advance()
                    self.expect(TokenType.PAREN_CLOSE)
                    self.advance()
                    statements_list.append(FunctionCallExpression(function_name=func_name,parameter=[StringExpression(string)]))
                    
                case _:
                    raise Exception(f"[Error] Unknown token {self.current_token.value} is found at line {self.current_token.line} cols {self.current_token.cols}")

            
    def parse_block(self)->list:
        try:
            self.expect(TokenType.CURLY_OPEN)
            self.advance()
            statements= self.parse_statements()
            self.advance()  
         
            return statements      
        except Exception as error:
            raise error
    
    def parse_function_proto_type(self)->FunctionProtoType:
        try:
            self.expect(TokenType.IDENTIFIER)
            function_name= self.current_token.value
            self.advance()
            self.expect(TokenType.PAREN_OPEN)
            self.advance()
            function_args:list[VariableProtoType]=[]
            is_variadic_function:bool=False
            return_type:str="void"
            
            if self.current_token.type !=TokenType.PAREN_CLOSE: 
                while True:
                    if self.current_token.type is TokenType.EXPANSION_OPERATOR:
                        is_variadic_function=True
                        self.advance()
                        break
                    function_arg= self.parse_variable_proto_type()
                    function_args.append(function_arg)
                    if self.current_token.type != TokenType.COMMA:
                        break
                    self.advance()
            
            self.expect(TokenType.PAREN_CLOSE)
            self.advance()
            
            if self.current_token!=None and self.current_token.type is TokenType.COLON:
                self.advance()
                self.expect(TokenType.IDENTIFIER,"return type")
                return_type=self.current_token.value
                self.advance()
            
               
            proto_type= FunctionProtoType(name=function_name,return_type=return_type,is_variadic=is_variadic_function,args=function_args)
            return proto_type
        except Exception as error:
            raise error
    
    def parse_function_declaration(self)->AST:
        
        try:
            proto_type=self.parse_function_proto_type()                
            block= self.parse_block()
            return FunctionDeclaration(proto_type,block)
        
        except Exception as error:
            print(error)
        
            
    def parse(self):
        self.ast_list:list[AST]=[]
        self.advance()
        while self.current_token != None:
            match self.current_token.type:
                
                case TokenType.FUNC_KEYWORD:
                    self.advance()
                    function_ast=self.parse_function_declaration()
                    self.ast_list.append(function_ast)
                case TokenType.EXTERN_KEYWORD:
                    self.advance()
                    function_proto= self.parse_function_proto_type()
                    self.ast_list.append(External(function_proto_type=function_proto))
                case _:
                    print(f"[Error] Unknown token {self.current_token.value} is found at line {self.current_token.line} cols {self.current_token.cols}",file=sys.stderr)
                    self.advance()

        
        
        



