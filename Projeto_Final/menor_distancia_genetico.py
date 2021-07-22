import random

class Ponto:
    def __init__(self, ponto, x, y):
        self.ponto = ponto
        self.x = x
        self.y = y

    def distancia(self, ponto):
        eixo_x = abs(self.x - ponto.x)
        eixo_y = abs(self.y - ponto.y)
        return eixo_x + eixo_y

    def __repr__(self):
        return f'({self.nome_ponto}, {self.x}, {self.y})'

    def __getitem__(self, indice):
        if indice == 0:
            return self.ponto

        elif indice == 1:
            return self.x

        elif indice == 2:
            return self.y

    
# ==================== Classe para calcular o Fitness (Pontuação de "mais aptidão") ====================

class Fitness:
    def __init__(self, rota):
        self.rota = rota
        self.distancia = 0
        self.fitness = 0.0
    
    def distanciaRota(self):
        if self.distancia ==0:
            distanciaCaminho = 0
            for i in range(0, len(self.rota)):
                doPonto = self.rota[i]
                aoPonto = None
                
                if i + 1 < len(self.rota):
                    aoPonto = self.rota[i + 1]

                else:
                    aoPonto = self.rota[0]
                
                distanciaCaminho += doPonto.distancia(aoPonto)

            self.distancia = distanciaCaminho
        return self.distancia
    
    def rotaFitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.distanciaRota())
        return self.fitness
        
# ==================== Entrada ====================

lista_matriz = []
with open('matriz.txt', 'r') as matriz:
    for line in matriz:
        linha = []
        for i in line:
            if i != '\n' and i != ' ':
                linha.append(i)
        lista_matriz.append(linha)

def pontos(lista_matriz):
    vertices = []

    for index, linha in enumerate(lista_matriz):
        for pos, elem in enumerate(linha):
            if elem != '0':
                ponto = (elem, index, pos)
                vertices.append(ponto)

    return vertices


vertices = pontos(lista_matriz)


lista_pontos = []
for ponto in vertices:
    if ponto[0] == 'R':
        ponto_partida = Ponto(ponto[0], ponto[1], ponto[2])

    else:
        lista_pontos.append(Ponto(ponto[0], ponto[1], ponto[2]))

# ==================== Para criar a população inicial ====================

def criaRota(lista_pontos):
    rota = random.sample(lista_pontos, len(lista_pontos))
    rota.insert(0, ponto_partida)
    return rota

def populacao_ini(lista_pontos, tam_pop):
    populacao = []

    for i in range(0, tam_pop):
        populacao.append(criaRota(lista_pontos))
    return populacao

# ==================== Escolha do melhor indivíduo ====================

def rankRotas(populacao):
    fitnessResultados = {}
    for i in range(0,len(populacao)):
        fitnessResultados[i] = Fitness(populacao[i]).rotaFitness() 
    return sorted(fitnessResultados.items(), key=lambda x: x[1], reverse=True)



# ==================== Faz a escolha das gerações futuras com base no elitismo, favorecendo melhores resultados ====================

def selecao(pop_escolhida, tam_elitismo):
    resultado_selecao = []
    tam_populacao = len(pop_escolhida)

    for i in range(0, tam_elitismo):
        resultado_selecao.append(pop_escolhida[i])


    for j in range(0, len(pop_escolhida) - tam_elitismo):
        
        individuo1 = pop_escolhida[random.randint(0, tam_populacao-1)]
        individuo2 = pop_escolhida[random.randint(0, tam_populacao-1)]
        
        individuo1_fitness = individuo1[1]
        individuo2_fitness = individuo2[1]

        if individuo1_fitness >= individuo2_fitness:
            resultado_selecao.append(individuo1)
        else:
            resultado_selecao.append(individuo2)
    return resultado_selecao


def individuos_selecionados(populacao, resultado_selecao):
    selecionados = []
    for i in range(0, len(resultado_selecao)):
        indice = resultado_selecao[i][0]
        selecionados.append(populacao[indice])
    return selecionados



# ==================== Faz o cruzamento entre os pais para obter os filhos ====================

def cruzamento(pai1, pai2):
    filho = []
    filho1 = []
    filho2 = []

    gene_a = int(random.random() * len(pai1))
    gene_b = int(random.random() * len(pai2))

    gene_ini = min(gene_a, gene_b)
    gene_fim = max(gene_a, gene_b)

    filho1.append(ponto_partida)

    for i in range(gene_ini, gene_fim):
        if ponto_partida == pai1[i]:
            continue
        else:
            filho1.append(pai1[i])

    for j in range(len(pai2)):
        if ponto_partida == pai2[j]:
            continue
        elif pai2[j] not in filho1:
            filho2.append(pai2[j])

    filho = filho1 + filho2
    return filho

def cruzamento_populacao(selecionados, tam_elitismo):
    filhos = []
    tamanho = len(selecionados) - tam_elitismo
    porcao = random.sample(selecionados, len(selecionados))

    for i in range(0, tam_elitismo):
        filhos.append(selecionados[i])

    for j in range(0, tamanho):
        filho = cruzamento(porcao[j], porcao[len(selecionados)-i-1])
        filhos.append(filho)
    return filhos

# ==================== Gera a mutação de genes com base na aleatoriedade ====================

def mutacao(individuo, taxa_mutacao):
    for indice_cidade in range(1, len(individuo)):
        if random.random() < taxa_mutacao:
            cidade_troca = int(random.random() * len(individuo))
            while cidade_troca == 0:
                cidade_troca = int(random.random() * len(individuo))

            cidade1 = individuo[indice_cidade]
            cidade2 = individuo[cidade_troca]

            individuo[indice_cidade] = cidade2
            individuo[cidade_troca] = cidade1

    return individuo


def mutacao_populacao(populacao, taxa_mutacao):
    populacao_mutada = []
    for indice_individuo in range(0, len(populacao)):
        individuo_mutado = mutacao(populacao[indice_individuo], taxa_mutacao)
        populacao_mutada.append(individuo_mutado)
    return populacao_mutada



def nova_geracao(populacao_atual, tam_elistimo, taxa_mutacao):
    populacao_classificada = rankRotas(populacao_atual)
    resultado_selecao = selecao(populacao_classificada, tam_elistimo)
    individuos_selecionados_selecao = individuos_selecionados(populacao_atual, resultado_selecao)
    filhos = cruzamento_populacao(individuos_selecionados_selecao, tam_elistimo)
    nova_geracao = mutacao_populacao(filhos, taxa_mutacao)
    return nova_geracao 


qnt_geracoes = 300
tam_elitismo = 20
taxa_mutacao = 0.05
tam_populacao = 200
populacao_atual = populacao_ini(lista_pontos, tam_populacao)

for i in range(0, qnt_geracoes):
    populacao_atual = nova_geracao(populacao_atual, tam_elitismo, taxa_mutacao)
    
indice = rankRotas(populacao_atual)[0][0]
melhor_rota = populacao_atual[indice]
print(f'Distância: {1/ rankRotas(populacao_atual)[0][1]} Dronômetros')

for i in range(len(melhor_rota)):
    print(melhor_rota[i][0], end=' ')