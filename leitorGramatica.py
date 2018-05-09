import re

regex = re.compile(r"\[(.*?)\]")


'''
l1 = "[ S ] > [ X ] [ Y ] [ Z ]		# O simbolo de \">\" representa a derivacao [r]."
l2 = "[ a ]	[b]"
#l3 = "[ b ]"

#print(re.findall(regex, l3))
#print(re.findall(regex, l2))
#l = re.finditer(regex, l1)

print(re.findall(regex, l1.split('#')[0]))
print(re.findall(regex, l2))

'''
##################################################
# Adiciona símbolo terminal na lista
def adicionaTerminal(linhaTerm):
    simbolos = re.findall(regex, linhaTerm.split('#')[0])
    for terminal in simbolos:
        terminais.insert( len(terminais), terminal.strip() )

##################################################
# Adiciona variável de transição na lista
def adicionaVariavel(linhaVar):
    simbolos = re.findall(regex, linhaVar.split('#')[0])
    for variavel in simbolos:
        variaveis.insert( len(variaveis), variavel.strip() )

##################################################
# Inicializa lista de regras com o identificador de
# palavra vazia
def inicializaRegras():
  for i in range(len(variaveis)):
    regras.insert(i, [variaveis[i]])

##################################################
# Insere regra de produção na lista de regras,
# mantendo a referência com as listas de variáveis
# e de símbolos terminais
def adicionaRegraDeProducao(linhaRegra):
  simbolos = re.findall(regex, linhaRegra.split('#')[0])
  if simbolos[0].strip() in variaveis:
    r = []
    for n in range(len(simbolos) - 1):
      r.append(simbolos[n+1].strip())
    indice = variaveis.index(simbolos[0].strip())
    regras[indice].append(r)


#################################################
# Exibe a definição formal da gramática detalhada
# no arquivo
def exibeDefinicaoFormalGramatica():
  print("G = (")
  # Variáveis
  gramatica = "     {"+", ".join(variaveis)+"},"
  print(gramatica)
  # terminais
  gramatica = "     {"+", ".join(terminais)+"},"
  print(gramatica)
  # Regras de produção

  print("     {")
  for i in range(len(regras)):
    for j in range(len(regras[i])):
        if j == 0:
            gramatica = "       "+ regras[i][j] + " -> "
        else:
            r = " ".join(regras[i][j])
            if j > 1:
                gramatica = gramatica + " | "
            gramatica = gramatica + r
    print(gramatica+";")

  print("     },")
  # Variavel inicial
  print("     "+variavelInicial+"\n    )")

##################################################
# Programa principal

# CORRIGIR: temos que entender como o script receberá
# o nome do arquivo de entrada (provavelmente será um
# parâmetro da chamada do script).
arquivo = 'gram1.txt'

lines = [line.strip('\n') for line in open(arquivo)]

# Variáveis e listas usadas no programa
i = 0
terminais = []
variaveis = []
regras = []
variavelInicial = ''
palavraVazia = 'V'

for line in lines:
    if line[0] == '#':
        i = i + 1
    else: # adiciona às listas os termos sem hash
        if i == 1:
            adicionaTerminal(line)
        elif i == 2:
            terminais.sort()
            adicionaVariavel(line)
        elif i == 3:
            variaveis.sort()
            var = re.findall(regex, line.split('#')[0])
            variavelInicial = var[0].strip()
            inicializaRegras()
        elif i == 4:
            adicionaRegraDeProducao(line)
        else:
            print("Sessão do arquivo não esperada. Abortando execução.")


exibeDefinicaoFormalGramatica()
