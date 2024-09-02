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



counter = 0
while(1):
    print("Insira as informações: ", end="")
    alfabeto = input()
    estadoAtual = estadoInicial

    for char in alfabeto:
        print(f'Estado atual {estadoAtual}')
        print(f'Entrada Atual {char}') 


        if estadoAtual == "s0":
            if re.fullmatch(_letter,char):
                estadoAtual = "s1"
                print ("Casou")
            else:
                estadoAtual = "s0"
                print ("Não casou")
                break
        
        elif estadoAtual == "s1":
            if re.fullmatch(_oneAndMoreLetter,char):
                estadoAtual = "s1"
                print ("Casou")
            else:
                print ("Não casou")
                break

# while conter<len(alfabeto):



#     '''
#     tô em s0, recebo uma letter => s1
#     tô em s1, recebo uma letter = s1
#     tô em s1, recebo diferente => s0 
#     '''

#  if re.fullmatch(_identifiers, al):
