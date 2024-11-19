"""
__author__ = "Jieung Kim", "SoonWon Moon", "Jay Hwan Lee"
__copyright__ = "Copyright 2024, Jieung Kim, SoonWon Moon, Jay Hwan Lee"
__credits__ = ["Jieung Kim", "SoonWon Moon", "Jay Hwan Lee"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Jieung Kim"
__email__ = "jieungkim@yonsei.ac.kr"
"""
# This file implements a parser for ToyPL, which is described in our README file.
import ply.yacc as yacc
import ply.lex as lex
from lexer import *
import sys

################################################################
# HW2 part start
# MODIFY THE FOLLOWING PARTS AND FILL OUT WITH YOUR OWN DEFINITIONS
# To see how results are generated, refer to the test oracles in 
# the [assessment] directory.
################################################################

###############################################################
# Program
###############################################################
# This is an example of how to make a parsing function to generate
# the corresponding AST with the following production rule:
# PROGRAM -> NAMESPACE_DECS CONST_DECS VAR_DECS FUNC_DECS


def p_program(p):
    """
    program : namespace_decs const_decs var_decs func_decs
    """
    p[0] = ("program", p[1], p[2], p[3], p[4])


###############################################################
# Namespace
###############################################################
# Implement functions to check the following rules 


def p_namespace_decs(p):
    """
    namespace_decs : empty 
    | namespace_dec namespace_decs
    """
    if p[1]==None:
        p[0] = []
    elif len(p)==3:
        p[0] = [p[1]] + p[2]

def p_namespace_dec(p):
    """
    namespace_dec : NAMESPACE NIDENT namespace_decs const_decs var_decs func_decs END
    """
    p[0] = ("namespace", p[2], p[3], p[4], p[5], p[6])

###############################################################
# Constants
###############################################################
# Implement functions to check the following rules 

# CONST_DECS -> E | "const" CONSTS
def p_const_decs(p):
    """
    const_decs : empty
    | CONST consts
    """
    if p[1]==None:
        p[0] = []
    elif len(p)==3:
        p[0] = p[2]
        
# CONSTS -> LIDENT ":=" NUMBER | LIDENT ":=" NUMBER "," CONSTS
def p_consts(p):
    """
    consts : LIDENT DEFINE NUMBER
    | LIDENT DEFINE NUMBER COMMA consts
    """
    if len(p)==4:
        p[0] = [(p[1], p[3])]
    else:
        p[0] = [(p[1], p[3])] + p[5]

###############################################################
# Variables
###############################################################
# Implement functions to check the following rules 

# VAR_DECS -> E | "var" VARS
def p_var_decs(p):
    """
    var_decs : empty
    | VAR vars
    """
    if p[1]==None:
        p[0] = []
    elif len(p)==3:
        p[0] = p[2]

# VARS -> LIDENT | LIDENT "," VARS
def p_vars(p):
    """
    vars : LIDENT
    | LIDENT COMMA vars
    """
    if len(p)==2:
        p[0] = [p[1]]
    elif len(p)==4:
        p[0] = [p[1]] + p[3]

###############################################################
# Functions
###############################################################
# Implement functions to check the following rules 

# FUNC_DECS -> E | FUNC_DEC FUNC_DECS
def p_func_decs(p):
    """
    func_decs : empty
    | func_dec func_decs
    """
    if p[1]==None:
        p[0] = []
    elif len(p)==3:
        p[0] = [p[1]] + p[2]

# FUNC_DEC -> "func" LIDENT "(" PARAMS ")" CONST_DECS VAR_DECS "begin" STMTS "end"
def p_func_dec(p):
    """
    func_dec : FUNC LIDENT LPAR params RPAR const_decs var_decs BEGIN stmts END
    """
    p[0] = ("func", p[2], p[4], p[6], p[7], p[9])
    
# PARAMS -> E | LIDENT PARAMS_TAIL
def p_params(p):
    """
    params : empty
    | LIDENT params_tail
    """
    if p[1]==None:
        p[0] = []
    elif len(p)==3:
        p[0] = [p[1]] + p[2]
        
