import re

##################################################
# Adiciona símbolo terminal na lista
def adicionaTerminal(t):
    t = re.sub('[\[\]]', '', t)
    terminais.insert( len(terminais), t.strip() )

##################################################
# Adiciona variável de transição na lista
def adicionaVariavel(v):
    v = re.sub('[\[\]]', '', v)
    variaveis.insert( len(variaveis), v.strip() )

##################################################
# Inicializa lista de regras com o identificador de
# palavra vazia
def inicializaRegras():
    for x in variaveis:
        regras.insert( 0, palavraVazia )

##################################################
# Insere regra de transição na lista de regras,
# mantendo a referência com as listas de variáveis
# e de símbolos terminais
#def adicionaRegraDeTransicao(r):
#    regras.insert(,r)

##################################################
# Programa principal

# CORRIGIR: temos que entender como o script receberá
# o nome do arquivo de entrada (provavelmente será um
# parâmetro da chamada do script). 
lines = [line.strip('\n') for line in open('gram1.txt')]

# isso aqui é firula
titles = ["Primeiro grupo: Símbolos terminais",
          "Segundo grupo: Variáveis",
          "Terceiro grupo: Variável inicial",
          "Quarto grupo: Regras de transição"]

# Variáveis e listas usadas no programa
i = 0
terminais = []
variaveis = []
variavelInicial = ''
regras = []
palavraVazia = 'V'


for line in lines:
    if line[0] == '#':
        print(titles[i])
        i = i + 1
    else: # adiciona às listas os termos sem hash
        if i == 1:
            adicionaTerminal(line)
        elif i == 2:
            terminais.sort()
            adicionaVariavel(line)
        elif i == 3:
            variaveis.sort()
            variavelInicial = re.sub('[\[\]]', '', line)
            inicializaRegras()
#        elif i == 4:
#            adicionaRegraDeTransicao(line)
        else:
            print(line)

print(terminais)
print(variaveis)
print(variavelInicial)
print(regras)
