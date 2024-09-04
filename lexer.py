import re
import string
from data import reservedWords, operatorsArithmetic, operatorsRelational, operatorsLogical

estados = ["s0", "s1"]
func_transictions = {}
estadosFinais = ["s1, s2"]
# Lista que contém todos os tokens
tokenList = []

# Lista de contendo os erros
errorList = []

# Tabela de Simbolos
symbol_table = []

# Line representa cada linha do arquivo, por exemplo.
line = "value=33.14;"



# Função que verifca o tipo de lexema
def  checkLexemeType(item):
    if item in reservedWords:
        tokenList.append(f'<keyword, {item}>')

    elif item in operatorsArithmetic or operatorsRelational or operatorsLogical:
        tokenList.append(f'<operators, {item}>')

    elif type(item) is float or type(item) is int :
        tokenList.append(f'<number, {item}>')
     


    
# Função para adicionar um identificador na tabela de simbolos ou utilizar uma keyword: 
def keywordOrIdentifier(lexeme):
    if lexeme in reservedWords:
        tokenList.append(f'<keyword, {lexeme}>')
    elif lexeme in symbol_table:
        tokenList.append(f'<identifiers, {lexeme}, {symbol_table.index(lexeme)}>')
    else:
        symbol_table.append(lexeme)
        tokenList.append(f'<identifiers, {lexeme}, {symbol_table.index(lexeme)}>')



def startAnalyze():
    initState = "s0"
    currentState = initState
    lexeme = ""
    counter = 0
    currentIndex = 0

    while currentIndex <= len(line) -1:
    # usado pra algumas verificações que serão preciso

        for char in line:
            nextIndex = currentIndex + 1 if currentIndex + 1 <= len(line) -1 else currentIndex

            # s0 ESTADO INICIAL - A PRIMEIRA ENTRADA PASSA POR AQUI

            if currentState == "s0":
                if char.isalpha():
                    currentState = "s1"
                    lexeme = lexeme + char
                elif char.isdigit():
                    currentState = "s2"
                    lexeme = lexeme + char
                else:
                    currentState = "s0"

            elif currentState == "s1":
                if char.isalpha() or char.isdigit() or char == '_':
                    currentState = "s1"
                    lexeme = lexeme + char 
                    if not line[nextIndex].isalpha() and not line[nextIndex].isdigit() and not line[nextIndex] == '_':
                        currentState = "s0"   
                        keywordOrIdentifier(lexeme)
                        lexeme = ''
                else:
                    keywordOrIdentifier(lexeme)
                    lexeme = ''

            
            elif currentState == "s2":

                if char.isdigit():
                    currentState = "s2"
                    lexeme = lexeme + char                
                    if not  line[nextIndex] == '.' and not line[nextIndex].isdigit():
                        currentState = "s0"
                        checkLexemeType(lexeme)
                        lexeme = ''                   
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
                        currentState = "s0"
                        checkLexemeType(float(lexeme))
                        lexeme = ''                   
                    else: 
                        currentState = 's3'
            currentIndex += 1
            
    

startAnalyze()
for item in tokenList:
    print(item)



