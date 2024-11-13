import ply.lex as lex

# List of token names
tokens = [
    'ID',
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN'
]

# Regular expressions for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'

# A rule to match numbers (integers)
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Rule for identifiers
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = 'ID'
    return t

# Rule to ignore comments that start with #
def t_COMMENT(t):
    r'\#.*'
    pass  # No return value. Token discarded.

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Test input string with a comment
data = '''
x = 10 + 20 # This is a comment
y = x - 5 # Another comment
'''

# Pass the input string to the lexer
lexer.input(data)

# Tokenize and print each token
while True:
    tok = lexer.token()
    if not tok:
        break  # No more input
    print(tok)
