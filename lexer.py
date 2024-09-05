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

# Line representa cada linha do arquivo, por exemplo.
line = "value = 33.14;"




# Função que retorna se Caractere está contido na lista de delimitadores:
def isDelimiter(char):
    return char in delimiters

# Função que verifca o tipo de lexema
def  checkLexemeType(item):
    if item in reservedWords:
        tokenList.append(f'<Key-words, {item}>')

    elif item in operatorsArithmetic or item in  operatorsRelational or  item in  operatorsLogical:
        tokenList.append(f'<Operators, {item}>')

    elif item in delimiters:
        tokenList.append(f'<Delimiters, {item}>')

    elif type(item) is float or type(item) is int :
        tokenList.append(f'<Number, {item}>')
     


    
# Função para adicionar um identificador na tabela de simbolos ou utilizar uma keyword: 
def keywordOrIdentifier(lexeme):
    if lexeme in reservedWords:
        tokenList.append(f'<Key-words, {lexeme}>')
    elif lexeme in symbol_table:
        tokenList.append(f'<Identifiers, {lexeme}, {symbol_table.index(lexeme)}>')
    
    else:
        symbol_table.append(lexeme)
        tokenList.append(f'<Identifiers, {lexeme}, {symbol_table.index(lexeme)}>')

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


def startAnalyze():
    initState = "s0"
    currentState = initState
    lexeme = ""
    counter = 0
    currentIndex = 0


    while currentIndex <= len(line) -1:
    # usado pra algumas verificações que serão preciso
        char = line[currentIndex]

        nextIndex = currentIndex + 1 if currentIndex + 1 < len(line) else currentIndex

        # s0 ESTADO INICIAL - A PRIMEIRA ENTRADA PASSA POR AQUI
        if currentState == "s0":
            if char.isalpha():
                currentState = "s1"
                lexeme = lexeme + char

            elif char.isdigit():
                currentState = "s2"
                lexeme = lexeme + char

            elif char == "\"":
                currentState = "s4"
                lexeme = lexeme + char
            elif char == "\'":
                currentState = "s6"
                lexeme = lexeme + char
            elif isDelimiter(char):
                currentState = "s8"
                lexeme = lexeme + char

            else:
                currentState = "s0"



        elif currentState == "s1":
            if char.isalpha() or char.isdigit() or char == '_':
                currentState = "s1"
                lexeme = lexeme + char 
                if not line[nextIndex].isalpha() and not line[nextIndex].isdigit() and not line[nextIndex] == '_':
                    keywordOrIdentifier(lexeme)
                    currentState, lexeme = reset(currentState, lexeme)
            else:
                keywordOrIdentifier(lexeme)
                currentState, lexeme = reset(currentState, lexeme)


        
        
        elif currentState == "s2":
            if char.isdigit():
                currentState = "s2"
                lexeme = lexeme + char                
                if not  line[nextIndex] == '.' and not line[nextIndex].isdigit():
                    checkLexemeType(lexeme)
                    currentState, lexeme = reset(currentState, lexeme)
                
                elif line[nextIndex] == '.': 
                    currentState = 's2'
                elif line[nextIndex].isdigit(): 
                    currentState = 's2'
            elif '.' == char: 
                lexeme = lexeme + char 
                currentState = 's3'
            else: 
                checkLexemeType(lexeme)
                lexeme = ''                   


        elif currentState == "s3":
            if char.isdigit():
                currentState = "s3"
                lexeme = lexeme + char                        
            if not line[nextIndex].isdigit():
                checkLexemeType(float(lexeme))
                currentState, lexeme = reset(currentState, lexeme)
            else: 
                currentState = 's3'

        elif currentState == "s4":
            if char == "\"":
                lexeme = lexeme + char
                stringTokenType(lexeme)
                lexeme = ''
            else: 
                lexeme = lexeme + char
                if line[nextIndex] != "\"":
                    currentState == "s4"
                    
                else: 
                    currentState == "s5"
        
        elif currentState == "s5":
            if char == "\"":
                lexeme = lexeme + char
                stringTokenType(lexeme)
                currentState, lexeme = reset(currentState, lexeme)


            else: 
                if currentIndex + 1 > len(line):
                    if line[nextIndex] != "\"":
                        lexeme = ''
                        print("Lexema resetado")


        elif currentState == "s6":
            if char == "\'":
                lexeme = lexeme + char
                characterTokenType(lexeme)
                currentState, lexeme = reset(currentState, lexeme)
            else: 
                lexeme = lexeme + char
                if line[nextIndex] != "\"":
                    currentState == "s6"
                    
                else: 
                    currentState == "s7"

        elif currentState == "s7":
            if char == "\'":
                lexeme = lexeme + char
                stringTokenType(lexeme)
                currentState, lexeme = reset(currentState, lexeme)
            else:
                if currentIndex + 1 > len(line):
                    if line[nextIndex] != "\'":
                        currentState, lexeme = reset(currentState, lexeme)
                        print("Lexema resetado")
        
        elif currentState == "s8":
            
            checkLexemeType(lexeme)
            currentState, lexeme = reset(currentState, lexeme)
            
            if currentIndex + 1 > len(line):
                currentState, lexeme = reset(currentState, lexeme)
                print("Lexema resetado")
        
        if currentIndex == len(line) -1 and lexeme != "":
            currentIndex = currentIndex
        else:
            currentIndex += 1

                
            
    

startAnalyze()
for item in tokenList:
    print(item)



