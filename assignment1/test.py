import ply.lex as lex

# List of token names. This is always required
tokens = (
    'NUMBER',      # Token for numbers
    'PLUS',        # Token for '+'
    'MINUS',       # Token for '-'
    'TIMES',       # Token for '*'
    'DIVIDE',      # Token for '/'
    'LPAREN',      # Token for '('
    'RPAREN'       # Token for ')'
)

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'

# A rule to recognize numbers (integers)
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    # Convert the token to an integer
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Test input string
data = '3 + 4 * (10 - 2) / 5'

# Pass the data to the lexer
lexer.input(data)

# Tokenize the input string
while True:
    tok = lexer.token()
    if not tok:
        break      # No more input
    print(tok)