# PARAMS_TAIL -> E | "," LIDENT PARAMS_TAIL
def p_params_tail(p):
    """
    params_tail : empty
    | COMMA LIDENT params_tail
    """
    if p[1]==None:
        p[0] = []
    elif len(p)==4:
        p[0] = [p[2]] + p[3]

###############################################################
# Statement definitions
###############################################################
# Implement functions to check the following rules 
# NOTE: Most cases in this assignment requires a simple method 
# that generate AST by using the result of parsing. However, 
# we may need additional routine for the assignment statement 
# to check the validity of the assignment statement and report 
# the error. 

# STMT -> "skip"
#       | IDENT "<-" "read"
#       | "print" "(" EXPR ")"
#       | IDENT "<-" EXPR
#       | IDENT "<-" "call" IDENT "(" ARGS ")"
#       | "if" BEXPR "then" STMT "else" STMT
#       | "while" BEXPR "do" STMT
#       | "return" EXPR
#       | "{" STMTS "}"
def p_stmt(p):
    """
    stmt : SKIP
    | ident ASSIGN READ
    | PRINT LPAR expr RPAR
    | ident ASSIGN expr
    | ident ASSIGN term mul factor
    | ident ASSIGN term div factor
    | ident ASSIGN CALL ident LPAR args RPAR
    | IF bexpr THEN stmt ELSE stmt
    | WHILE bexpr DO stmt
    | RETURN expr 
    | LBRC stmts RBRC

    """
    if len(p)==2:
        p[0] = ("skip", )
    elif len(p)==5:
        if p[1]=="print":
            p[0] = ("print", p[3])
        else:
            p[0] = ("while", p[2], p[4])
    elif len(p)==4:
        if p[1]=="{":
            p[0] = ("stmts", p[2])
        elif p[2]=="<-" and p[3]=="read":  
            p[0] = ("read", p[1])
        elif p[2]=="<-":
            p[0] = ("assign", p[1], p[3])
    elif len(p)==6:
        p[0] = ("assign", p[1], (p[4], p[3], p[5]))
    elif len(p)==8:
        p[0] = ("call", p[1], p[4], p[6])
    elif len(p)==7:
        p[0] = ("if", p[2], p[4], p[6])
    elif len(p)==3:
        p[0] = ("return", p[2])

# STMTS -> STMT | STMT ";" | STMT ";" STMTS
def p_stmts(p):
    """
    stmts : stmt
    | stmt SEMICOLON
    | stmt SEMICOLON stmts
    """
    if len(p)==2:
        p[0] = [p[1]]
    elif len(p)==3:
        p[0] = [p[1]] 
    elif len(p)==4:
        p[0] = [p[1]] + p[3]
        
# ARGS -> E | EXPR ARGS_TAIL
def p_args(p):
    """
    args : empty
    | expr args_tail
    """
    if p[1]==None:
        p[0] = []
    elif len(p)==3:
        p[0] = [p[1]] + p[2]

# ARGS_TAIL -> E | "," EXPR ARGS
def p_args_tail(p):
    """
    args_tail : empty
    | COMMA expr args
    """
    if p[1]==None:
        p[0] = []
    elif len(p)==4:
        p[0] = [p[2]] + p[3]

###############################################################
# Boolean expressions
###############################################################
# Implement functions to handle the following rules

# CMP_OP -> "==" | "/=" | "<" | "<=" | ">" | ">="
def p_cmp_op(p):
    """
    cmp_op : EQ
    | NE
    | GT
    | GE
    | LT
    | LE
    """

    p[0] = p[1] 

# BEXPR -> BTERM | BEXPR "||" BTERM
def p_bexpr(p):
    """
    bexpr : bterm
    | bexpr OR bterm
    """
    if len(p)==2:
        p[0] = p[1]
    elif len(p)==4:
        p[0] = ("or", p[1], p[3])

# BTERM -> BFACTOR | BTERM "&&" BFACTOR
def p_bterm(p):
    """
    bterm : bfactor
    | bterm AND bfactor
    """
    if len(p)==2:
        p[0] = p[1]
    elif len(p)==4:
        p[0] = ("and", p[1], p[3])

# BFACTOR -> EXPR CMP_OP EXPR | "(" BEXPR ")"
def p_bfactor(p):
    """
    bfactor : expr cmp_op expr
    | LPAR bexpr RPAR
    """
    if p[1]=="(" and p[3]==")":
        p[0] = p[2]
    else:
        p[0] = (p[2], p[1], p[3])

