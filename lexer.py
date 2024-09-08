from data import reservedWords, delimiters, operators, uniqueOperators, doubleOperators

# Lista que contém todos os tokens
tokenList = []

# Lista que contém todos os erros
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
def addTokenList(lexeme, type, n):
    if type == "Identifiers":
        if lexeme in reservedWords:
            tokenList.append(f'<Key-words, {lexeme}, {n}>')
        elif lexeme in symbol_table:
            tokenList.append(f'<Identifiers, {lexeme}, {symbol_table.index(lexeme)}, {n}>')
        else:
            symbol_table.append(lexeme)
            tokenList.append(f'<Identifiers, {lexeme}, {symbol_table.index(lexeme)}, {n}>')
    else: 
        tokenList.append(f'<{type}, {lexeme}, {n}>')
    
def addErrorList(lexeme, type, n):
    if type == "SMF":
        errorList.append(f'<String mal formada, {lexeme}, {n}>')
    elif type == "CMF":
        errorList.append(f'<Character mal formado, {lexeme}, {n}>')
    elif type == "OMF":
        errorList.append(f'<Operador mal formado, {lexeme}, {n}>')
    elif type == "BCMF":
        errorList.append(f'<Comentário de bloco mal formado, {lexeme}, {n}>')
    else: 
        tokenList.append(f'<Erro>, {lexeme}, {n}>')

# Função para resetar o estado e o buffer do lexema quando um token é encontrado
def reset(state, lexem):
    state = "s0"
    lexem = ''
    return state, lexem

