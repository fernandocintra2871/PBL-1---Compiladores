
key_words = [
    "variables",
    "methods",
    "constants",
    "class",
    "return",
    "empty",
    "main",
    "if",
    "then",
    "else",
    "while",
    "for",
    "read",
    "write",
    "integer",
    "float",
    "boolean",
    "string",
    "true",
    "false",
    "extends"
]

symbol_table = []


START = 0
IDENTIFIERS = 1

try:
    with open('code.txt', 'r') as file:
        content = file.read()
except FileNotFoundError:
    print("O arquivo 'code.txt' não foi encontrado.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")

content = content.replace('\n', ' ')

begin = 0
lookahead = 0
state = 0
while lookahead < len(content):
   
    c = content[lookahead]
    if state == START:
        if c.isalpha():
            state = IDENTIFIERS
        elif c == " ":
            begin += 1
        lookahead += 1
    
    elif state == IDENTIFIERS:
        if not(c.isalpha() or c.isdigit() or c == "_"):
            lexeme = content[begin:lookahead]
            if lexeme in key_words:
                print(f"<key-words, {lexeme}>")
            elif lexeme in symbol_table:
                print(f"<identifiers, {lexeme}, {symbol_table.index(lexeme)}>")
            else:
                symbol_table.append(lexeme)
                print(f"<identifiers, {lexeme}, {symbol_table.index(lexeme)}>")
            begin = lookahead
            state = START
        else:
            lookahead += 1
