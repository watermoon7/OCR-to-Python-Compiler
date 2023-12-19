import sys
from Tokens import *

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
        print("Successfully finished lexing.")
        return token_list