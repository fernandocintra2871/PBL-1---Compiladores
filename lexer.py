import re
import string
from data import reservedWords, delimiters, operators, uniqueOperators

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


# Função que retorna se Caractere está contido na lista de delimitadores:
def isOperator(char):
    return char in operators


# Função para adicionar o token na lista de tokens:
def addTokenList(lexeme, type, n=999):
    if (type == ""):
        if lexeme in reservedWords:
            tokenList.append(f'<Key-words, {lexeme}, {n}>')
        elif lexeme in symbol_table:
            tokenList.append(f'<Identifiers, {lexeme}, {symbol_table.index(lexeme)}, {n}>')
        else:
            symbol_table.append(lexeme)
            tokenList.append(f'<Identifiers, {lexeme}, {symbol_table.index(lexeme)}, {n}>')

    elif (type == "String"):
        if (lexeme[0] == "\"" and lexeme[-1] == "\""):
            tokenList.append(f'<{type}, {lexeme}, {n}>')

    elif (type == "Character"):
        if (lexeme[0] == "\'" and lexeme[-1] == "\'"):
            tokenList.append(f'<{type}, {lexeme}, {n}>')

    else: 
        tokenList.append(f'<{type}, {lexeme}, {n}>')
    


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
                        addTokenList(lexeme, "", n=999)
                        currentState, lexeme = reset(currentState, lexeme)
                else:
                    addTokenList(lexeme, "", n=999)
                    currentState, lexeme = reset(currentState, lexeme)

            elif char.isdigit():
                lexeme = lexeme + char
                if nextIndex < len(line):
                    if line[nextIndex].isdigit() or line[nextIndex] == ".":
                        currentState = "s2"
                    else:
                        addTokenList(lexeme, "Number", n=999)
                        currentState, lexeme = reset(currentState, lexeme)  
                else:
                    addTokenList(lexeme, "Number", n=999)
                    currentState, lexeme = reset(currentState, lexeme)

            elif char == "\"":
                lexeme = lexeme + char
                if nextIndex < len(line):
                    if line[nextIndex] != "\"":
                        currentState = "s5"
                    else:
                        addTokenList(lexeme, "String", n)
                        currentState, lexeme = reset(currentState, lexeme)  
                else:
                    errorList.append(f'<Error, String mal formada>')
                    currentState, lexeme = reset(currentState, lexeme)

            elif char == "\'":
                lexeme = lexeme + char
                if nextIndex < len(line):
                    if line[nextIndex] != "\'":
                        currentState = "s6"
                    else:
                        addTokenList(lexeme, "Character", n)
                        currentState, lexeme = reset(currentState, lexeme)  
                else:
                    errorList.append(f'<Error, Character mal formada>')
                    currentState, lexeme = reset(currentState, lexeme)

            elif isDelimiter(char):
                lexeme = lexeme + char
                addTokenList(lexeme, "Delimiters", n)
                currentState, lexeme = reset(currentState, lexeme)

            elif isOperator(char):
                lexeme += char
                if nextIndex < len(line):
                    if lexeme == "/" or lexeme == "*"  or lexeme == "." :
                        addTokenList(lexeme, "Operators", n)
                        currentState, lexeme = reset(currentState, lexeme)
                    else: 
                        # Comparação para ++ == --
                        if lexeme == "+" and line[nextIndex] != lexeme:
                            addTokenList(lexeme, "Operators", n)
                            currentState, lexeme = reset(currentState, lexeme)
                        else: 
                            currentState = 's8'
                        
                        if lexeme == "-" and line[nextIndex] != lexeme:
                            addTokenList(lexeme, "Operators", n)
                            currentState, lexeme = reset(currentState, lexeme)
                        else: 
                            currentState = 's8'

                        if lexeme == "=" and line[nextIndex] != lexeme:
                            addTokenList(lexeme, "Operators", n)
                            currentState, lexeme = reset(currentState, lexeme)
                        else: 
                            currentState = 's8'
                    
                else:
                    if lexeme in uniqueOperators:
                        addTokenList(lexeme, "Operators", n)
                        currentState, lexeme = reset(currentState, lexeme)
                    else: 
                        errorList.append(f"<Erro, operadores {line}> ")
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
                    addTokenList(lexeme, "", n)
                    # keywordOrIdentifier(lexeme, n)
                    currentState, lexeme = reset(currentState, lexeme)
            else:
                addTokenList(lexeme, "", n)
                # keywordOrIdentifier(lexeme, n)
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
                    addTokenList(lexeme, "Number", n)
                    # checkLexemeType(float(lexeme), n)
                    currentState, lexeme = reset(currentState, lexeme)
            else:
                addTokenList(lexeme, "Number", n)
                # checkLexemeType(float(lexeme), n)
                currentState, lexeme = reset(currentState, lexeme)                   

        # s3 Numbers 2
        elif currentState == "s3":
            if nextIndex < len(line):
                if line[nextIndex].isdigit():
                    lexeme = lexeme + char 
                    currentState = "s4"
                # se ele tá em s3 signfica que tem: xxxx . 
                # ele ta aguardando os próximos digitos, se o próximo não for digito, sai daqui. 
                
                else:
                
                    addTokenList(lexeme, "Number", n)
                    currentState, lexeme = reset(currentState, lexeme)
            else:
                addTokenList(lexeme, "Number", n)
                currentState, lexeme = reset(currentState, lexeme) 

        # s4 Numbers 3
        elif currentState == "s4":
            lexeme = lexeme + char 
            if nextIndex < len(line):
                if line[nextIndex].isdigit():
                    currentState = "s4"
                else:
                    addTokenList(lexeme, "Number", n)
                    currentState, lexeme = reset(currentState, lexeme)
            else:
                addTokenList(lexeme, "Number", n)
                currentState, lexeme = reset(currentState, lexeme) 

        # s5 String
        elif currentState == "s5":
            if char == "\"":
                lexeme = lexeme + char
                addTokenList(lexeme, "String", n)
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
                errorList.append(f'<Error, Character mal formado>')
                currentState, lexeme = reset(currentState, lexeme)

        # s7 Character
        elif currentState == "s7":
            if char == "\'":
                lexeme = lexeme + char
                addTokenList(lexeme, "Character", n)
                currentState, lexeme = reset(currentState, lexeme)
            else:
                errorList.append(f'<Error, Character mal formado>')
                currentState, lexeme = reset(currentState, lexeme)

        
        # s8 Operators
        elif currentState == "s8":
            if(lexeme == "+" and char == "+"):
                lexeme += char
                addTokenList(lexeme, "Operators", n)
                currentState, lexeme = reset(currentState, lexeme)
            else:
                currentState, lexeme = reset(currentState, lexeme)

            if(lexeme == "-" and char == "-"):
                lexeme += char
                addTokenList(lexeme, "Operators", n)
                currentState, lexeme = reset(currentState, lexeme)
            else:
                currentState, lexeme = reset(currentState, lexeme)

            if(lexeme == "=" and char == "="):
                lexeme += char
                addTokenList(lexeme, "Operators", n)
                currentState, lexeme = reset(currentState, lexeme)
            else:
                currentState, lexeme = reset(currentState, lexeme)

            

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


