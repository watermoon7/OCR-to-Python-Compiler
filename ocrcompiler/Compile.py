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
    generator.code = ""
    print("Finished compilation")

def compile_line(source_code):
    lexer = Lexer.Lexer(source_code)
    parser = Parser.Parser(lexer.Lex(), generator)

    parser.program()
    return generator.code.strip()


def main():
    if len(sys.argv) == 1:
        sys.exit("No file path passed as an argument")
    elif len(sys.argv) == 3:
        if sys.argv[1] in ["--compile", "-c"]:
            line = compile_line(sys.argv[2].rstrip("'"))
            print(line)
        elif sys.argv[1] in ["--interpret", "-i"]:
            line = compile_line(sys.argv[2].rstrip("'"))
            exec(line)
    else:
        input_path = sys.argv[1]

        if os.path.isfile(input_path):
            compile_file(input_path)
        elif os.path.isdir(input_path):
            file_paths = glob.glob(os.path.join(input_path, '*.txt')) + glob.glob(os.path.join(input_path, '*.ocr'))
            for source_code in file_paths:
                compile_file(source_code)
        else:
            sys.exit("Invalid file name or directory.")

if __name__ == "__main__":
    main()