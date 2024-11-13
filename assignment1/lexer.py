"""
__author__ = "Jieung Kim", "SoonWon Moon", "Jay Hwan Lee"
__copyright__ = "Copyright 2024, Jieung Kim, SoonWon Moon, Jay Hwan Lee"
__credits__ = ["Jieung Kim", "SoonWon Moon", "Jay Hwan Lee"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Jieung Kim"
__email__ = "jieungkim@yonsei.ac.kr"
"""
# This file implements a lexer for ToyPL, which is described in our README file.
import ply.lex as lex
import sys

# Reserved keywords and token definitions. You should not touch them.
reserved = {
    "namespace": "NAMESPACE",
    "const": "CONST",
    "var": "VAR",
    "func": "FUNC",
    "begin": "BEGIN",
    "end": "END",
    "skip": "SKIP",
    "read": "READ",
    "print": "PRINT",
    "call": "CALL",
    "if": "IF",
    "then": "THEN",
    "else": "ELSE",
    "while": "WHILE",
    "do": "DO",
    "return": "RETURN"
}

tokens = [
    # separators
    "COMMA",  # ,
    "COLON",  # :
    "SEMICOLON",  # ;
    "PERIOD",  # .
    "LPAR",  # (
    "RPAR",  # )
    "LBRC",  # {
    "RBRC",  # }
    # arithmetic operators
    "PLUS",  # +
    "MINUS",  # -
    "MUL",  # *
    "DIV",  # /
    "MOD",  # %
    # comparison operators
    "EQ",  # ==
    "NE",  # /=
    "LT",  # <
    "LE",  # <=
    "GT",  # >
    "GE",  # >=
    # boolean operators
    "OR",  # ||
    "AND",  # &&
    # assignments
    "DEFINE",  # :=
    "ASSIGN",  # <-
    # tokens that has to be defined with action functions
    "NIDENT",
    "LIDENT",
    "NUMBER",
] + list(reserved.values())

################################################################
# HW1 part start
# MODIFY THE FOLLOWING PARTS AND FILL OUT WITH YOUR OWN DEFINITIONS
# To see how results are generated, refer to the test oracles in 
# the [assessment] directory.
################################################################
t_COMMA = r","
t_COLON = r":"
t_SEMICOLON = r";"
t_PERIOD = r"\."
t_LPAR = r"\("
t_RPAR = r"\)"
t_LBRC = r"\{"
t_RBRC = r"\}"
t_PLUS = r"\+"
t_MINUS = r"-"
t_MUL = r"\*"
t_DIV = r"/"
t_MOD = r"%"
t_EQ = r"=="
t_NE = r"/="
t_LT = r"<"
t_LE = r"<="
t_GT = r">"
t_GE = r">="
t_OR = r"\|\|"
t_AND = "&&"
t_DEFINE = r":="
t_ASSIGN = r"<-"
t_NIDENT = r"[A-Z][a-zA-Z_0-9]*"
t_ignore = " \t"

# Global variable for storing error messages.
error_message = ""

# When checking the keyword, error handling requires several steps 
# using user-defined functions, which are not provided in this code. 
# You will need to implement these functions yourself.

# The process performs the following actions:
# 1. If the recognized lexeme is similar to the keyword (e.g., the keyword can be formed by 
#    (1) transposing two adjacent characters, 
#    (2) adding one character - when the keyword length is greater than 2, or 
#    (3) deleting one character),
#    the lexer will automatically correct the lexeme to the intended keyword.
# 2. If the lexeme does not match these criteria, it will be treated as an identifier. 
#    However, if the lexeme exceeds 79 characters in length, it will be truncated to that limit.

# Maximum identifier length
MAX_IDENTIFIER_LENGTH = 79

# Check if two lexemes differ by one character replacement
def is_one_character_replacement(lexeme):
    for keyword in list(reserved.keys()):
        if len(lexeme) != len(keyword):
            continue
        if any(lexeme[:i] + lexeme[i + 1:] == keyword[:i] + keyword[i + 1:] for i in range(len(lexeme))):
            return keyword

    return None

# Check if two lexemes differ by one character deletion
def is_one_character_deletion(lexeme):
    for keyword in list(reserved.keys()):
        if len(lexeme) != len(keyword) + 1:
            continue
        if any(lexeme[:i] + lexeme[i + 1:] == keyword for i in range(len(lexeme))):
            return keyword

    return None

