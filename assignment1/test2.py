import ply.lex as lex

# List of reserved keywords
reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE'
}

# List of token names including reserved keywords
tokens = [
    'ID',       # Identifiers (variables)
    'NUMBER',   # Numbers
    'PLUS',     # +
    'MINUS',    # -
    'TIMES',    # *
    'DIVIDE',   # /
    'LPAREN',   # (
    'RPAREN',   # )
] + list(reserved.values())  # Add reserved keywords to the list of tokens

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
    t.value = int(t.value)  # Convert the token value to an integer
    return t

# A rule to handle identifiers and reserved keywords
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'  # Regular expression for identifiers
    t.type = reserved.get(t.value, 'ID')  # Check if the identifier is a reserved word
    return t

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

# Test input string containing identifiers, numbers, and keywords
data = '''
if x + 10 > 5:
    while y - 2:
        x = x * 3
else:
    y = y / 2
'''

# Pass the input string to the lexer
lexer.input(data)

# Tokenize and print each token
while True:
    tok = lexer.token()
    if not tok:
        break  # No more input
    print(tok)
