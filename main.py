import random
import copy
import matplotlib.pyplot as plt
import numpy as np

class Populacao:
  def __init__(self, tamanho_populacao=10):
    self.tamanho_populacao = tamanho_populacao
    self.populacao = []
    self.fitness = 0

  def inicializacao(self):
    pass

  def mutacao(self):
    nova_lista = []
    for individuo in self.populacao:
      nova_lista.append(individuo.mutacao())
    return nova_lista

  def crossover(self):
    return []

  def selecionar(self, populacao1 = [], populacao2 = []):
    nova_lista = sorted(self.populacao, key=self._fitness_populacao, reverse=True)
    self.populacao = nova_lista[0:self.tamanho_populacao]

  def top_fitness(self):
    return self.top_individuo().fitness()

  def top_individuo(self):
    return self.populacao[0]

  def _fitness_populacao(self, individuo):
    return individuo.fitness()
  
class AlgoritmoGeneticoPopulacao:
  def __init__(self, populacao):
    self.populacao = populacao
    self.erro = float('inf')
    self.geracoes = 1

  def erro_final(self):
    return self.erro

  def qtd_geracoes(self):
    return self.geracoes

  def rodar(self, max_geracoes = 5000, imprimir_em_geracaoes = 100, erro_min = 0.01):
    print(f"Geração: {self.geracoes}, Erro: {round(self.erro,3)}, {self.populacao.top_individuo().imprime()}")

    while True:
      if self.geracoes >= max_geracoes or self.erro <= erro_min:
        print(f"Geração: {self.geracoes}, Erro: {self.erro}, {self.populacao.top_individuo().imprime()}")
        break

      populacao_mutada = self.populacao.mutacao()
      populacao_crossover = self.populacao.crossover()

      self.populacao.selecionar(populacao_mutada, populacao_crossover)
      fitness = self.populacao.top_fitness()

      if (1-fitness) < self.erro:
        self.erro = (1-fitness)

      self.geracoes += 1
      if self.geracoes % imprimir_em_geracaoes == 0:
        print(f"Geração: {self.geracoes}, Erro: {self.erro}, {self.populacao.top_individuo().imprime()}")
    return self.populacao.top_individuo()


# Dados do problema
ANALISES = {
    'Análise 1': ['Espectrofotômetro UV-VIS', 'Cromatógrafo Gasoso'],
    'Análise 2': ['Cromatógrafo Líquido', 'Espectrômetro Infravermelho'],
    'Análise 3': ['Microscópio', 'Balança Analítica'],
    'Análise 4': ['Espectrômetro de Massa'],
    'Análise 5': ['Agitador Magnético', 'Espectrômetro Infravermelho'],
    'Análise 6': ['Cromatógrafo Líquido', 'Espectrofotômetro UV-VIS'],
    'Análise 7': ['Espectrofotômetro UV-VIS', 'Microscópio'],
    'Análise 8': ['Cromatógrafo Gasoso'],
    'Análise 9': ['Espectrômetro Infravermelho', 'Balança Analítica'],
    'Análise 10': ['Espectrômetro de Massa', 'Cromatógrafo Gasoso']
}

RESTRICOES = {
    'Balança Analítica': 6,
    'Agitador Magnético': 4,
    'Cromatógrafo Líquido': 8,
    'Cromatógrafo Gasoso': 6,
    'Espectrofotômetro UV-VIS': 4,
    'Espectrômetro Infravermelho': 6,
    'Espectrômetro de Massa': 4,
    'Microscópio': 6
}

# Lista de todos os equipamentos
EQUIPAMENTOS = list(RESTRICOES.keys())
# Total de dias para o planejamento semanal
TOTAL_DIAS = 5  # Segunda a Sexta