# Check if two lexemes differ by one character addition
def is_one_character_addition(lexeme):
    for keyword in list(reserved.keys()):
        if len(lexeme) != len(keyword) - 1 or len(keyword) <= 2:
            continue
        if any(keyword[:i] + keyword[i + 1:] == lexeme for i in range(len(keyword))):
            return keyword

    return None

# Check if two adjacent characters are transposed
def is_adjacent_character_transposition(lexeme):
    for keyword in list(reserved.keys()):
        if len(lexeme) != len(keyword):
            continue
        if any(lexeme[:i] + lexeme[i + 1] + lexeme[i] + lexeme[i + 2:] \
            == keyword for i in range(len(lexeme) - 1)):
            return keyword

    return None

def t_RESERVED(t):
    r'([a-z_][a-zA-Z_0-9]*)'
    global error_message
    lexeme = t.value

    if len(lexeme) > MAX_IDENTIFIER_LENGTH:
        new_error_message = "Long identifier '%s'" % lexeme
        error_message = error_message + "\n" + new_error_message
        lexeme = lexeme[:MAX_IDENTIFIER_LENGTH]  # Truncate lexeme if it exceeds the limit
        t.value = lexeme

    replace = is_one_character_replacement(lexeme)
    transpose = is_adjacent_character_transposition(lexeme)
    addition = is_one_character_addition(lexeme)
    deletion = is_one_character_deletion(lexeme)

    if lexeme in list(reserved.keys()):                     # matches with keyword
        t.type = reserved[lexeme]
    elif isinstance(replace, str):
        new_error_message = "Char replace: %s -> %s" % (lexeme, replace)
        error_message = error_message + "\n" + new_error_message
        t.type = reserved[replace]
        t.value = replace
    elif isinstance(transpose, str):    # rule 1 case
        new_error_message = "Char transpose: %s -> %s" % (lexeme, transpose)
        error_message = error_message + "\n" + new_error_message
        t.type = reserved[transpose]
        t.value = transpose
    elif isinstance(addition, str):     # rule 2 case
        new_error_message = "Char insert: %s -> %s" % (lexeme, addition)
        error_message = error_message + "\n" + new_error_message
        t.type = reserved[addition]
        t.value = addition
    elif isinstance(deletion, str):     # rule 3 case
        new_error_message = "Char remove: %s -> %s" % (lexeme, deletion)
        error_message = error_message + "\n" + new_error_message
        t.type = reserved[deletion]
        t.value = deletion
    else:                               # LIDENT
        t.type = "LIDENT"
    return t

# The number must be representable within 32 bits. If it isn't, an error message will be generated, 
# and the token's value (attribute) will be set to 0.
def t_NUMBER(t):
    r'[0-9]+'
    val = int(t.value)
    if 0xffffffff >= val and val >= 0x00000000:
        t.value = val
        return t
    else:
        global error_message
        new_error_message = "Large number size '%s'" % t.value
        error_message = error_message + "\n" + new_error_message
        t.value = 0
        return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# This function doesn't require any changes. 
# It only demonstrates how to incorporate error messages during assignment.
def t_error(t):
    global error_message 
    new_error_message = "Illegal character '%s'" % t.value[0]
    error_message = error_message + "\n" + new_error_message
    t.lexer.skip(1)

def t_comment(t):
    r'\#.*'
    pass  # No return value. Token discarded.

################################################################
# HW1 part end
################################################################

# Do not touch after this line
# Create a lexer
lexer = lex.lex()

def initialize_error_message():
    global error_message
    error_message = "ERRORS:\n"

def lex_str(s):
    lexer.input(s)
    lexer.lineno = 1
    ts = []
    while True:
        t = lexer.token()
        if t:
            ts.append(t)
        else:
            lexer.lineno = 1
            return ts

def main(filename):
    initialize_error_message()
    file_obj = open(filename, "r")
    inputs = file_obj.read()
    file_obj.close()
    tok_list = lex_str(inputs)
    print(error_message)
    print(tok_list)

if __name__ == "__main__":
    filename = sys.argv[1]
    main(filename)
