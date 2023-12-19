import sys
from Tokens import *

def index_token_sublist(lst, sublist):
    # returns the index of the first instance of a sublist of tokens in a token list
    # e.g. the index of
    # [TAB, PRINT] in
    # [IF, COMPARISON, THEN, NL, TAB, PRINT, OPENPAR, IDENT, CLOSEPAR, NL, ENDIF, NL EOF]
    # is 4
    try:
        # ;) very readable
        return list(zip(*[list(map(type, lst))[i:len(lst)-len(sublist)+i+1] for i in range(len(sublist))])).index(sublist)
    except:
        return -1



class Parser:

    def __init__(self, token_list, generator):
        self.generator = generator
        self.token_list = token_list
        self.tok = self.next_token()
        self.global_symbols = {"print", "input", "openRead", "openWrite", "int", "str", "bool", "float"}
        self.classes = set()
        self.line = 1

    def generate(self, code):
        self.generator.generate(code)

    def next_token(self):
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
            self.affirm_grammar(WHILE)
            self.comparison(local_symbols)
            self.generate(":")
            self.affirm_grammar(NL)

            local_symbols = self.statement(local_symbols, extra_tabs = extra_tabs + 1)
            while index_token_sublist([self.tok] + self.token_list, (*[TAB for _ in range(max(0, extra_tabs))], ENDWHILE)) != 0:
                local_symbols = self.statement(local_symbols, extra_tabs = extra_tabs + 1)
            self.affirm_tabs(extra_tabs)
            self.affirm_grammar(ENDWHILE, NL)
        elif isinstance(self.tok, FOR):
            iterator = self.affirm_grammar(FOR, IDENT)[1]
            self.generate(' in range(')
            self.affirm_grammar(EQ, nullify=True)
            self.affirm_grammar(INT, local_symbols = local_symbols)
            self.generate(", ")
            self.affirm_grammar(TO, nullify=True)
            self.affirm_grammar(INT, local_symbols = local_symbols)
            self.generate("):")
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
            self.generate("while not (")

            pos = index_token_sublist(self.token_list, (NL, *[TAB for _ in range(extra_tabs)], UNTIL)) + extra_tabs + 1
            temp, self.token_list = self.token_list[:pos], self.token_list[pos:]

            self.affirm_grammar(TAB, UNTIL, nullify = True)
            self.comparison(local_symbols)
            self.generate("):")
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
            self.generate(":")
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
                self.generate("(")
                if self.token_list[0].keyword not in local_symbols | self.global_symbols:
                    sys.exit("Unrecognised identifier: " + self.token_list[0].keyword + " at line " + str(self.line))
                self.affirm_grammar(INHERITS, IDENT, local_symbols = local_symbols)
                self.generate(")")
            self.generate(":")

            self.affirm_grammar(NL)

            temp_local_symbols = self.statement(local_symbols | public_attributes | private_attributes | public_methods | private_methods, extra_tabs = extra_tabs + 1)
            while index_token_sublist([self.tok] + self.token_list, (*[TAB for _ in range(max(0, extra_tabs))], ENDCLASS)) != 0:
                temp_local_symbols = self.statement(temp_local_symbols | public_attributes | private_attributes | public_methods | private_methods, extra_tabs = extra_tabs + 1)
            self.affirm_tabs(extra_tabs)
            self.affirm_grammar(ENDCLASS, NL)
        elif isinstance(self.tok, SUPER):
            self.affirm_grammar(SUPER, PERIOD, nullify = True)
            self.generate("super().")
            if isinstance(self.tok, NEW):
                self.generate("__init__")
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
                self.call(local_symbols)
            else:
                local_symbols.add(self.tok.keyword)
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
                temp_local_symbols = self.call(local_symbols)
                self.generate(":")
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

        print("Successfully finished compiling.")