###############################################################
# Arithmetic expressions
###############################################################
# Implement functions to handle the following rules

# EXPR -> TERM | EXPR "+" TERM | EXPR "-" TERM
def p_expr(p):
    """
    expr : term
    | expr plus term
    | expr minus term
    """
    if len(p)==2:
        p[0] = p[1]
    elif len(p)==4:
        p[0] = (p[2], p[1], p[3])

def p_plus(p):
    """
    plus : PLUS
    """
    p[0] = p[1]
def p_minus(p):
    """
    minus : MINUS 
    """
    p[0] = p[1]
        
# TERM -> FACTOR | TERM "*" FACTOR | TERM "/" FACTOR | TERM "%" FACTOR
def p_term(p):
    """
    term : factor
    | term mul factor
    | term div factor
    | term mod factor
    """
    if len(p)==2:
        p[0] = p[1]
    elif len(p)==4:
        p[0] = (p[2], p[1], p[3])

def p_mul(p):
    """
    mul : MUL
    """
    p[0] = p[1]

def p_div(p):
    """
    div : DIV
    """
    p[0] = p[1]

def p_mod(p):
    """
    mod : MOD
    """
    p[0] = p[1]
# FACTOR -> IDENT | NUMBER | "(" EXPR ")"
def p_factor(p):
    """
    factor : NUMBER
    | ident
    | LPAR expr RPAR
    """
    if isinstance(p[1], int):
        p[0] = ("number", p[1])
    elif p[1]=="(":
        p[0] = p[2]
    else:
        p[0] = ("var", p[1])

###############################################################
# Identifiers
###############################################################
# Implement functions to handle the following rules
 
# IDENT -> ABS_PATH LIDENT | REL_PATH LIDENT
def p_ident_abs(p):
    """
    ident : abs_path LIDENT
    """
    p[0] = ("abs", p[1], p[2])
def p_ident_rel(p):
    """
    ident : rel_path LIDENT
    """
    p[0] = ("rel", p[1], p[2])

# ABS_PATH -> ":" REL_PATH
def p_abs_path(p):
    """
    abs_path : COLON rel_path
    """
    p[0] = p[2]

# REL_PATH -> E | NIDENT "." REL_PATH
def p_rel_path(p):
    """
    rel_path : empty
    | NIDENT PERIOD rel_path
    """
    if p[1]==None:
        p[0] = []
    elif len(p)==4:
        p[0] = [p[1]] + p[3]


###############################################################
# Error Reporter and Handler (Panic Mode Recovery)
###############################################################
# Global variable for storing error messages.
error_message = ""

def error_reporter(message):
    global error_message
    new_error_message = message
    error_message = error_message + "\n" + new_error_message

# Synchronization tokens for our panic mode recovery are as follows:
# ",", ":", ";", ".", "(", ")", "{", "}" 
def p_error(p):
    global error_message
    if p:
        # Report the error with details about the offending token
        error_reporter(f"Error in line '{p}'")
        
        # Synchronize: Skip tokens until a synchronization token is found
        while True:
            tok = parser.token()  # Get the next token
            if not tok or tok.value in [',', ':', ';', '.', '(', ')', '{', '}']:
                break
        
        error_reporter(f"Recovered to next {tok.type} at Line {tok.lineno}.")
        tok = parser.token()
        parser.errok()
        return tok
        
    else:
        # Handle unexpected end of input
        error_reporter("Syntax error at end of input")
        return

################################################################
# HW2 part end
# NOTE: do not touch the remaining parts of this file.
###############################################################
###############################################################
# Empty rule
###############################################################
def p_empty(p):
    """
    empty :
    """

###############################################################
# Generate the parser and test it
###############################################################
parser = yacc.yacc()

def initialize_error_message():
    global error_message
    error_message = "ERRORS:\n"

def main(filename):
    initialize_error_message()
    file_obj = open(filename, "r")
    inputs = file_obj.read()
    file_obj.close()
    ast = parser.parse(inputs)
    print(error_message)
    print(ast)


if __name__ == "__main__":
    filename = sys.argv[1]
    main(filename)
