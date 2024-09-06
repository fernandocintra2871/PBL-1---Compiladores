import re
import string
from data import reservedWords, operatorsArithmetic, operatorsRelational, operatorsLogical, delimiters

estados = ["s0", "s1"]
func_transictions = {}
estadosFinais = ["s1, s2","s3", "s4", "s5"]
# Lista que contém todos os tokens
tokenList = []

# Lista de contendo os erros
errorList = []

# Tabela de Simbolos
symbol_table = []

# Função que retorna se Caractere está contido na lista de delimitadores:
def isDelimiter(char):
    return char in delimiters

# Função que verifca o tipo de lexema
def  checkLexemeType(item, n=999):
    if item in reservedWords:
        tokenList.append(f'<Key-words, {item}, {n}>')

    elif item in operatorsArithmetic or item in  operatorsRelational or  item in  operatorsLogical:
        tokenList.append(f'<Operators, {item}, {n}>')

    elif item in delimiters:
        tokenList.append(f'<Delimiters, {item}, {n}>')

    elif type(item) is float or type(item) is int :
        tokenList.append(f'<Number, {item}, {n}>')
     


    
# Função para adicionar um identificador na tabela de simbolos ou utilizar uma keyword: 
def keywordOrIdentifier(lexeme, n=999):
    if lexeme in reservedWords:
        tokenList.append(f'<Key-words, {lexeme}, {n}>')
    elif lexeme in symbol_table:
        tokenList.append(f'<Identifiers, {lexeme}, {symbol_table.index(lexeme)}, {n}>')
    
    else:
        symbol_table.append(lexeme)
        tokenList.append(f'<Identifiers, {lexeme}, {symbol_table.index(lexeme)}, {n}>')

# Função para retornar um token do tipo string
def stringTokenType(lexeme):
    if lexeme[0] == "\"" and lexeme[-1] == "\"" :
        tokenList.append(f'<String, {lexeme}>')
    

# Função para retornar um token do tipo Caractere
def characterTokenType(lexeme):
    if lexeme[0] == "\'" and lexeme[-1] == "\'" :
        tokenList.append(f'<Character, {lexeme}>')


# Função para reset, quando acabar a linha (add index para verificar se está no fim de linha e deixar implicito a está func)
def reset(state, lexem):
    state = "s0"
    lexem = ''
    return state, lexem


