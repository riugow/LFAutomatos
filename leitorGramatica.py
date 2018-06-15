import re

regex = re.compile(r"\[(.*?)\]")

#frase = "Mary saw Jupiter with Mars in the sky"

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
  gramatica = "     V = {"+", ".join(variaveis)+"},"
  print(gramatica)
  # terminais
  gramatica = "     T = {"+", ".join(terminais)+"},"
  print(gramatica)
  # Regras de produção

  print("     P = {")
  for i in range(len(regras)):
    for j in range(len(regras[i])):
        if j == 0:
            gramatica = "           "+ regras[i][j] + " -> "
        else:
            r = " ".join(regras[i][j])
            if j > 1:
                gramatica = gramatica + " | "
            gramatica = gramatica + r
    print(gramatica+";")

  print("         },")
  # Variavel inicial
  print("     "+variavelInicial+"\n    )")

##################################################
# imprime a tabela de derivacao
def imprimeTabelaDeDerivacao(tabela, termos):
    impressao = ['+']
    for i in range(len(termos) + 1):
        impressao.append('|')
        impressao.append('+')

    bordaHorizontal = ''
    largura = 0
    for i in range(len(termos)):
        largura = len(termos[i])
        for j in range(i, len(tabela)):
            if len(', '.join(tabela[j][i])) > largura:
                largura = len(', '.join(tabela[j][i]))
        bordaHorizontal = '-'
        for j in range(largura):
            bordaHorizontal += '-'
        bordaHorizontal += '-+'
        for j in range(i*2, len(impressao), 2):
            impressao[j] += bordaHorizontal
        for j in range(i, len(tabela)):
            termo = ' ' + ', '.join(tabela[j][i])
            for k in range(largura - len(termo) + 1):
                termo += ' '
            impressao[j*2+1] += termo + ' |'
        termo = ' ' + ''.join(termos[i])
        for j in range(largura - len(termo) + 1):
            termo += ' '
        impressao[len(impressao) - 2] += termo + ' |'
    print('\n'.join(impressao))
