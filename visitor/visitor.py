from abc import ABC,abstractmethod





class Visitor(ABC):
    @abstractmethod
    def visit_number_expression(self,node):
        pass
    
    @abstractmethod
    def visit_variable_expression(self,node):
        pass
    
     
    @abstractmethod
    def visit_string_expression(self,node):
        pass
    
    @abstractmethod
    def visit_variable_declaration(self,node):
        pass
    
    @abstractmethod
    def visit_function_declaration(self,node):
        pass
    
    @abstractmethod
    def visit_binary_expression(self,node):
        pass
    
    @abstractmethod
    def visit_external(self,node):
        pass
    
    @abstractmethod
    def visit_function_expression(self,node):
        pass

class TypeCheckerVisitor(Visitor):
        
    def visit_number_expression(self, node):
        return super().visit_number_expression(node)
    
    def visit_variable_expression(self, node):
        return super().visit_variable_expression(node)
    
    def visit_variable_declaration(self, node):
        return super().visit_variable_declaration(node)
    
    def visit_function_declaration(self, node):
        return super().visit_function_declaration(node)
    
    def visit_binary_expression(self, node):
        return super().visit_binary_expression(node)


