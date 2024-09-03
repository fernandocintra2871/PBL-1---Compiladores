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
from data import reservedWords

_letter = r'[a-zA-Z]'
_oneAndMoreLetter = r'(?:[A-Za-z0-9_]*)'
_digit = r'[0-9]'
_identifiers = r'[A-Za-z](?:[A-Za-z0-9_]*)'


'''
tô em s0, recebo uma letter => s1
tô em s1, recebo uma letter = s1
tô em s1, recebo diferente => s0 
'''


estados = ["s0", "s1"]
# alfabeto = "_value_"
func_transictions = {}
estadoInicial = "s0"
estadoAtual = estadoInicial
estadosFinais = ["s1"]


#line representa cada linha do arquivo, por exemplo.
line = "extends="
counter = 0
estadoAtual = estadoInicial
lexeme = ""
currentIndex = 0

# Função que verifica se está contido na lista de palavras chaves 
def  checkInReservedWords(value):
    print(value in reservedWords)
    if value in reservedWords:
        print (f'<keyword, {value}>')
     



while currentIndex < len(line):
    # usado pra algumas verificações que serão preciso
    next_index = currentIndex + 1 if currentIndex + 1 < len(line) else currentIndex

    for char in line:
        currentIndex += 1
        if estadoAtual == "s0":
            if re.fullmatch(_letter,char):
                estadoAtual = "s1"
                lexeme = lexeme + char
            else:
                estadoAtual = "s0"
                break
    
        elif estadoAtual == "s1":
            
            if re.fullmatch(_oneAndMoreLetter,char):
                estadoAtual = "s1"
                lexeme = lexeme + char               
            else:
                checkInReservedWords(lexeme)
                index = len(line)
                break
    


# while conter<len(alfabeto):



#     '''
#     tô em s0, recebo uma letter => s1
#     tô em s1, recebo uma letter = s1
#     tô em s1, recebo diferente => s0 
#     '''

#  if re.fullmatch(_identifiers, al):
