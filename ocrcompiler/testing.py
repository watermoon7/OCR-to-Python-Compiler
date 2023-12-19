
if __name__ == '__main__':
    input_path = "test2.ocr"
    with open(input_path, "r") as file:
        source_code = file.read()

    lexer = Lexer(source_code)
    a = lexer.Lex()
    parser = Parser(a)

    parser.program()