# Função que analisa o arquivo de texto para identificar os tokens e os erros quando ocorridos
def startAnalyze(file):
    n = 1 # Linha do arquivo lida
    currentState = "s0" # Estado atual da maquina de estados
    lexeme = "" # Buffer que armazena os caracteres do lexema que está sendo formado
    
    for line in file: 
        currentIndex = 0
        while currentIndex <= len(line) -1:
            char = line[currentIndex]
            nextIndex = currentIndex + 1 
            # Estado inicial
            if currentState == "s0":
                # Inicia a verificação se o lexema é um Identifiers ou Key-words
                if char.isalpha(): # Verificar se o caracter é uma Letter
                    lexeme = lexeme + char
                    if nextIndex < len(line):
                        if line[nextIndex].isalpha() or line[nextIndex].isdigit() or line[nextIndex] == '_':
                            currentState = "s1"
                        else:
                            addTokenList(lexeme, "Identifiers", n)
                            currentState, lexeme = reset(currentState, lexeme)
                    else:
                        addTokenList(lexeme, "Identifiers", n)
                        currentState, lexeme = reset(currentState, lexeme)
                
                # Inicia a verificação se o lexema é um Numbers
                elif char.isdigit(): # Verificar se o caracter é um Digit
                    lexeme = lexeme + char
                    if nextIndex < len(line):
                        if line[nextIndex].isdigit() or line[nextIndex] == ".":
                            currentState = "s2"
                        else:
                            addTokenList(lexeme, "Number", n)
                            currentState, lexeme = reset(currentState, lexeme)  
                    else:
                        addTokenList(lexeme, "Number", n)
                        currentState, lexeme = reset(currentState, lexeme)

                # Inicia a verificação se o lexema é uma String
                elif char == "\"":
                    lexeme = lexeme + char
                    if nextIndex < len(line):
                        if line[nextIndex].isalpha() or line[nextIndex].isdigit() or (32 <= ord(line[nextIndex]) <= 126 and ord(line[nextIndex]) != 39):
                            currentState = "s5"
                        else:
                            addErrorList(lexeme, "SMF", n)
                            currentState, lexeme = reset(currentState, lexeme)  
                    else:
                        addErrorList(lexeme, "SMF", n)
                        currentState, lexeme = reset(currentState, lexeme)

                # Inicia a verificação se o lexema é um Character
                elif char == "\'":
                    lexeme = lexeme + char
                    if nextIndex < len(line):
                        if line[nextIndex].isalpha() or line[nextIndex].isdigit() or (32 <= ord(line[nextIndex]) <= 126 and ord(line[nextIndex]) != 34 and ord(line[nextIndex]) != 39):
                            currentState = "s6"
                        else:
                            addErrorList(lexeme, "CMF", n)
                            currentState, lexeme = reset(currentState, lexeme)
                    else:
                        addErrorList(lexeme, "CMF", n)
                        currentState, lexeme = reset(currentState, lexeme)

                # Inicia a verificação se o lexema é um Delimiter
                elif isDelimiter(char):
                    lexeme = lexeme + char
                    addTokenList(lexeme, "Delimiters", n)
                    currentState, lexeme = reset(currentState, lexeme)

                # Inicia a verificação se o lexema é um Operators
                elif isOperator(char):
                    lexeme += char
                    if nextIndex < len(line):
                        if lexeme == "/":      
                            if line[nextIndex] == "/":
                                currentState = 's9'
                            elif line[nextIndex] == "*":
                                currentState = 's11'
                            else:
                                addTokenList(lexeme, "Operators", n)
                                currentState, lexeme = reset(currentState, lexeme)
                        elif char == "*":
                            addTokenList(lexeme, "Operators", n)
                            currentState, lexeme = reset(currentState, lexeme)
                        else: 
                            if lexeme == ".":
                                addTokenList(lexeme, "Operators", n)
                                currentState, lexeme = reset(currentState, lexeme)
                            else: 
                                if lexeme == "+" and line[nextIndex] != lexeme:
                                    addTokenList(lexeme, "Operators", n)
                                    currentState, lexeme = reset(currentState, lexeme)
                                elif lexeme == "-" and line[nextIndex] != lexeme:
                                    addTokenList(lexeme, "Operators", n)
                                    currentState, lexeme = reset(currentState, lexeme)
                                elif lexeme == "=" and line[nextIndex] != lexeme:
                                    addTokenList(lexeme, "Operators", n)
                                    currentState, lexeme = reset(currentState, lexeme)
                                elif lexeme == ">" and line[nextIndex] != "=":
                                    addTokenList(lexeme, "Operators", n)
                                    currentState, lexeme = reset(currentState, lexeme)
                                elif lexeme == "<" and line[nextIndex] != "=":
                                    addTokenList(lexeme, "Operators", n)
                                    currentState, lexeme = reset(currentState, lexeme)
                                else: 
                                    currentState = 's8'
                    else:
                        if lexeme in uniqueOperators:
                            addTokenList(lexeme, "Operators", n)
                            currentState, lexeme = reset(currentState, lexeme)
                        else: 
                            addErrorList(lexeme, "OMF", n)
                            currentState, lexeme = reset(currentState, lexeme)
                else:
                    currentState = "s0"
                    
            # Estado s1 (Identifiers)
            elif currentState == "s1":
                lexeme = lexeme + char 
                if nextIndex < len(line):
                    if line[nextIndex].isalpha() or line[nextIndex].isdigit() or line[nextIndex] == '_':
                        currentState = "s1"
                    else: 
                        addTokenList(lexeme, "Identifiers", n)
                        currentState, lexeme = reset(currentState, lexeme)
                else:
                    addTokenList(lexeme, "Identifiers", n)
                    currentState, lexeme = reset(currentState, lexeme)
            
            # Estado s2 (Numbers)
            # Consome os primeiros numeros
            elif currentState == "s2":
                lexeme = lexeme + char   
                if nextIndex < len(line):
                    if line[nextIndex].isdigit():
                        currentState = "s2"
                    elif line[nextIndex] == ".":
                        currentState = "s3"
                    else:
                        addTokenList(lexeme, "Number", n)
                        currentState, lexeme = reset(currentState, lexeme)
                else:
                    addTokenList(lexeme, "Number", n)
                    currentState, lexeme = reset(currentState, lexeme)                   

            # Estado s3 (Numbers)
            # Consome o .
            elif currentState == "s3":
                if nextIndex < len(line):
                    if line[nextIndex].isdigit():
                        lexeme = lexeme + char 
                        currentState = "s4"         
                    else:
                        addTokenList(lexeme, "Number", n)
                        currentState, lexeme = reset(currentState, lexeme)
                else:
                    addTokenList(lexeme, "Number", n)
                    currentState, lexeme = reset(currentState, lexeme) 

            # s4 (Numbers)
            # Consome os demais numeros depois do .
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

            # s5 (String)
            elif currentState == "s5":
                lexeme = lexeme + char
                if char == "\"":
                    addTokenList(lexeme, "String", n)
                    currentState, lexeme = reset(currentState, lexeme)
                elif nextIndex < len(line):
                    if line[nextIndex].isalpha() or line[nextIndex].isdigit() or (32 <= ord(line[nextIndex]) <= 126 and ord(line[nextIndex]) != 39):
                        currentState = "s5"
                    else:
                        addErrorList(lexeme, "SMF", n)
                        currentState, lexeme = reset(currentState, lexeme)
                else:
                    addErrorList(lexeme, "SMF", n)
                    currentState, lexeme = reset(currentState, lexeme)

            # s6 (Character)
            elif currentState == "s6":
                lexeme = lexeme + char
                if char == "\'":
                    addTokenList(lexeme, "Character", n)
                    currentState, lexeme = reset(currentState, lexeme)
                elif nextIndex < len(line):
                    if line[nextIndex] != "\'":
                        addErrorList(lexeme, "CMF", n)
                        currentState, lexeme = reset(currentState, lexeme)
                    else:
                        currentState = "s6"
                else:
                    addErrorList(lexeme, "CMF", n)
                    currentState, lexeme = reset(currentState, lexeme)

            # s8 (Operators)
            # Indentifica os operadores com o lexema de tamanho 2
            elif currentState == "s8":
                lexeme = lexeme + char
                if lexeme in doubleOperators:
                    addTokenList(lexeme, "Operators", n)
                    currentState, lexeme = reset(currentState, lexeme)
                else:
                    addErrorList(lexeme, "OMF", n)
                    currentState, lexeme = reset(currentState, lexeme)

                
            # s9 (Individual Comments)
            elif currentState == 's9':
                lexeme += char
                if nextIndex < len(line):
                    currentState == 's9'
                else: 
                    addTokenList(lexeme, "Comments", n)
                    currentState, lexeme = reset(currentState, lexeme)
    
            # S11 (Block comment)
            # Consome os caracteres até encontrar um * seguido de uma /
            elif currentState == 's11':
                lexeme += char
                if nextIndex < len(line):
                    if char == '*' and line[nextIndex] == '/':
                        currentState = 's13'
                    else:
                       currentState = 's11' 
                else:
                    currentState = 's11'
            
            # S13 (Block comment)
            # Consome a / e identifica o o token
            elif currentState == 's13':
                lexeme += char
                addTokenList(lexeme, "Comments", n)
                currentState, lexeme = reset(currentState, lexeme)

            currentIndex += 1 # Avança pra o proximo caracter da linha
        n += 1 # Avança pra proxima linha
    
    # Se chegou ao final do arquivo e se manteve no estado s11
    # É sinal que um comentario de bloco não foi fechado
    if currentState == 's11': 
        addErrorList(lexeme, "BCMF", n)

"""
==============================
        Código Principal
==============================
"""
try:
    with open('code.txt', 'r') as file:
        startAnalyze(file)
except FileNotFoundError:
    print("O arquivo 'code.txt' não foi encontrado.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")

print("\nTokens:")
for item in tokenList:
    print(item)

if len(errorList) == 0:
    print("SUCESSO!")
else:
    print("\nErros:")
    for item in errorList:
        print(item)