##################################################
# simplifica a gramática
def simplificaGramatica():
    print("Aplicando algoritmos de simplificação da gramática.")
    print("Passo 1: Excluindo produções vazias")
    # Passo 1 - Etapa 1
    variaveisProducoesVazias = ['V']
    tamanhoDerivacoesVazias = 0
    existemProducoesVazias = True
    while(existemProducoesVazias):
        existemProducoesVazias = False
        while (tamanhoDerivacoesVazias != len(variaveisProducoesVazias)):
            if 'V' in variaveisProducoesVazias:
                tamanhoDerivacoesVazias = 0
            else:
                tamanhoDerivacoesVazias = len(variaveisProducoesVazias)
            for i in range(len(regras)):
                for j in range(1, len(regras[i])):
                    for var in variaveisProducoesVazias:
                        if var in regras[i][j] and len(regras[i][j]) == 1 and regras[i][0] not in variaveisProducoesVazias:
                            variaveisProducoesVazias.append(regras[i][0])
                            existemProducoesVazias = True
                if ['V'] in regras[i]:
                    regras[i].remove(['V'])
            if 'V' in variaveisProducoesVazias:
                variaveisProducoesVazias.remove('V')
        # Passo 1 - Etapa 2
        derivacoesCorrigidas = True
        while (derivacoesCorrigidas == True):
            derivacoesCorrigidas = False
            for i in range(len(regras)):
                for j in range(1, len(regras[i])):
                    for var in variaveisProducoesVazias:
                        if var in regras[i][j] and len(regras[i][j]) > 1:
                            for k in [n for n,x in enumerate(regras[i][j]) if x == var]:
                                r = regras[i][j][:]
                                r.pop(k)
                                if r not in regras[i]:
                                    regras[i].append(r)
                                    derivacoesCorrigidas = True
    # Passo 1 - Etapa 3
    derivacoesVariavelInicial = [s for s in regras if variavelInicial in s][0]
    for v in derivacoesVariavelInicial[1:]:
        vazia = ['V']
        if len(v) == 1 and v[0] in variaveisProducoesVazias and vazia not in regras[regras.index(derivacoesVariavelInicial)]:
            regras[regras.index(derivacoesVariavelInicial)].append(vazia)
    exibeDefinicaoFormalGramatica()
    print("Passo 2: Excluindo produções que substituem variáveis")
    # Passo 2 - Etapa 1
    fecho = []
    for i in range(len(regras)):
        for derivacao in regras[i][1:]:
            for v in variaveis:
                if v in derivacao and len(derivacao) == 1:
                    f = [regras[i][0], derivacao[0]]
                    fecho.append(f)
                    # Passo 2 - Etapa 2
                    regras[i].remove(derivacao)
    # Passo 2 - Etapa 2 (sim, começou no loop acima e terminou aqui)
    for f in fecho:
        origem = [s for s in regras if f[0] in s][0]
        destino = [s for s in regras if f[1] in s][0][1:]
        for derivacao in destino:
            regras[regras.index(origem)].append(derivacao)
    exibeDefinicaoFormalGramatica()
    print("Passo 3: Excluindo símbolos inúteis")
    # Passo 3 - Etapa 1
    variaveisGeradoras = []
    terminaisEVariaveis = terminais[:]
    tamanhoVariaveisGeradoras = -1
    while (tamanhoVariaveisGeradoras != len(variaveisGeradoras)):
        tamanhoVariaveisGeradoras = len(variaveisGeradoras)
        for i in range(len(regras)):
            for j in range(1, len(regras[i])):
                for t in terminaisEVariaveis:
                    if t in regras[i][j] and regras[i][0] not in variaveisGeradoras:
                        variaveisGeradoras.append(regras[i][0])
                        terminaisEVariaveis.append(regras[i][0])

    for var in variaveis:
        if var not in variaveisGeradoras:
            for i in range(len(regras)):
                if regras[i][0] == var:
                    derivacaoARemover = [s for s in regras if var in s][0]
                    regras.remove(derivacaoARemover)
                for derivacao in regras[i][1:]:
                    if var in derivacao:
                        regras[i].remove(derivacao)

    for var in variaveis:
        if var not in variaveisGeradoras:
            variaveis.remove(var)

    # Passo 3 - Etapa 2
    variaveisDerivadas = [variavelInicial]
    terminaisAlcancados = []
    tamVariaveisDerivadas = 0
    tamTerminaisAlcancados = -1
    while tamVariaveisDerivadas != len(variaveisDerivadas) and tamTerminaisAlcancados != len(terminaisAlcancados):
        tamVariaveisDerivadas = len(variaveisDerivadas)
        tamTerminaisAlcancados = len(terminaisAlcancados)
        for i in range(len(regras)):
            for derivacao in regras[i][1:]:
                for var in variaveis:
                    if var in derivacao and var not in variaveisDerivadas:
                        variaveisDerivadas.append(var)
                for term in terminais:
                    if term in derivacao and term not in terminaisAlcancados:
                        terminaisAlcancados.append(term)

    for var in variaveis:
        if var not in variaveisDerivadas:
            for i in range(len(regras)):
                if regras[i][0] == var:
                    derivacaoARemover = [s for s in regras if var in s][0]
                    regras.remove(derivacaoARemover)
                for derivacao in regras[i][1:]:
                    if var in derivacao:
                        regras[i].remove(derivacao)

    for term in terminais:
        if term not in terminaisAlcancados:
            for i in range(len(regras)):
                for derivacao in regras[i][1:]:
                    if term in derivacao:
                        regras[i].remove(derivacao)

    for var in variaveis:
        if var not in variaveisDerivadas:
            variaveis.remove(var)

    for term in terminais:
        if term not in terminaisAlcancados:
            terminais.remove(term)

    exibeDefinicaoFormalGramatica()


##################################################
# Cria uma variável Vn ou Tn, sendo n um número natural
def criaVariavel(tipoVariavel = True):
    constante = 'V'
    if tipoVariavel == False:
        constante = 'T'
    i = 1
    novaVariavel = constante + str(i)
    while novaVariavel in variaveis:
        i = i + 1
        novaVariavel = constante + str(i)
    return novaVariavel