def startAnalyze(line, n):
    initState = "s0"
    currentState = initState
    lexeme = ""
    counter = 0
    currentIndex = 0


    while currentIndex <= len(line) -1:
    # usado pra algumas verificações que serão preciso
        char = line[currentIndex]
        nextIndex = currentIndex + 1

        # s0 ESTADO INICIAL - A PRIMEIRA ENTRADA PASSA POR AQUI
        if currentState == "s0":
            if char.isalpha():
                lexeme = lexeme + char
                if nextIndex < len(line):
                    if line[nextIndex].isalpha() or line[nextIndex].isdigit() or line[nextIndex] == '_':
                        currentState = "s1"
                    else:
                        keywordOrIdentifier(lexeme, n)
                        currentState, lexeme = reset(currentState, lexeme)
                else:
                    keywordOrIdentifier(lexeme, n)
                    currentState, lexeme = reset(currentState, lexeme)

            elif char.isdigit():
                lexeme = lexeme + char
                if nextIndex < len(line):
                    if line[nextIndex].isdigit() or line[nextIndex] == ".":
                        currentState = "s2"
                    else:
                        checkLexemeType(float(lexeme), n)
                        currentState, lexeme = reset(currentState, lexeme)  
                else:
                    checkLexemeType(float(lexeme), n)
                    currentState, lexeme = reset(currentState, lexeme)

            elif char == "\"":
                currentState = "s4"
                lexeme = lexeme + char
            elif char == "\'":
                currentState = "s6"
                lexeme = lexeme + char
            elif isDelimiter(char):
                currentState = "s8"
                lexeme = lexeme + char
                checkLexemeType(lexeme)
                currentState, lexeme = reset(currentState, lexeme)
            else:
                currentState = "s0"


        # s1 Identifiers
        elif currentState == "s1":
            lexeme = lexeme + char 
            if nextIndex < len(line):
                if line[nextIndex].isalpha() or line[nextIndex].isdigit() or line[nextIndex] == '_':
                    currentState = "s1"
                else: 
                    keywordOrIdentifier(lexeme, n)
                    currentState, lexeme = reset(currentState, lexeme)
            else:
                keywordOrIdentifier(lexeme, n)
                currentState, lexeme = reset(currentState, lexeme)
        
        # s2 Numbers 1
        elif currentState == "s2":
            lexeme = lexeme + char   
            if nextIndex < len(line):
                if line[nextIndex].isdigit():
                    currentState = "s2"
                elif line[nextIndex] == ".":
                    currentState = "s3"
                else:
                    checkLexemeType(float(lexeme), n)
                    currentState, lexeme = reset(currentState, lexeme)
            else:
                checkLexemeType(float(lexeme), n)
                currentState, lexeme = reset(currentState, lexeme)                   

        # s3 Numbers 2
        elif currentState == "s3":
            if nextIndex < len(line):
                if line[nextIndex].isdigit():
                    lexeme = lexeme + char 
                    currentState = "s4"
                else:
                    checkLexemeType(float(lexeme), n)
                    currentState, lexeme = reset(currentState, lexeme)
                    lexeme = lexeme + char 
                    checkLexemeType(lexeme, n)
                    currentState, lexeme = reset(currentState, lexeme)
            else:
                checkLexemeType(float(lexeme), n)
                currentState, lexeme = reset(currentState, lexeme) 

        # s4 Numbers 3
        elif currentState == "s4":
            lexeme = lexeme + char 
            if nextIndex < len(line):
                if line[nextIndex].isdigit():
                    currentState = "s4"
                else:
                    checkLexemeType(float(lexeme), n)
                    currentState, lexeme = reset(currentState, lexeme)
            else:
                checkLexemeType(float(lexeme), n)
                currentState, lexeme = reset(currentState, lexeme) 

        # s4 String
        elif currentState == "s4":
            if char == "\"":
                lexeme = lexeme + char
                stringTokenType(lexeme)
                currentState, lexeme = reset(currentState, lexeme)
            elif char.isalpha() or char.isdigit() or (32 <= ord(char) <= 126 and ord(char) != 34 and ord(char) !=39):
                lexeme = lexeme + char
                if currentIndex >= len(line) - 1: # Tratamento string não fechada
                    currentState, lexeme = reset(currentState, lexeme)
                    errorList.append(f'<Error, String não fechada>')
            else:
                currentState, lexeme = reset(currentState, lexeme)
                errorList.append(f'<Error, String mal formada>')

        # s6 Character
        elif currentState == "s6":
            if char.isalpha() or char.isdigit() or (32 <= ord(char) <= 126 and ord(char) != 34 and ord(char) !=39):
                lexeme = lexeme + char
                currentState = "s7"
            else:
                currentState, lexeme = reset(currentState, lexeme)
                errorList.append(f'<Error, Character mal formado>')

        # s7 Character
        elif currentState == "s7":
            if char == "\'":
                lexeme = lexeme + char
                characterTokenType(lexeme)
                currentState, lexeme = reset(currentState, lexeme)
            else:
                errorList.append(f'<Error, Character mal formado>')
        

        if currentIndex == len(line) -1 and lexeme != "":
            currentIndex = currentIndex
        else:
            currentIndex += 1

         
            

try:
    with open('code.txt', 'r') as file:
        n = 1
        for line in file:
            startAnalyze(line, n)
            n += 1
except FileNotFoundError:
    print("O arquivo 'code.txt' não foi encontrado.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")


for item in tokenList:
    print(item)

print("\nErros:")

for item in errorList:
    print(item)


