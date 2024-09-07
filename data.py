reservedWords = {
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
}


# Operadores aritmeticos 
operatorsArithmetic = ['+', '-', '++', '--','*', '/']

# Operadores Relacionais 
operatorsRelational = ['==', '!=', '>', '>=', '<', '<=']

# Operadores Lógicos 
operatorsLogical = ['&&', '||']

# Operador de Acesso
operatorsAssignment = ['=']

operatorsAcess = ["."]

uniqueOperators = ['+','-','*', '/', '=','.']

doubleOperators = ['++', '--','==', '!=', '>=', '<=', '&&', '||']

#operators = ['+', '-', '++', '--','*', '/', '==', '!=', '>', '>=', '<', '<=', '&&', '||', '=', "."]
operators = ['+', '-','*', '/', '!', '>', '<', '&', '|', '=', "."]
# Operador de Atribuição

# Delimitadores
delimiters = [';',',','(',')','{','}']




# Dicionário que contém todas as expressões regulares 
'''
    As outras expressões como :
    numbers: ( - )? Digit+( . Digit+)?
    string: "(Letter | Digit | Symbol)*"
    character: '(Letter | Digit | Symbol)' 
    Symbols: ASCII from 32 to 126 (except 34 and 39)

    São composições que utilizam as outras expressões regulares, por exemplo.
'''




    # "identifiers": r'[A-Za-z](?:[A-Za-z0-9_]*)'
regularExpressions = {
    "numbers" : r"(-)?[0-9]+(\.[0-9]+)?",
    "identifiers": r"[a-zA-Z]([a-zA-Z0-9_])*",
    "letter" : r"[a-zA-Z]",
    "digit" : r"[0-9]",
    "operatorsArithmetic": ['+', '-', '++', '--','*', '/'],
    "operatorsRelational" : ['==', '=', '!=', '>', '>=', '<', '<=', ],
    "operatorsLogical" : ['&&', '||'],
    "acessOperator" : ['.'],
    "delimiters" : [';',',','(',')','{','}'],

}

## Algumas regras:
    # - Se vem // seguidas é um comment
    # - Se vem / e depois * é um comentário em bloco
    # - Se recebe " é inicio de string, a string só encerra quando achar " na mesma linha, ou então será um erro