##################################################
# FNC
def formaNormalChomsky():
    print('Normalizando a gramática de acordo com a Forma Normal de Chomsky')
    # Etapa 1 : confere / cria derivações Variavel > Terminal
    terminaisNormalizados = []
    for i in range(len(regras)):
        for t in terminais:
            if regras[i][1] == [t]:
                terminaisNormalizados.append(t)

    for t in terminais:
        novaDerivacao = []
        if t not in terminaisNormalizados:
            novaVariavel = criaVariavel(False)
            terminaisNormalizados.append(t)
            terminalSubstituido = False
            for i in range(len(regras)):
                for j in range(1, len(regras[i])):
                    if len(regras[i][j]) > 1 and t in regras[i][j]:
                        regras[i][j] = [novaVariavel if x==t else x for x in regras[i][j]][:]
                        terminalSubstituido = True
            if terminalSubstituido:
                d = []
                d.append(novaVariavel)
                variaveis.append(novaVariavel)
                novaDerivacao.append(t)
                d.append(novaDerivacao)
                regras.append(d)

    # Etapa 2 : confere / reduz derivações com mais de três variáveis à direita
    for i in range(len(regras)):
        for j in range(1, len(regras[i])):
            derivacaoSubstituta = []
            #Para produções de tamanho maior que 2, simplificar
            if len(regras[i][j]) > 2:
                novaDerivacao = regras[i][j][:]
                novaDerivacao.pop(0)
                variavelSubstituta = criaVariavel()
                for k in range(len(regras)):
                    if novaDerivacao == regras[k][1] and len(regras[k]) < 3:
                        variavelSubstituta = regras[k][0]

                derivacaoSubstituta.append(regras[i][j][0])
                derivacaoSubstituta.append(variavelSubstituta)
                regras[i][j] = derivacaoSubstituta[:]

                if (variavelSubstituta not in variaveis):
                    variaveis.append(variavelSubstituta)
                    d = []
                    d.append(variavelSubstituta)
                    d.append(novaDerivacao)
                    regras.append(d)

    exibeDefinicaoFormalGramatica()
##################################################
# Reconhecimento de entrada usando o algoritmo de
# Cocke-Younger-Kasami
def cyk(entrada):
    print('Verificando a aceitação da expressão informada pela gramática')
    print('usando o algoritmo de Cocke-Younger-Kasami:')
    #print('Verificando a aceitação da expressão\'' + entrada + '\'')
    #print('pela gramática usando o algoritmo de Cocke-Younger-Kasami:')

    termos = entrada.split()
    tabelaTriangular = []
    linha = []
    for termo in termos:
        var = []
        for i in range(len(regras)):
            for derivacao in regras[i][1:]:
                if termo in derivacao:
                    var.append(regras[i][0])
        linha.append(var)
    tabelaTriangular.append(linha)

    for n in range(len(termos) - 1):
        linha = []
        for r in range(len(tabelaTriangular[0])-1):
            var = []
            for s in range(len(tabelaTriangular)):
                for i in range(len(regras)):
                    for derivacao in regras[i][1:]:
                        if len(derivacao) == 2:
                            if derivacao[0] in tabelaTriangular[len(tabelaTriangular) - s - 1][r] and derivacao[1] in tabelaTriangular[s][r + s + 1]:
                                if regras[i][0] not in var:
                                    var.append(regras[i][0])
            linha.append(var)
        tabelaTriangular.insert(0, linha)
    if variavelInicial in tabelaTriangular[0][0]:
        print('A expressão informada foi reconhecida pela gramática!')
        imprimeTabelaDeDerivacao(tabelaTriangular, termos)
    else:
        print('A expressão informada NÃO foi reconhecida pela gramática.')
##################################################
# Programa principal

filename = input('Informe o nome do arquivo: ')
#filename = 'gram3.txt'

try:
    arquivo = open(filename)
except IOError:
    print("***ERROR! Invalid filename***")

lines = [line.strip('\n') for line in arquivo]

# Variáveis e listas usadas no programa
i = 0
terminais = []
variaveis = []
regras = []
variavelInicial = ''
palavraVazia = 'V'

for line in lines:
    if line[0] == '#':
        if line.startswith('#Terminais'):
            i = 1
        elif line.startswith('#Variaveis'):
            i = 2
        elif line.startswith('#Inicial'):
            i = 3
        elif line.startswith('#Regras'):
            i = 4
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
            i = 5
            break

if (i != 5):
    exibeDefinicaoFormalGramatica()
    simplificaGramatica()
    formaNormalChomsky()
    print('Informe a expressão a ter ser reconhecimento verificado pela gramática.')
    frase = input('NOTA: Separe cada termo usando um espaço em branco: ')
    cyk(frase)
