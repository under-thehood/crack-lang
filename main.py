import sys
import subprocess
sys.path.append('../')
from frontend.clexer import Lexer
from frontend.cparser import Parser
from backend.codegen import CodeGenerator
from visitor.codegen_visitor import CodeGenerationVisitor


def link_object_files_using_gcc(object_files, output_file):
    try:
        subprocess.run(["gcc", *object_files, "-o", output_file], check=True)
        print(f"Successfully linked {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error linking object files: {e}")

#[NOTE: Currently Not Working]
# def link_object_files_using_linker(object_files, output_file):
#     try:
#         subprocess.run(["ld", *object_files, "-o", output_file,'-lc'], check=True)
#         print(f"Successfully linked {output_file}")
#     except subprocess.CalledProcessError as e:
#         print(f"Error linking object files: {e}")


string= """ 
extern printf(fmt:str,...):i32

func main(){
   
   let a:i32 = 24*32+1
   
   
   let b:str= "hello world"
  
   printf("hello world\n")
   
   printf("My name is saugat")
   
   }
   """
   
   
def run_lexer():
   lexer:Lexer= Lexer(string)
   lexer.tokenize()
   for token in lexer.tokens:
      token.display()


def run_parser():
   lexer:Lexer=Lexer(string)
   
   lexer.tokenize()
   parser:Parser=Parser(lexer.tokens)
   
   parser.parse()
   return parser
   

def run_codegenerator():
   generator= CodeGenerator()
   generator.display()
   
   
if __name__ == '__main__':
   parser=run_parser()
   visitor= CodeGenerationVisitor()
   
   for ast in parser.ast_list:
      ast.accept(visitor)
   
   visitor.display()
   visitor.generator.compile()
 
   object_files = ["output.o"]  
   output_file = "program" 
   link_object_files_using_gcc(object_files, output_file)

   

