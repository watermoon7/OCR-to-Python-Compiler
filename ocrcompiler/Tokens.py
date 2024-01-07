from Generator import *

class Token:
    def generate(self, nullify = False):
        generator.generate(self)

    def __repr__(self):
        return str(self.__class__.__name__)

# Symbols
class OPENPAR(Token):
    def __init__(self, nullify = False):
        self.keyword = "" if nullify else "("

class CLOSEPAR(Token):
    def __init__(self, nullify = False):
        self.keyword = "" if nullify else ")"

class APOST(Token):
    def __init__(self, nullify = False):
        self.keyword = "" if nullify else "'"

class NL(Token):
    def __init__(self, nullify = False):
        self.keyword = "" if nullify else "\n"

class OPENSQR(Token):
    def __init__(self, nullify = False):
        self.keyword = "" if nullify else "["

class CLOSESQR(Token):
    def __init__(self, nullify = False):
        self.keyword = "" if nullify else "]"

class COLON(Token):
    def __init__(self, nullify = False):
        self.keyword = "" if nullify else ":"

class PERIOD(Token):
    def __init__(self, nullify = False):
        self.keyword = "" if nullify else "."

class EQ(Token):
    def __init__(self, nullify = False):
        self.keyword = "" if nullify else " = "

class COMMA(Token):
    def __init__(self, nullify = False):
        self.keyword = "" if nullify else ", "

# Operators
class PLUS(Token):
    def __init__(self, nullify = False):
        self.keyword = "" if nullify else "+"

class MINUS(Token):
    def __init__(self, nullify = False):
        self.keyword = "" if nullify else "-"

class ASTERISK(Token):
    def __init__(self, nullify = False):
        self.keyword = "" if nullify else " * "

class SLASH(Token):
    def __init__(self, nullify = False):
        self.keyword = "" if nullify else " / "

class MOD(Token):
    def __init__(self, nullify = False):
        self.keyword = "" if nullify else "MOD"

class DIV(Token):
    def __init__(self, nullify = False):
        self.keyword = "" if nullify else "DIV"

class CARAT(Token):
    def __init__(self, nullify = False):
        self.keyword = "" if nullify else "^"

class EQEQ(Token):
    def __init__(self, nullify = False):
        self.keyword = "" if nullify else " == "

class NOTEQ(Token):
    def __init__(self, nullify = False):
        self.keyword = "" if nullify else " != "

class LT(Token):
    def __init__(self, nullify = False):
        self.keyword = "" if nullify else " < "

class GT(Token):
    def __init__(self, nullify = False):
        self.keyword = "" if nullify else " > "

class LTEQ(Token):
    def __init__(self, nullify = False):
        self.keyword = "" if nullify else " <= "

class GTEQ(Token):
    def __init__(self, nullify = False):
        self.keyword = "" if nullify else " >= "


# Keywords
class PRINT(Token):
    def __init__(self, nullify = False):
        self.keyword = "" if nullify else "print"

class IF(Token):
    def __init__(self, nullify = False):
        self.keyword = "" if nullify else "if "

class ELIF(Token):
    def __init__(self, nullify = False):
        self.keyword = "" if nullify else "elif "

class ELSE(Token):
    def __init__(self, nullify = False):
        self.keyword = "" if nullify else "else"

class THEN(Token):
    def __init__(self, nullify = False):
        self.keyword = "" if nullify else ":"

class ENDIF(Token):
    def __init__(self, nullify = False):
        self.keyword = ""

class WHILE(Token):
    def __init__(self, nullify = False):
        self.keyword = "" if nullify else "while "

class ENDWHILE(Token):
    def __init__(self, nullify = False):
        self.keyword = ""

class FOR(Token):
    def __init__(self, nullify = False):
        self.keyword = "" if nullify else "for "

class TO(Token):
    def __init__(self, nullify = False):
        self.keyword = "" if nullify else " to "

class NEXT(Token):
    def __init__(self, nullify = False):
        self.keyword = ""

class DO(Token):
    def __init__(self, nullify = False):
        self.keyword = "" if nullify else "while "

class UNTIL(Token):
    def __init__(self, nullify = False):
        self.keyword = ""

class SWITCH(Token):
    def __init__(self, nullify = False):
        self.keyword = "" if nullify else "match "

class ENDSWITCH(Token):
    def __init__(self, nullify = False):
        self.keyword = ""

class CASE(Token):
    def __init__(self, nullify = False):
        self.keyword = "" if nullify else "case "

class DEFAULT(Token):
    def __init__(self, nullify = False):
        self.keyword = "" if nullify else "case _"

class FUNCTION(Token):
    def __init__(self, nullify = False):
        self.keyword = "" if nullify else "def "

class ENDFUNCTION(Token):
    def __init__(self, nullify = False):
        self.keyword = ""

class RETURN(Token):
    def __init__(self, nullify = False):
        self.keyword = "" if nullify else "return "

class PROCEDURE(Token):
    def __init__(self, nullify = False):
        self.keyword = "" if nullify else "def "

class ENDPROCEDURE(Token):
    def __init__(self, nullify = False):
        self.keyword = ""

class CLASS(Token):
    def __init__(self, nullify = False):
        self.keyword = "" if nullify else "class "

class INHERITS(Token):
    def __init__(self, nullify = False):
        self.keyword = "" if nullify else ""

class PUBLIC(Token):
    def __init__(self, nullify = False):
        self.keyword = ""

class PRIVATE(Token):
    def __init__(self, nullify = False):
        self.keyword = ""

class SUPER(Token):
    def __init__(self, nullify = False):
        self.keyword = "" if nullify else "super()."

class ENDCLASS(Token):
    def __init__(self, nullify = False):
        self.keyword = ""

class NEW(Token):
    def __init__(self, text = "", nullify = False):
        self.keyword = ""

class AND(Token):
    def __init__(self, text = "", nullify = False):
        self.keyword = "" if nullify else " and "

class OR(Token):
    def __init__(self, text = "", nullify = False):
        self.keyword = "" if nullify else " or "

class NOT(Token):
    def __init__(self, text = "", nullify = False):
        self.keyword = "" if nullify else " not "

# Other ---
class TAB(Token):
    def __init__(self, nullify = False):
        self.keyword = "" if nullify else "    "

class INT(Token):
    def __init__(self, text = "", nullify = False):
        self.keyword = "" if nullify else text

class FLOAT(Token):
    def __init__(self, text = "", nullify = False):
        self.keyword = "" if nullify else text

class STR(Token):
    def __init__(self, text = "", nullify = False):
        self.keyword = "" if nullify else "\"" + text + "\""

class BOOL(Token):
    def __init__(self, text = "", nullify = False):
        self.keyword = "" if nullify else text

class IDENT(Token):
    # TYPES INCLUDE
    # - Integer, float, string, boolean (basic type)
    # - Function/ procedure
    # - Object
    # - Reference

    def __init__(self, text = "", type_ = None, nullify = False):
        self.type = type_
        self.keyword = "" if nullify else text

class COMPARISON(Token):
    def __init__(self, text = "", nullify = False):
        self.keyword = "" if nullify else text

class EXPRESSION(Token):
    def __init__(self, text = "", nullify = False):
        self.keyword = "" if nullify else text

class COMMENT(Token):
    def __init__(self, text = "", nullify = False):
        self.keyword = "" if nullify else "# " + text

class EOF(Token):
    def __init__(self, nullify = False):
        self.keyword = ""


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
