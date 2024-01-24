from visitor.visitor import Visitor
from backend.codegen import CodeGenerator,data_types
from frontend.cast import BinaryExpression,FunctionDeclaration,External, StringExpression,FunctionCallExpression

class CodeGenerationVisitor(Visitor):
    def __init__(self) -> None:
        super().__init__()
        
        self.generator= CodeGenerator("module1")
        
        
    def visit_number_expression(self, node):
        return self.generator.create_number_literal(data_types["i32"],node.value)
    
    def visit_variable_expression(self, node):
        return super().visit_variable_expression(node)
    
    def visit_variable_declaration(self, node):
        return self.generator.create_local_variable(node.proto_type.name,node.proto_type.data_type,node.value.accept(self))
    
    def visit_function_declaration(self, node:FunctionDeclaration):
        args=[]
        
        for item in node.prototype.args:
            args.append(data_types[item.data_type])
            
        func_prototype= self.generator.create_function_proto_type(return_type=data_types[node.prototype.return_type],isvariadic=node.prototype.is_variadic,args=args)
        func=self.generator.create_function(func_prototype,node.prototype.name)
        self.generator.create_basic_block(func)
        
        for statement in node.statements:
            statement.accept(self)
        
        self.generator.end_basic_block("void")
        
        
    
    def visit_binary_expression(self, node:BinaryExpression):
       return self.generator.create_binary_operation(node.left.accept(self),node.operation,node.right.accept(self))
            

    def display(self):
        print(self.generator.module)
    
    def visit_external(self, node:External):
        args=[]
        
        for item in node.prototype.args:
            args.append(data_types[item.data_type])
            
        func_prototype= self.generator.create_function_proto_type(return_type=data_types[node.prototype.return_type],isvariadic=node.prototype.is_variadic,args=args)
        func=self.generator.create_function(func_prototype,node.prototype.name)
    
    def visit_string_expression(self, node:StringExpression):
        return self.generator.create_string_literal(node.string)
    
    def visit_function_expression(self, node:FunctionCallExpression):
        arg:list=[]
        for item in node.parameter:
            arg.append(item.accept(self))
        self.generator.create_function_call(node.name,arg)