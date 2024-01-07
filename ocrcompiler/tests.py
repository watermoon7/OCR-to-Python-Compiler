import sys, os, glob
from ocrcompiler import Lexer, Parser
from ocrcompiler.Generator import *

def test_1(code):
    lexer = Lexer.Lexer(code)
    token_list = lexer.Lex()
    print(token_list)

code = """print("Hello world")"""
test_1(code)