
from abc import ABC,abstractmethod
from visitor.visitor import Visitor
from dataclasses import dataclass

#==============================Utils============================
@dataclass
class VariableProtoType:
    name:str
    data_type:str

@dataclass
class FunctionProtoType:
    name:str
    return_type:str
    is_variadic:bool
    args:list[VariableProtoType]
    
#=================Expressions=======================================    
class Expression(ABC):
    @abstractmethod
    def accept(self,visitor:Visitor):
        pass
   
class NumberExpression(Expression):
    def __init__(self,number:int) -> None:
        super().__init__() 

        self.value= number
        
    def accept(self,visitor:Visitor):
        return visitor.visit_number_expression(self)

class VariableExpression(Expression):
    def __init__(self,variable_name:str) -> None:
        super().__init__()
        self.name= variable_name
    
    def accept(self,visitor:Visitor):
        visitor.visit_variable_expression(self)

class StringExpression(Expression):
    def __init__(self,string:str) -> None:
        super().__init__()
        self.string= string
    
    def accept(self,visitor:Visitor):
        return visitor.visit_string_expression(self) 

class FunctionCallExpression(Expression):
    def __init__(self,function_name:str,parameter:list[Expression]) -> None:
        super().__init__()
        self.name= function_name
        self.parameter= parameter
    
    def accept(self, visitor: Visitor):
        visitor.visit_function_expression(self)
        
        

class BinaryExpression(Expression):
    def __init__(self,left:Expression,right:Expression,operation:str) -> None:
        super().__init__()
        self.right= right
        self.left= left
        self.operation=operation
    
    def accept(self, visitor: Visitor):
        return visitor.visit_binary_expression(self)




#=======================Statements================================
class Statements(ABC):
    @abstractmethod
    def accept(self,visitor:Visitor):
        pass


class VariableDeclaration(Statements):
    def __init__(self,variable_proto_type:VariableProtoType,expression:Expression) -> None:
        self.value= expression
        self.proto_type=variable_proto_type
        
    
    def accept(self,visitor:Visitor):
        visitor.visit_variable_declaration(self)


#=====================================AST============================      
class AST(ABC):
    @abstractmethod
    def accept(self,visitor:Visitor):
        pass
            
                    

        


class FunctionDeclaration(AST):
    def __init__(self,function_proto_type:FunctionProtoType,statements:list[Statements]):
        self.prototype= function_proto_type
        self.statements= statements
    
    def accept(self,visitor:Visitor):
        visitor.visit_function_declaration(self)
        
        
class External(AST):
    def __init__(self,function_proto_type:FunctionProtoType) -> None:
        self.prototype= function_proto_type
    
    def accept(self, visitor: Visitor):
        visitor.visit_external(self)
        
        
                
        



