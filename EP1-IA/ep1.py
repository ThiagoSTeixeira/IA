"""
 NUMERO USP,
  DECLARO QUE SOU A UNICA PESSOA AUTORA E RESPONSAVEL POR ESSE PROGRAMA.
  TODAS AS PARTES ORIGINAIS DESSE EXERCICIO PROGRAMA (EP) FORAM
  DESENVOLVIDAS E IMPLEMENTADAS POR MIM SEGUINDO AS INSTRUCOES
  DESSE EP E, PORTANTO, NAO CONSTITUEM ATO DE DESONESTIDADE ACADEMICA,
  FALTA DE ETICA OU PLAGIO.
  DECLARO TAMBEM QUE SOU A PESSOA RESPONSAVEL POR TODAS AS COPIAS
  DESSE PROGRAMA E QUE NAO DISTRIBUI OU FACILITEI A
  SUA DISTRIBUICAO. ESTOU CIENTE QUE OS CASOS DE PLAGIO E
  DESONESTIDADE ACADEMICA SERAO TRATADOS SEGUNDO OS CRITERIOS
  DIVULGADOS NA PAGINA DA DISCIPLINA.
  ENTENDO QUE EPS SEM ASSINATURA NAO SERAO CORRIGIDOS E,
  AINDA ASSIM, PODERAO SER PUNIDOS POR DESONESTIDADE ACADEMICA.

  Nome : Thiago Santos Teixeira
  NUSP : 10736987

  Referencias: Com excecao das rotinas fornecidas no enunciado
  e em sala de aula, caso voce tenha utilizado alguma referencia,
  liste-as abaixo para que o seu programa nao seja considerado
  plagio ou irregular.

  Exemplo:
  - O algoritmo Quicksort foi baseado em:
  https://pt.wikipedia.org/wiki/Quicksort
  http://www.ime.usp.br/~pf/algoritmos/aulas/quick.html
"""

import util

############################################################
# Part 1: Segmentation problem under a unigram model

class SegmentationProblem(util.Problem):
    def __init__(self, query, unigramCost):
        self.query = query
        self.unigramCost = unigramCost

    def isState(self, state):
        """ Metodo que implementa verificacao de estado """
        for i in range(state):
            if len(state[i]>len(self.query)): return False
        return True

    def initialState(self):
        """ Metodo que implementa retorno da posicao inicial """
        return ((self.query, ""))

    def actions(self, state):
        """ Metodo que implementa retorno da lista de acoes validas
        para um determinado estado
        """
        acoes = [] #lista de tuplas
        entrada = state[0]
        for i in range(len(entrada)):
            dire=entrada[-i-1:]
            esq = entrada[:-i-1]
            if state[1] == '': add = [dire]
            else: add = [state[1]]+[dire]
            add = ' '.join(add)
            acoes.append((esq, add))
        return acoes

    def nextState(self, state, action):
        """ Metodo que implementa funcao de transicao """
        return ((action[0], action[1]))

    def isGoalState(self, state):
        """ Metodo que implementa teste de meta """
        return state[0] == ''

    def stepCost(self, state, action):
        """ Metodo que implementa funcao custo """
        #o custo sera uma subtracao entre o custo da acao e do estado
        sCost = sum([self.unigramCost(i) for i in state[1].split()])
        aCost = sum([self.unigramCost(i) for i in action[1].split()])
        return aCost - sCost

def segmentWords(query, unigramCost):

    if len(query) == 0:
        return ''
     
    # BEGIN_YOUR_CODE 
    sp = SegmentationProblem(query, unigramCost)
    goal = util.uniformCostSearch(sp)
    return ' '.join(reversed(goal.state[1].split()))
    # Voce pode usar a função getSolution para recuperar a sua solução a partir do no meta
    # valid,solution  = util.getSolution(goalNode,problem)

    #return resp

    # END_YOUR_CODE

############################################################
# Part 2: Vowel insertion problem under a bigram cost

class VowelInsertionProblem(util.Problem):
    def __init__(self, queryWords, bigramCost, possibleFills):
        self.queryWords = queryWords
        self.bigramCost = bigramCost
        self.possibleFills = possibleFills

    def isState(self, state):
        """ Metodo  que implementa verificacao de estado """
        return True

    def initialState(self):
        """ Metodo  que implementa retorno da posicao inicial """
        qw = self.queryWords
        qw.insert(0, "-BEGIN-") #palavra especial do enunciado
        qw = ' '.join(qw)
        return((qw, ""))

    def actions(self, state):
        """ Metodo  que implementa retorno da lista de acoes validas
        para um determinado estado
        """
        acoes = []
        entrada = state[0].split()
        if len(entrada) >= 2:
            pf = self.possibleFills(entrada[1])
            if pf: acoes = [(entrada[0], i) for i in pf]
            else: acoes.append(("", entrada[1]))
        else:
            pf = self.possibleFills(entrada[0])
            acoes = [("", i) for i in pf]
        return acoes

    def nextState(self, state, action):
        """ Metodo que implementa funcao de transicao """
        antiga = state[0].split()
        nova = state[1]
        if action[0]:
            antiga.pop(0)
            antiga.pop(0)
            nova = state[1]+" "+action[1]
            if antiga:
                antiga.insert(0, action[1])
                antiga=" ".join(antiga)
                return((antiga, nova))
            return(("", nova))
        return(("", action[1]))

    def isGoalState(self, state):
        """ Metodo que implementa teste de meta """
        return state[0]=="" or state[0]=="-BEGIN-"

    def stepCost(self, state, action):
        """ Metodo que implementa funcao custo """
        return self.bigramCost(action[0], action[1])

def insertVowels(queryWords, bigramCost, possibleFills):
    # BEGIN_YOUR_CODE 
    obj = util.uniformCostSearch(VowelInsertionProblem(queryWords, bigramCost, possibleFills))
    return " ".join(obj.state[1].split())
    # Voce pode usar a função getSolution para recuperar a sua solução a partir do no meta
    # valid,solution  = util.getSolution(goalNode,problem)

    #raise NotImplementedError
    # END_YOUR_CODE

############################################################


def getRealCosts(corpus='corpus.txt'):

    """ Retorna as funcoes de custo unigrama, bigrama e possiveis fills obtidas a partir do corpus."""
    
    _realUnigramCost, _realBigramCost, _possibleFills = None, None, None
    if _realUnigramCost is None:
        print('Training language cost functions [corpus: '+ corpus+']... ')
        
        _realUnigramCost, _realBigramCost = util.makeLanguageModels(corpus)
        _possibleFills = util.makeInverseRemovalDictionary(corpus, 'aeiou')

        print('Done!')

    return _realUnigramCost, _realBigramCost, _possibleFills

def main():
    """ Voce pode/deve editar o main() para testar melhor sua implementacao.

    A titulo de exemplo, incluimos apenas algumas chamadas simples para
    lhe dar uma ideia de como instanciar e chamar suas funcoes.
    Descomente as linhas que julgar conveniente ou crie seus proprios testes.
    """
    unigramCost, bigramCost, possibleFills  =  getRealCosts()
    
    resulSegment = segmentWords('believeinyourselfhavefaithinyourabilities', unigramCost)
    print(resulSegment)
    

    resultInsert = insertVowels('smtms ltr bcms nvr'.split(), bigramCost, possibleFills)
    print(resultInsert)

if __name__ == '__main__':
    main()
