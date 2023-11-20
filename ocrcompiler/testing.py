import sys
from Tokens import *

# if you see this message, forgive me for the sins I have committed


def split_list_by_element(lst, element):
    result = []
    current_sublist = []

    for item in lst:
        if isinstance(item, element):
            if current_sublist:
                result.append(current_sublist)
                current_sublist = []
        else:
            current_sublist.append(item)

    if current_sublist:
        result.append(current_sublist)

    return result

def check_if_keyword(text):
    if text == 'if': return IF
    elif text == 'elseif': return ELIF
    elif text == 'else': return ELSE
    elif text == 'then': return THEN
    elif text == 'endif': return ENDIF
    elif text == 'while': return WHILE
    elif text == 'endwhile': return ENDWHILE
    elif text == 'for': return FOR
    elif text == 'to': return TO
    elif text == 'next': return NEXT
    elif text == 'do': return DO
    elif text == 'until': return UNTIL
    elif text == 'switch': return SWITCH
    elif text == 'endswitch': return ENDSWITCH
    elif text == 'case': return CASE
    elif text == 'default': return DEFAULT
    elif text == 'function': return FUNCTION
    elif text == 'endfunction': return ENDFUNCTION
    elif text == 'procedure': return PROCEDURE
    elif text == 'endprocedure': return ENDPROCEDURE
    elif text == 'return': return RETURN
    elif text == 'class': return CLASS
    elif text == 'inherits': return INHERITS
    elif text == 'public': return PUBLIC
    elif text == 'private': return PRIVATE
    elif text == 'super': return SUPER
    elif text == 'endclass': return ENDCLASS
    elif text == 'new': return NEW
    elif text == 'AND': return AND
    elif text == 'OR': return OR
    elif text == 'NOT': return NOT
    else: return None

class Lexer:

    def __init__(self, source_code):
        # the lexer steps through the code
        self.source_code = source_code.replace("    ", "\t") + '\n'
        self.cur_char = ''
        self.cur_pos = -1
        self.next_char()

    def next_char(self):
        self.cur_pos += 1
        if self.cur_pos >= len(self.source_code):
            self.cur_char = "EOF"
        else:
            self.cur_char = self.source_code[self.cur_pos]
        return self.cur_char

    def peek(self):
        if self.cur_pos + 1 >= len(self.source_code):
            return "EOF"
        return self.source_code[self.cur_pos + 1]

    def skip_whitespace(self):
        while self.cur_char == ' ' or self.cur_char == '\r':
            self.next_char()

    def get_token(self):
        self.skip_whitespace()

        if self.cur_char == '+':
            token = PLUS()
        elif self.cur_char == '-':
            token = MINUS()
        elif self.cur_char == '*':
            token = ASTERISK()
        elif self.cur_char == '/':
            if self.peek() == '/':
                self.next_char()
                start_pos = self.cur_pos + 1
                while self.peek() != "\n":
                    self.next_char()
                token = COMMENT(self.source_code[start_pos : self.cur_pos + 1])
            else:
                token = SLASH()
        elif self.cur_char == '^':
            token = CARAT()
        elif self.cur_char == '(':
            token = OPENPAR()
        elif self.cur_char == ')':
            token = CLOSEPAR()
        elif self.cur_char == '[':
            token = OPENSQR()
        elif self.cur_char == ']':
            token = CLOSESQR()
        elif self.cur_char == ':':
            token = COLON()
        elif self.cur_char == ',':
            token = COMMA()
        elif self.cur_char == '.':
            token = PERIOD()
        elif self.cur_char == '=':
            if self.peek() == '=':
                self.next_char()
                token = EQEQ()
            else:
                token = EQ()
        elif self.cur_char == '>':
            if self.peek() == '=':
                self.next_char()
                token = GTEQ()
            else:
                token = GT()
        elif self.cur_char == '<':
            if self.peek() == '=':
                self.next_char()
                token = LTEQ()
            else:
                token = LT()
        elif self.cur_char == '!':
            if self.peek() == '=':
                self.next_char()
                token = NOTEQ()
            else:
                sys.exit("Expected !=, got !" + self.peek())
        elif self.cur_char == '\n':
            token = NL()
        elif self.cur_char == '\t':
            token = TAB()
        elif self.cur_char == "EOF":
            token = EOF()
        elif self.cur_char in ['\"', "“"]:
            self.next_char()
            start_pos = self.cur_pos

            while self.cur_char not in ['\"', "“"]:
                # Probably don't need this if statement - remove after testing
                if self.cur_char in ['\r', '\n', '\t', '\\']:
                    sys.exit("Illegal character in string: " + str([self.cur_char])[1:-1])
                elif self.cur_char == "EOF":
                    sys.exit("Error: Unterminated string.")
                self.next_char()

            string_text = self.source_code[start_pos : self.cur_pos]
            token = STR(string_text)
        elif self.cur_char.isdigit():
            start_pos = self.cur_pos

            while self.peek().isdigit():
                self.next_char()

            if self.peek() == '.':
                self.next_char()
                if not self.peek().isdigit():
                    sys.exit("Expected a digit, got " + self.peek())
                while self.peek().isdigit():
                    self.next_char()

                token = FLOAT(self.source_code[start_pos : self.cur_pos + 1])
            else:
                token = INT(self.source_code[start_pos: self.cur_pos + 1])
        elif self.cur_char.isalpha():
            start_pos = self.cur_pos

            while self.peek().isalnum() or self.peek() in ["_", "-"]:
                self.next_char()

            token_text = self.source_code[start_pos : self.cur_pos + 1]
            if token_text in ["true", "false"]:
                token = BOOL(token_text)
            else:
                keyword = check_if_keyword(token_text)

                if keyword is None:
                    token = IDENT(token_text)
                else:
                    token = keyword()
        else:
            sys.exit("Unknown token: " + self.cur_char)

        self.next_char()
        return token

    def Lex(self):
        token = self.get_token()
        token_list = [token]
        while not isinstance(token, EOF):
            token = self.get_token()
            token_list.append(token)
        return token_list


