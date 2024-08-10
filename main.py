import re

# Define patterns for tokenizing the input
patterns = {
    'VARIABLE': r'@[a-zA-Z_][a-zA-Z0-9_]*',
    'NUMBER': r'\d+',
    'PLUS': r'plus',
    'SHOW': r'show',
    'ASSIGN': r'equal',
    'WHITESPACE': r'\s+',
    'UNKNOWN': r'.'
}

def tokenize(code):
    tokens = []
    while code:
        match = None
        for token_type, pattern in patterns.items():
            regex = re.compile(pattern)
            match = regex.match(code)
            if match:
                if token_type != 'WHITESPACE' and token_type != 'UNKNOWN':
                    tokens.append((token_type, match.group(0)))
                code = code[match.end():]
                break
        if not match:
            raise RuntimeError(f'Unexpected character: {code[0]}')
    return tokens

def parse(tokens):
    ast = []
    while tokens:
        token_type, token_value = tokens.pop(0)
        if token_type == 'VARIABLE':
            if tokens and tokens[0][0] == 'ASSIGN':
                tokens.pop(0)  # Remove 'equal'
                if tokens and tokens[0][0] == 'NUMBER':
                    ast.append(('assign', token_value, int(tokens.pop(0)[1])))
                else:
                    raise RuntimeError('Expected number after assignment')
            else:
                raise RuntimeError('Expected assignment after variable')
        elif token_type == 'SHOW':
            if tokens and tokens[0][0] == 'VARIABLE':
                ast.append(('show', tokens.pop(0)[1]))
            else:
                raise RuntimeError('Expected variable after show')
        else:
            raise RuntimeError(f'Unexpected token: {token_type}')
    return ast

def evaluate(ast, context):
    for node in ast:
        if node[0] == 'assign':
            context[node[1]] = node[2]
        elif node[0] == 'show':
            print(context.get(node[1], 'Undefined variable'))

# Sample code for the cursed language
code = """
@x equal 5
@y equal 10
show @x
show @y
"""

# Tokenize, parse, and evaluate
tokens = tokenize(code)
ast = parse(tokens)
context = {}
evaluate(ast, context)
