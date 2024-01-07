#!/Users/will/Desktop/compiler/venv/bin/python
import sys, os, glob
import Lexer
import Parser
from Generator import *

def compile_file(source: str):
    with open(source, "r") as file:
        source_code = file.read()

    lexer = Lexer.Lexer(source_code)
    parser = Parser.Parser(lexer.Lex(), generator)

    parser.program()
    path = source.split('.')[0] + ".py"
    generator.write(path)
    print("Finished compilation")

def main():
    if len(sys.argv) == 1:
        sys.exit("No file path passed as an argument")
    else:
        input_path = sys.argv[1]

    if os.path.isfile(input_path):
        compile_file(input_path)
    elif os.path.isdir(input_path):
        file_paths = glob.glob(os.path.join(input_path, '*.txt'))
        for source_code in file_paths:
            compile_file(source_code)
    else:
        sys.exit("Invalid file name or directory.")

if __name__ == "__main__":
    main()