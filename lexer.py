# M = (Q, Σ, δ, q0, F)

# q = conjunto de estados do autômato (q0 (estado inicial), q1(estado de espera))

# Σ = alfabeto  de entradas

#δ = Funções de transição{
#    δ: (q0, letter) => q1
#    δ: (q1, letter) => q1
#    δ: (q0, other) => q0
#}

#q0 = estado inicial
#F = conjunto de estados de aceitação {q1}

import re
from data import reservedWords, regularExpressions

'''
tô em s0, recebo uma letter => s1
tô em s1, recebo uma letter = s1
tô em s1, recebo diferente => s0 
'''


estados = ["s0", "s1"]
# alfabeto = "_value_"
func_transictions = {}
# initState = "s0"
# currentState = initState
estadosFinais = ["s1, s2"]


#line representa cada linha do arquivo, por exemplo.



tokenList = []
errorList = []




# Função que verifca o tipo de lexema
def  checkLexemeType(item):
    print(item)
    if item in reservedWords:
        tokenList.append(f'<keyword, {item}>')

    if item in regularExpressions['operatorsRelational'] or item in regularExpressions['operatorsLogical'] or item in regularExpressions['operatorsArithmetic']:
        tokenList.append(f'<operators, {item}>')

    if re.fullmatch(regularExpressions['numbers'], item):
        tokenList.append(f'<number, {item}>')
     
    

line = "extends=33.14;"

def startAnalyze():
    initState = "s0"
    counter = 0
    currentState = initState
    lexeme = ""
    currentIndex = 0

    while currentIndex <= len(line) -1:
    # usado pra algumas verificações que serão preciso

        for char in line:

            nextIndex = currentIndex + 1 if currentIndex + 1 <= len(line) -1 else currentIndex
            if currentState == "s0":
                if re.fullmatch(regularExpressions['letter'],char):
                    currentState = "s1"
                    lexeme = lexeme + char

                elif re.fullmatch(regularExpressions['digit'], char):
                    currentState = "s2"
                    lexeme = lexeme + char
   
                else:
                    currentState = "s0"

            elif currentState == "s1":
                if re.fullmatch(regularExpressions['letter'],char) or re.fullmatch(regularExpressions['digit'],char) or char == '_':
                    currentState = "s1"
                    lexeme = lexeme + char 

                    if not re.fullmatch(regularExpressions['letter'],line[nextIndex]) and not re.fullmatch(regularExpressions['digit'],line[nextIndex]) and not line[nextIndex] == '_':
                        currentState = "s0"   
                        checkLexemeType(lexeme)
                        lexeme = ''
                else:
                    checkLexemeType(lexeme)
                    lexeme = ''

            
            elif currentState == "s2":

                if re.fullmatch(regularExpressions['digit'], char):
                    currentState = "s2"
                    lexeme = lexeme + char 
                    
                    print     ('.' == line[nextIndex] )                 
                    if not '.' == line[nextIndex] and not re.fullmatch(regularExpressions['digit'], line[nextIndex]):

                        currentState = "s0"
                        checkLexemeType(lexeme)
                        lexeme = ''                   
                    elif '.' == line[nextIndex]: 
                        currentState = 's3'
                    elif re.fullmatch(regularExpressions['digit'], line[nextIndex]): 
                        currentState = 's2'
                elif '.' == char: 
                    lexeme = lexeme + char 
                    currentState = 's3'
                

            elif currentState == "s3":
                 if re.fullmatch(regularExpressions['digit'], char) or '.' == char:
                    currentState = "s3"
                    lexeme = lexeme + char                           
                    if not re.fullmatch(regularExpressions['digit'], line[nextIndex]):
                        currentState = "s0"
                        checkLexemeType(lexeme)
                        lexeme = ''                   
                   
                    else: 
                        currentState = 's3'
            currentIndex += 1
            
    

startAnalyze()
for item in tokenList:
    print(item)