class Agendamento:
    def __init__(self, cromossomo=None):
        # Um cromossomo é uma lista de tuplas (análise, equipamento, dia, hora)
        self.cromossomo = cromossomo or self.gerar_cromossomo_aleatorio()
        self._fitness_cache = None
    
    def gerar_cromossomo_aleatorio(self):
        cromossomo = []
        
        # Para cada análise
        for analise, equipamentos in ANALISES.items():
            # Para cada equipamento necessário para a análise
            for equipamento in equipamentos:
                # Escolha aleatória de dia e hora
                dia = random.randint(0, TOTAL_DIAS - 1)
                hora = random.randint(8, 17)  # Horário de trabalho de 8h às 17h
                
                # Adicionar ao cromossomo
                cromossomo.append((analise, equipamento, dia, hora))
        
        return cromossomo
    
    def fitness(self):
        # Se já calculado, retorna o valor em cache
        if self._fitness_cache is not None:
            return self._fitness_cache
        
        penalidades = 0
        
        # Verificar uso máximo diário de cada equipamento
        uso_diario_equipamentos = {}
        for eq in EQUIPAMENTOS:
            uso_diario_equipamentos[eq] = [0] * TOTAL_DIAS
        
        # Contar o uso de cada equipamento por dia
        for analise, equipamento, dia, hora in self.cromossomo:
            uso_diario_equipamentos[equipamento][dia] += 1
        
        # Penalizar excesso de uso diário
        for equipamento, uso_diario in uso_diario_equipamentos.items():
            for dia, uso in enumerate(uso_diario):
                if uso > RESTRICOES[equipamento]:
                    penalidades += (uso - RESTRICOES[equipamento])
        
        # Verificar conflitos de horário (mesmo equipamento, mesmo dia, mesma hora)
        horarios_ocupados = {}
        for analise, equipamento, dia, hora in self.cromossomo:
            chave = (equipamento, dia, hora)
            if chave in horarios_ocupados:
                penalidades += 1
            else:
                horarios_ocupados[chave] = analise
        
        # Verificar se a análise não está em 2 equipamentos ao mesmo tempo
        analises_horarios = {}
        for analise, equipamento, dia, hora in self.cromossomo:
            chave = (analise, dia, hora)
            if chave in analises_horarios:
                penalidades += 1
            else:
                analises_horarios[chave] = equipamento
        
        # Verificar se todas as análises têm todos os equipamentos necessários
        analises_equipamentos = {}
        for analise, equipamento, dia, hora in self.cromossomo:
            if analise not in analises_equipamentos:
                analises_equipamentos[analise] = set()
            analises_equipamentos[analise].add(equipamento)
        
        for analise, equipamentos in ANALISES.items():
            equipamentos_necessarios = set(equipamentos)
            equipamentos_agendados = analises_equipamentos.get(analise, set())
            if equipamentos_necessarios != equipamentos_agendados:
                penalidades += len(equipamentos_necessarios - equipamentos_agendados)
        
        # Verificar se os equipamentos de uma mesma análise estão próximos no tempo
        # (Preferência para que estejam no mesmo dia)
        cronograma_analises = {}
        for analise, equipamento, dia, hora in self.cromossomo:
            if analise not in cronograma_analises:
                cronograma_analises[analise] = []
            cronograma_analises[analise].append((dia, hora))
        
        for analise, horarios in cronograma_analises.items():
            if len(horarios) > 1:
                # Verificar se todos os equipamentos da análise estão no mesmo dia
                dias_distintos = len(set(dia for dia, _ in horarios))
                if dias_distintos > 1:
                    penalidades += 0.5 * (dias_distintos - 1)  # Penalidade menor por dias diferentes
        
        # Calcular o fitness normalizado (0 a 1, onde 1 é o melhor)
        # Quanto mais próximo de 0 for a penalidade, melhor o fitness
        max_penalidades = 3 * len(self.cromossomo)  # Um número alto para normalização
        fitness = 1 - min(penalidades / max_penalidades, 1)
        
        # Armazenar em cache
        self._fitness_cache = fitness
        return fitness
    
    def mutacao(self, taxa_mutacao = 0.1):
        novo_individuo = Agendamento(copy.deepcopy(self.cromossomo))
        
        for i in range(len(novo_individuo.cromossomo)):
            if random.random() < taxa_mutacao:
                analise, equipamento, dia, hora = novo_individuo.cromossomo[i]
                
                # 50% de chance de mudar o dia ou a hora
                if random.random() < 0.5:
                    dia = random.randint(0, TOTAL_DIAS - 1)
                else:
                    hora = random.randint(8, 17)
                
                novo_individuo.cromossomo[i] = (analise, equipamento, dia, hora)
        
        # Mutação adicional: trocar horários entre duas análises (10% de chance)
        if random.random() < 0.1 and len(novo_individuo.cromossomo) >= 2:
            idx1, idx2 = random.sample(range(len(novo_individuo.cromossomo)), 2)
            
            # Trocar apenas dia e hora, mantendo análise e equipamento
            analise1, equip1, dia1, hora1 = novo_individuo.cromossomo[idx1]
            analise2, equip2, dia2, hora2 = novo_individuo.cromossomo[idx2]
            
            novo_individuo.cromossomo[idx1] = (analise1, equip1, dia2, hora2)
            novo_individuo.cromossomo[idx2] = (analise2, equip2, dia1, hora1)
        
        # Invalidar o cache de fitness
        novo_individuo._fitness_cache = None
        return novo_individuo
    
    def crossover(self, outro_individuo):
        # Crossover de ponto único
        ponto_corte = random.randint(1, len(self.cromossomo) - 1)
        
        filho1_cromossomo = self.cromossomo[:ponto_corte] + outro_individuo.cromossomo[ponto_corte:]
        filho2_cromossomo = outro_individuo.cromossomo[:ponto_corte] + self.cromossomo[ponto_corte:]
        
        return Agendamento(filho1_cromossomo), Agendamento(filho2_cromossomo)
    
    def imprime(self):
        return f"Fitness: {self.fitness():.4f}"
    
    def imprimir_agendamento(self):
        # Ordenar por dia, hora e equipamento para melhor visualização
        agendamento_ordenado = sorted(self.cromossomo, key=lambda x: (x[2], x[3], x[1]))
        
        dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
        
        print("\n=== AGENDAMENTO DETALHADO ===")
        for analise, equipamento, dia, hora in agendamento_ordenado:
            print(f"Dia: {dias[dia]}, Hora: {hora}:00 - {analise} - {equipamento}")
    
    def plotar_agendamento(self):
        equipamentos_indices = {equip: i for i, equip in enumerate(EQUIPAMENTOS)}
        plt.figure(figsize=(15, 8))

        cores = plt.cm.tab10(np.linspace(0, 1, len(ANALISES)))
        cores_analises = {analise: cores[i] for i, analise in enumerate(ANALISES.keys())}

        for analise, equipamento, dia, hora in self.cromossomo:
            x = dia + (hora - 8) / 9  # Ajusta para horário (8h às 17h → escala 0 a 1)
            y = equipamentos_indices[equipamento]

            plt.plot([x], [y], 'o', markersize=10, color=cores_analises[analise],
                    label=analise if analise not in plt.gca().get_legend_handles_labels()[1] else "")

            plt.text(x, y, f"{hora}h", fontsize=8, ha='right', va='bottom', color='black')

        plt.yticks(range(len(EQUIPAMENTOS)), EQUIPAMENTOS)
        plt.xticks(range(TOTAL_DIAS), ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"])

        plt.xlim(-0.5, TOTAL_DIAS - 0.5)
        plt.ylim(-0.5, len(EQUIPAMENTOS) - 0.5)
        plt.grid(True, linestyle='--', alpha=0.7)

        plt.title('Agendamento Semanal do Laboratório')
        plt.xlabel('Dia da Semana')
        plt.ylabel('Equipamento')

        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        plt.legend(by_label.values(), by_label.keys(), loc='upper center',
                bbox_to_anchor=(0.5, -0.15), ncol=5)

        plt.tight_layout()
        plt.show()


class PopulacaoLaboratorio(Populacao):
    def __init__(self, tamanho_populacao=50):
        super().__init__(tamanho_populacao=tamanho_populacao)
        self.inicializacao()
    
    def inicializacao(self):
        # Inicializar a população com indivíduos aleatórios
        self.populacao = [Agendamento() for _ in range(self.tamanho_populacao)]
    
    def mutacao(self):
        # Aplicar mutação em cada indivíduo da população
        return super().mutacao()
    
    def crossover(self):
        # Implementação do crossover
        nova_lista = []
        
        # Embaralhar a população para seleção aleatória
        populacao_embaralhada = random.sample(self.populacao, len(self.populacao))
        
        # Aplicar crossover entre pares consecutivos
        for i in range(0, len(populacao_embaralhada) - 1, 2):
            pai1 = populacao_embaralhada[i]
            pai2 = populacao_embaralhada[i + 1]
            
            filho1, filho2 = pai1.crossover(pai2)
            nova_lista.extend([filho1, filho2])
        
        return nova_lista
    
    def selecionar(self, populacao_mutada=[], populacao_crossover=[]):
        # Combinar todas as populações
        populacao_combinada = self.populacao + populacao_mutada + populacao_crossover
        
        # Selecionar os melhores indivíduos - elitismo
        self.populacao = sorted(populacao_combinada, key=lambda x: x.fitness(), reverse=True)[:self.tamanho_populacao]


# Função principal para executar o algoritmo genético
def resolver_agendamento_laboratorio():
    # Criar e inicializar a população
    populacao = PopulacaoLaboratorio(tamanho_populacao=100)
    
    # Criar o algoritmo genético
    ag = AlgoritmoGeneticoPopulacao(populacao)
    
    # Executar o algoritmo genético
    melhor_solucao = ag.rodar(max_geracoes=1000, imprimir_em_geracaoes=100, erro_min=0.001)
    
    # Imprimir o resultado
    print("\n=== MELHOR SOLUÇÃO ENCONTRADA ===")
    print(f"Fitness: {melhor_solucao.fitness():.4f}")
    print(f"Gerações: {ag.qtd_geracoes()}")
    print(f"Erro final: {ag.erro_final():.6f}")
    
    # Mostrar o agendamento detalhado
    melhor_solucao.imprimir_agendamento()
    
    # Plotar o agendamento
    melhor_solucao.plotar_agendamento()
    
    # Analisar a solução
    analisar_solucao(melhor_solucao)
    
    return melhor_solucao


def analisar_solucao(solucao):
    """Analisa a solução encontrada em termos de restrições atendidas"""
    print("\n=== ANÁLISE DA SOLUÇÃO ===")
    
    # Contar análises completas
    analises_equipamentos = {}
    for analise, equipamento, dia, hora in solucao.cromossomo:
        if analise not in analises_equipamentos:
            analises_equipamentos[analise] = set()
        analises_equipamentos[analise].add(equipamento)
    
    analises_completas = 0
    for analise, equipamentos in ANALISES.items():
        equipamentos_necessarios = set(equipamentos)
        equipamentos_agendados = analises_equipamentos.get(analise, set())
        if equipamentos_necessarios == equipamentos_agendados:
            analises_completas += 1
    
    print(f"Análises completas: {analises_completas} de {len(ANALISES)}")
    
    # Verificar uso diário de equipamentos
    uso_diario = {equip: [0] * TOTAL_DIAS for equip in EQUIPAMENTOS}
    for analise, equipamento, dia, hora in solucao.cromossomo:
        uso_diario[equipamento][dia] += 1
    
    dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
    restricoes_violadas = 0
    
    print("\nUso diário de equipamentos (horas):")
    for equipamento, uso in uso_diario.items():
        print(f"{equipamento}: ", end="")
        for dia in range(TOTAL_DIAS):
            status = "✓" if uso[dia] <= RESTRICOES[equipamento] else "✗"
            if status == "✗":
                restricoes_violadas += 1
            print(f"{dias[dia]}: {uso[dia]}/{RESTRICOES[equipamento]} {status} | ", end="")
        print()
    
    print(f"\nRestrições de capacidade violadas: {restricoes_violadas}")
    
    # Verificar conflitos de horário
    conflitos = 0
    horarios_ocupados = {}
    for analise, equipamento, dia, hora in solucao.cromossomo:
        chave = (equipamento, dia, hora)
        if chave in horarios_ocupados:
            conflitos += 1
    
    print(f"Conflitos de horário (mesmo equipamento): {conflitos}")
    
    # Verificar análises em múltiplos equipamentos simultaneamente
    conflitos_analise = 0
    analises_horarios = {}
    for analise, equipamento, dia, hora in solucao.cromossomo:
        chave = (analise, dia, hora)
        if chave in analises_horarios:
            conflitos_analise += 1
    
    print(f"Conflitos de horário (mesma análise): {conflitos_analise}")
    
    # Verificar dias distintos para a mesma análise
    dias_por_analise = {}
    for analise, equipamento, dia, hora in solucao.cromossomo:
        if analise not in dias_por_analise:
            dias_por_analise[analise] = set()
        dias_por_analise[analise].add(dia)

# Executar a solução
if __name__ == "__main__":
    melhor_solucao = resolver_agendamento_laboratorio()