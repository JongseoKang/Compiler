import ply.lex as lex
import difflib

# List of reserved keywords
reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'return': 'RETURN'
}

# Maximum identifier length
MAX_IDENTIFIER_LENGTH = 79

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
] + list(reserved.values())

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

# Function to check if a lexeme is close to a keyword
def correct_lexeme(lexeme):
    if len(lexeme) > MAX_IDENTIFIER_LENGTH:
        lexeme = lexeme[:MAX_IDENTIFIER_LENGTH]  # Truncate lexeme if it exceeds the limit

    # Find close matches with reserved keywords (allowing small errors)
    close_matches = difflib.get_close_matches(lexeme, reserved.keys(), n=1, cutoff=0.8)
    
    if close_matches:
        corrected_keyword = close_matches[0]
        if is_one_character_addition(lexeme, corrected_keyword) or \
           is_one_character_deletion(lexeme, corrected_keyword) or \
           is_adjacent_character_transposition(lexeme, corrected_keyword):
            return reserved[corrected_keyword]
    
    return None

# Check if two lexemes differ by one character addition
def is_one_character_addition(lexeme, keyword):
    return len(lexeme) == len(keyword) + 1 and any(
        lexeme[:i] + lexeme[i + 1:] == keyword for i in range(len(lexeme)))

# Check if two lexemes differ by one character deletion
def is_one_character_deletion(lexeme, keyword):
    return len(lexeme) == len(keyword) - 1 and any(
        lexeme[:i] + keyword[i + 1:] == lexeme for i in range(len(keyword)))

# Check if two adjacent characters are transposed
def is_adjacent_character_transposition(lexeme, keyword):
    if len(lexeme) != len(keyword):
        return False
    return any(lexeme[:i] + lexeme[i + 1] + lexeme[i] + lexeme[i + 2:] == keyword
               for i in range(len(lexeme) - 1))

# A rule to handle identifiers and reserved keywords with corrections
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    corrected_token = correct_lexeme(t.value)
    if corrected_token:
        t.type = corrected_token  # Corrected to a keyword
    else:
        if len(t.value) > MAX_IDENTIFIER_LENGTH:
            t.value = t.value[:MAX_IDENTIFIER_LENGTH]  # Truncate long identifiers
        t.type = 'ID'
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

# Test input string with typos
data = '''
iff x + 10 
whille y - 2:
rturn z
x = 12345abcdefg123456789abcdefg123456789abcdefg123456789abcdefg123456789abaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
'''

# Pass the input string to the lexer
lexer.input(data)

# Tokenize and print each token
while True:
    tok = lexer.token()
    if not tok:
        break  # No more input
    print(tok)