def generate(kind):
    # function to manually generate text 
    generator.generate(kind)

def index_token_sublist(lst, sublist):
    # returns the index of the first instance of a sublist of tokens in a token list
    # e.g. the index of
    # [TAB, PRINT] in
    # [IF, COMPARISON, THEN, NL, TAB, PRINT, OPENPAR, IDENT, CLOSEPAR, NL, ENDIF, NL EOF]
    # is 4
    try:
        # ;) hehe
        return list(zip(*[list(map(type, lst))[i:len(lst)-len(sublist)+i+1] for i in range(len(sublist))])).index(sublist)
    except:
        return -1



class Parser:

    def __init__(self, token_list):
        self.token_list = token_list
        self.tok = self.next_token()
        self.global_symbols = {"print", "input", "openRead", "openWrite", "int", "str", "bool", "float", "+"}
        self.classes = set()
        self.line = 1

    def next_token(self):
        #print(self.token_list[:20])
        return self.token_list.pop(0)

    def affirm_grammar(self, *args, local_symbols = None, nullify = False):
        if local_symbols is None: local_symbols = {}

        # ensures that the tokens passed in are the next ones in the token list
        tok_keywords = []
        for kind in args:
            if isinstance(self.tok, kind):
                if isinstance(self.tok, NL):
                    self.line += 1
                if not nullify:
                    self.tok.generate()
                tok_keywords.append(self.tok.keyword)
                self.tok = self.next_token()
            elif isinstance(kind(), (INT, BOOL, STR, FLOAT)) and isinstance(self.tok, IDENT):
                self.tok.generate()
                if isinstance(self.token_list[0], OPENPAR):
                    self.call(local_symbols)
                self.tok = self.next_token()
            else:
                sys.exit("Wrong token. Expected a " + str(type(kind())) + " but got a " + str(type(self.tok)) + " at line " + str(self.line))
        return tok_keywords

    def affirm_tabs(self, iterations = None):
        # affirms that there is proper indentation
        for _ in range(max(0, iterations)):
            self.affirm_grammar(TAB)

    def call(self, local_symbols):
        # method for affirming proper call logic
        # e.g. ensuring that if a function is called then brackets and parameters are passed properly
        self.affirm_grammar(OPENPAR)
        while not isinstance(self.tok, CLOSEPAR):
            if isinstance(self.tok, IDENT):
                local_symbols.add(self.tok.keyword)
            self.expression(local_symbols)
            if isinstance(self.tok, COMMA):
                self.affirm_grammar(COMMA)
            else:
                assert isinstance(self.tok, CLOSEPAR), \
                "Expected a ')' but got a " + str(type(self.tok)) + " at line " + str(self.line)

        self.affirm_grammar(CLOSEPAR)
        return local_symbols

    def statement(self, local_symbols = None, extra_tabs = 0):
        self.affirm_tabs(extra_tabs)
        if local_symbols is None: local_symbols = set()

        if isinstance(self.tok, IF):
            self.affirm_grammar(IF)
            self.comparison(local_symbols)
            self.affirm_grammar(THEN, NL)

            local_symbols = self.statement(local_symbols, extra_tabs = extra_tabs + 1)
            while index_token_sublist([self.tok] + self.token_list, (*[TAB for _ in range(max(0, extra_tabs))], ENDIF)) != 0:
                if index_token_sublist([self.tok] + self.token_list, (*[TAB for _ in range(max(0, extra_tabs))], ELIF)) == 0:
                    self.affirm_tabs(extra_tabs)
                    self.affirm_grammar(ELIF)
                    self.comparison(local_symbols)
                    self.affirm_grammar(THEN, NL)
                elif index_token_sublist([self.tok] + self.token_list, (*[TAB for _ in range(max(0, extra_tabs))], ELSE)) == 0:
                    self.affirm_tabs(extra_tabs)
                    self.affirm_grammar(ELSE, THEN, NL)
                local_symbols = self.statement(local_symbols, extra_tabs = extra_tabs + 1)
            self.affirm_tabs(extra_tabs)
            self.affirm_grammar(ENDIF, NL)
        elif isinstance(self.tok, WHILE):
            print("WHILE STATEMENT")
            print(local_symbols)
            self.affirm_grammar(WHILE)
            self.comparison(local_symbols)
            generate(":")
            self.affirm_grammar(NL)

            local_symbols = self.statement(local_symbols, extra_tabs = extra_tabs + 1)
            while index_token_sublist([self.tok] + self.token_list, (*[TAB for _ in range(max(0, extra_tabs))], ENDWHILE)) != 0:
                local_symbols = self.statement(local_symbols, extra_tabs = extra_tabs + 1)
                print("    ", local_symbols)
            self.affirm_tabs(extra_tabs)
            self.affirm_grammar(ENDWHILE, NL)
        elif isinstance(self.tok, FOR):
            iterator = self.affirm_grammar(FOR, IDENT)[1]
            generate(' in range(')
            self.affirm_grammar(EQ, nullify=True)
            self.affirm_grammar(INT, local_symbols = local_symbols)
            generate(", ")
            self.affirm_grammar(TO, nullify=True)
            self.affirm_grammar(INT, local_symbols = local_symbols)
            generate("):")
            local_symbols.add(iterator)
            self.affirm_grammar(NL)

            local_symbols = self.statement(local_symbols, extra_tabs = extra_tabs + 1)
            while index_token_sublist([self.tok] + self.token_list, (*[TAB for _ in range(max(0, extra_tabs))], NEXT)) != 0:
                local_symbols = self.statement(local_symbols, extra_tabs = extra_tabs + 1)

            self.affirm_tabs(extra_tabs)
            keywords = self.affirm_grammar(NEXT, IDENT, nullify = True)
            self.affirm_grammar(NL)
            assert iterator == keywords[1], \
                "Expected " + iterator + " but got " + keywords[1] + " at line " + str(self.line)
        elif isinstance(self.tok, DO):
            # BROKEN FOR NESTED DO STATEMENTS
            self.affirm_grammar(DO, NL, nullify = True)
            generate("while not (")

            pos = index_token_sublist(self.token_list, (NL, *[TAB for _ in range(extra_tabs)], UNTIL)) + extra_tabs + 1
            temp, self.token_list = self.token_list[:pos], self.token_list[pos:]

            self.affirm_grammar(TAB, UNTIL, nullify = True)
            self.comparison(local_symbols)
            generate("):")
            self.affirm_grammar(NL)
            extra_tok = self.tok
            # need to include a tab at the start because it was looked over when calling self.next_token()
            # also need to include UNTIL(), NL() so that we know when the end of the block is

            self.token_list = [TAB()] + temp + [UNTIL(), NL()] + [extra_tok] + self.token_list
            self.line -= 1
            self.tok = self.next_token()

            local_symbols = self.statement(local_symbols, extra_tabs = extra_tabs + 1)
            while index_token_sublist([self.tok] + self.token_list, (*[TAB for _ in range(max(0, extra_tabs))], UNTIL)) != 0:
                local_symbols = self.statement(local_symbols, extra_tabs = extra_tabs + 1)

            self.affirm_tabs(extra_tabs)
            self.affirm_grammar(UNTIL, NL)
        elif isinstance(self.tok, SWITCH):
            self.affirm_grammar(SWITCH, IDENT, COLON, NL)

            self.affirm_tabs(extra_tabs + 1)
            self.affirm_grammar(CASE)
            self.expression(local_symbols)
            self.affirm_grammar(COLON, NL)
            local_symbols = self.statement(local_symbols, extra_tabs + 2)

            flag = False
            while index_token_sublist([self.tok] + self.token_list, (*[TAB for _ in range(max(0, extra_tabs))], ENDSWITCH)) != 0:
                if index_token_sublist([self.tok] + self.token_list, (*[TAB for _ in range(max(0, extra_tabs+1))], CASE)) == 0 and not flag:
                    self.affirm_tabs(extra_tabs + 1)
                    self.affirm_grammar(CASE)
                    self.expression(local_symbols)
                    self.affirm_grammar(COLON, NL)
                elif index_token_sublist([self.tok] + self.token_list, (*[TAB for _ in range(max(0, extra_tabs+1))], DEFAULT)) == 0 and not flag:
                    self.affirm_tabs(extra_tabs + 1)
                    self.affirm_grammar(DEFAULT, COLON, NL)
                    flag = True

                local_symbols = self.statement(local_symbols, extra_tabs + 2)

            self.affirm_tabs(extra_tabs)
            self.affirm_grammar(ENDSWITCH, NL)
        elif isinstance(self.tok, (FUNCTION, PROCEDURE)):
            temp = self.tok
            self.affirm_grammar(FUNCTION if isinstance(self.tok, FUNCTION) else PROCEDURE)

            name = self.tok.keyword
            local_symbols.add(name)
            self.affirm_grammar(IDENT)
            temp_local_symbols = self.call(local_symbols)
            generate(":")
            self.affirm_grammar(NL)

            temp_local_symbols = self.statement(local_symbols | temp_local_symbols, extra_tabs = extra_tabs + 1)
            while index_token_sublist([self.tok] + self.token_list, (*[TAB for _ in range(max(0, extra_tabs))], ENDFUNCTION if isinstance(temp, FUNCTION) else ENDPROCEDURE)) != 0:
                temp_local_symbols = self.statement(local_symbols | temp_local_symbols, extra_tabs = extra_tabs + 1)

            self.affirm_tabs(extra_tabs)
            self.affirm_grammar(ENDFUNCTION if isinstance(temp, FUNCTION) else ENDPROCEDURE, NL)
        elif isinstance(self.tok, RETURN):
            self.affirm_grammar(RETURN)
            self.expression(local_symbols)
            self.affirm_grammar(NL)
        elif isinstance(self.tok, CLASS):
            public_attributes = set()
            private_attributes = set()
            public_methods = set()
            private_methods = set()

            self.affirm_grammar(CLASS)
            name = self.affirm_grammar(IDENT, local_symbols = local_symbols)[0]
            local_symbols.add(name)

            if isinstance(self.tok, INHERITS):
                generate("(")
                if self.token_list[0].keyword not in local_symbols | self.global_symbols:
                    sys.exit("Unrecognised identifier: " + self.token_list[0].keyword + " at line " + str(self.line))
                self.affirm_grammar(INHERITS, IDENT, local_symbols = local_symbols)
                generate(")")
            generate(":")

            self.affirm_grammar(NL)

            # statements will either be:
            #  - PUBLIC/PRIVATE IDENT/FUNCTION/PROCEDURE
            #  - IDENT/FUNCTION/PROCEDURE (assumed public)

            '''
            def scope_logic():
                scope = "private" if isinstance(self.tok, PRIVATE) else "public"

                if isinstance(self.tok, PUBLIC):
                    self.affirm_grammar(PUBLIC)
                elif isinstance(self.tok, PRIVATE):
                    self.affirm_grammar(PRIVATE)

                if scope == "public":
                    if isinstance(self.tok, FUNCTION) or isinstance(self.tok, PROCEDURE):
                        public_methods.add(self.token_list[0].keyword)
                    else:
                        public_attributes.add(self.tok.keyword)
                else:
                    if isinstance(self.tok, FUNCTION) or isinstance(self.tok, PROCEDURE):
                        private_methods.add(self.token_list[0].keyword)
                    else:
                        private_attributes.add(self.tok.keyword)

                if index_token_sublist(self.token_list, (IDENT, NL)) == 0:
                    self.affirm_grammar(IDENT, NL)

                self.statement(local_symbols | public_attributes | private_attributes | public_methods | private_methods, extra_tabs = extra_tabs + 1)
                '''

            temp_local_symbols = self.statement(local_symbols | public_attributes | private_attributes | public_methods | private_methods, extra_tabs = extra_tabs + 1)
            while index_token_sublist([self.tok] + self.token_list, (*[TAB for _ in range(max(0, extra_tabs))], ENDCLASS)) != 0:
                temp_local_symbols = self.statement(temp_local_symbols | public_attributes | private_attributes | public_methods | private_methods, extra_tabs = extra_tabs + 1)
            self.affirm_tabs(extra_tabs)
            self.affirm_grammar(ENDCLASS, NL)
        elif isinstance(self.tok, SUPER):
            self.affirm_grammar(SUPER, PERIOD, nullify = True)
            generate("super().")
            if isinstance(self.tok, NEW):
                generate("__init__")
                self.call(local_symbols)
            else:
                self.affirm_grammar(IDENT)
                self.call(local_symbols)
            self.affirm_grammar(NL)
        elif isinstance(self.tok, IDENT):
            while isinstance(self.token_list[0], PERIOD):
                self.affirm_grammar(IDENT, PERIOD)

            if isinstance(self.token_list[0], OPENPAR):
                self.affirm_grammar(IDENT)
                print("flag1", local_symbols)
                self.call(local_symbols)
            else:
                local_symbols.add(self.tok.keyword)
                print("added " + self.tok.keyword)
                self.affirm_grammar(IDENT, EQ)
                self.expression(local_symbols)
            self.affirm_grammar(NL)
        elif isinstance(self.tok, (PUBLIC, PRIVATE)):
            self.affirm_grammar(PUBLIC if isinstance(self.tok, PUBLIC) else PRIVATE)
            if isinstance(self.tok, (FUNCTION, PROCEDURE)):
                temp = self.tok
                self.affirm_grammar(FUNCTION if isinstance(self.tok, FUNCTION) else PROCEDURE)

                name = self.tok.keyword
                if isinstance(self.tok, NEW):
                    self.tok.keyword = "__init__"
                    self.affirm_grammar(NEW)
                else:
                    self.affirm_grammar(IDENT)
                local_symbols.add(name)


                self.token_list.insert(0, IDENT("self"))
                if isinstance(self.token_list[1], IDENT):
                    self.token_list.insert(1, COMMA())
                print(self.token_list[:10])
                temp_local_symbols = self.call(local_symbols)
                generate(":")
                self.affirm_grammar(NL)

                temp_local_symbols = self.statement(local_symbols | temp_local_symbols, extra_tabs=extra_tabs + 1)
                while index_token_sublist([self.tok] + self.token_list, (*[TAB for _ in range(max(0, extra_tabs))],
                                                                         ENDFUNCTION if isinstance(temp,
                                                                                                   FUNCTION) else ENDPROCEDURE)) != 0:
                    temp_local_symbols = self.statement(local_symbols | temp_local_symbols, extra_tabs=extra_tabs + 1)

                self.affirm_tabs(extra_tabs)
                self.affirm_grammar(ENDFUNCTION if isinstance(temp, FUNCTION) else ENDPROCEDURE, NL)
            else:
                local_symbols = self.statement(local_symbols)
        elif isinstance(self.tok, COMMENT):
            self.affirm_grammar(COMMENT, NL)
        elif isinstance(self.tok, NL):
            self.affirm_grammar(NL)
        else:
            sys.exit("Unrecognised Token: " + str(type(self.tok)) + " at line " + str(self.line))

        return local_symbols

    def comparison(self, local_symbols):
        if isinstance(self.tok, NOT):
            self.affirm_grammar(NOT)

        def single():
            self.expression(local_symbols)
            if isinstance(self.tok, (EQEQ, GT, GTEQ, LT, LTEQ, NOTEQ)):
                self.affirm_grammar(type(self.tok))
            else:
                sys.exit("Must include a comparison operator at line " + str(self.line))
            self.expression(local_symbols)

        single()
        while isinstance(self.tok, (AND, OR)):
            self.affirm_grammar(type(self.tok))
            single()

    def expression(self, local_symbols):
        flag = False
        if isinstance(self.tok, OPENPAR):
            self.affirm_grammar(OPENPAR)
            flag = True

        self.term(local_symbols)
        while isinstance(self.tok, (PLUS, MINUS)):
            self.affirm_grammar(type(self.tok))
            self.term(local_symbols)

        if flag:
            self.affirm_grammar(CLOSEPAR)


    def term(self, local_symbols):
        self.unary(local_symbols)
        while isinstance(self.tok, (ASTERISK, SLASH, DIV, MOD)):
            self.affirm_grammar(type(self.tok))
            self.unary(local_symbols)

    def unary(self, local_symbols):
        if isinstance(self.tok, (PLUS, MINUS)):
            self.affirm_grammar(type(self.tok))
        self.primary(local_symbols)

    def primary(self, local_symbols):
        if isinstance(self.tok, (INT, FLOAT, STR, BOOL)):
            self.affirm_grammar(type(self.tok), local_symbols = local_symbols)
        elif isinstance(self.tok, IDENT):
            print(self.tok.keyword, local_symbols, self.global_symbols)
            if self.tok.keyword not in local_symbols and self.tok.keyword not in self.global_symbols:
                sys.exit("Unrecognised identifier: " + self.tok.keyword + " at line " + str(self.line))
            while isinstance(self.token_list[0], PERIOD):
                self.affirm_grammar(IDENT, PERIOD)
            self.affirm_grammar(IDENT)
            if isinstance(self.tok, OPENPAR):
                self.call(local_symbols)
        elif isinstance(self.tok, OPENPAR):
            self.expression(local_symbols)
        else:
            sys.exit("Illegal primary: " + self.tok.keyword + ", of type: " + str(type(self.tok)) + " at line " + str(self.line))

    def program(self):
        # calls statement until the EOF (end of file) token is met
        # (and adds all returned values to the global symbols)

        while not isinstance(self.tok, EOF):
            self.global_symbols |= self.statement()
        generator.write(input_path)

        print("Successfully finished compiling.")

if __name__ == '__main__':
    input_path = "test2.ocr"
    with open(input_path, "r") as file:
        source_code = file.read()

    lexer = Lexer(source_code)
    a = lexer.Lex()
    '''for i in split_list_by_element(a, NL):
        print(type(o) for o in i)'''

    parser = Parser(a)

    parser.program()
