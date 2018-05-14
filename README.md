# LFAutomatos

Pendências:
 - Organizar o código "solto" (escopo global) em funções (pelo menos uma para ler o conteúdo do arquivo e construir as listas de símbolos da gramática);
 - Melhorar a expressão regular que identifica os símbolos nas linhas do arquivo, evitando que ela identifique elementos após um caractere de início de comentário (#)

BUGS!
 - CORRIGIDO (Se uma variável não tiver regras definidas na gramática, o programa ainda exibe a variável seguida de uma seta pra direita. Ele precisa prever este cenário.)
 - CORRIGIDO (As seções do arquivo estão sendo estritamente distintas pela aparição de um caractere # no início da linha. Esta identificação deve ser melhorada, verificando o nome da seção após este caractere. Outras linhas com este caractere, mas sem o nome da seção, devem ser simplesmente ignoradas.)
