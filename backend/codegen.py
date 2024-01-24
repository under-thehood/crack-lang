
from llvmlite import ir
import llvmlite.binding as llvm

data_types:dict[str:ir.Type]= {
            "i32":ir.IntType(32),
            "i64":ir.IntType(64),
            "i8":ir.IntType(8),
            "void":ir.VoidType(),
            "str":ir.PointerType(ir.IntType(8))    
        }


     

class CodeGenerator:
    def __init__(self,filename:str) -> None:
        self.context= ir.context.Context()
        self.module= ir.Module(filename,self.context)
        self.builder= ir.IRBuilder()
        
        self.data_type:dict={}
        self.function:dict={}
        
        self.variable={}
    
    def create_number_literal(self,type:ir.IntType,number:int)->ir.Value:
        return ir.Constant(data_types["i32"],number)
    
    def create_string_literal(self,string:str)->ir.Value:
        string = string + '\0'
        string_type = ir.ArrayType(ir.IntType(8), len(string))
        str_ptr = self.builder.alloca(string_type, name="str")
        self.builder.store(ir.Constant(string_type, bytearray(string.encode())), str_ptr)

        format_ptr = self.builder.gep(str_ptr, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 0)], name="format_ptr")

        
        return format_ptr
        
    def create_local_variable(self,name:str,type:str,value:ir.Value)->ir.Value:
        
        var=self.builder.alloca(data_types[type],name=name)
        self.builder.store(value, var)
        return var
    
    def create_global_variable(self,type:ir.Type,name:str,value:ir.Value)->ir.Value:
        global_variable= ir.GlobalVariable(self.module,type,name=name)
        global_variable.initializer= value
        return global_variable
    
    def create_function_proto_type(self,return_type:ir.Type,args: list,isvariadic:bool)->ir.FunctionType:
        return ir.FunctionType(return_type, args=args,var_arg=isvariadic)
    
    def create_function(self,proto_type:ir.FunctionType,function_name:str)->ir.Function:
        func= ir.Function(self.module,proto_type, name=function_name)
        self.function[function_name]= func
        return func
        
    def create_basic_block(self,function:ir.Function):
        block = function.append_basic_block(name="entry")
        self.builder._block=block
        
    def end_basic_block(self,type:str):
        self.builder.ret_void()
        
    def create_function_call(self,function_name:str,parameter:list[ir.Value]):
        self.builder.call(self.function[function_name],parameter)
        
    def create_binary_operation(self,left:ir.Value,operation:str,right:ir.Value)->ir.Value:
        match operation:
            case '+':
                return self.builder.add(lhs=left,rhs=right)
            case '-':
                return self.builder.sub(lhs=left,rhs=right) 
            case '*':
                return self.builder.mul(lhs=left,rhs=right)
            case '/':
                return self.builder.fdiv(lhs=left,rhs=right)
            
           
    def compile(self):
        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()

        # Create a target machine
        target = llvm.Target.from_default_triple()
        target_machine = target.create_target_machine()
        module = llvm.parse_assembly(str(self.module))
        obj= target_machine.emit_object(module)
        
        
    
        # # Create a module
        # module = llvm.parse_assembly(str(self.module))

        # # Create a builder
        # builder = llvm.create_mcjit_compiler(module, target_machine)

        # # Compile the module
        # builder.finalize_object()
      
        # Write the object file
        with open("output.o", "wb") as f:
            f.write(obj)

        
        # # Link the object file
        # llvm_link = llvm.get_tool('llvm-link')
        # llvm_link(['output.o', '-o', 'output'])      

        # # Compile the bitcode file
        # llvm_opt = llvm.get_tool('opt')
        # llvm_opt(['-O3', 'output.bc', '-o', 'output.opt.bc'])       

        # # Generate the executable file
        # llvm_llc = llvm.get_tool('llc')
        # llvm_llc(['output.opt.bc', '-filetype=obj', '-o', 'output.o'])

        # # Clean up
        # llvm.delete_module(module)
            
        
    
    
        
        





