import random as rd
import math

rd.seed()

def aleatorio():
    u = rd.random() # Generate a number between [0.0, 1.0)
    u = 1.0 - u # Returns a number between (0.0, 1.0]
    return u

# MAIN:
# Simulador de um caixa onde clientes cheguem em média a cada 10 segundos,
# e o caixa gaste em média 8segundos para atender cada pessoa.
#
# Utilização ou Ocupação = fração de tempo que o caixa permanecerá ocupado.
# Utilização = 0.8.
#
# O tempo entre a chegada de clientes, bem como o tempo de atendimento devem
# ser gerados de maneira pseudoaleatória através da variável aleatória exponencial.
tempo_medio_clientes = float(input("Informe o tempo medio entre a chegada de clientes (segundos): "))
tempo_medio_clientes = 1.0 / tempo_medio_clientes

tempo_medio_atendimento = float(input("Informe o tempo medio gasto para atender cada pessoa (segundos): "))
tempo_medio_atendimento = 1.0 / tempo_medio_atendimento

tempo = 0.0 # tempo em que a simulação está (tempo decorrido)
tempo_simulacao = float(input("Informe o tempo total de simulacao (segundos): ")) # tempo total de simulacao

# Armazena o tempo de chegada do próximo cliente
chegada_cliente = float((-1.0/tempo_medio_clientes) * math.log(aleatorio()))

# Armazena o tempo em que o cliente que estiver sendo atendido sairá do comércio
saida_atendimento = 0.0

fila = 0.0

# Armazena a Utilização
util = 0.0

# Armazena o número de eventos para o cálculo de E[N] e E[W]
numEventosEN = 0.0
numEventosEWa = 0.0
numEventosEWb = 0.0
# Armazena a área no gráfico para o cálculo de E[N] e E[W]
somaAreasEN = 0.0
somaAreasEWa = 0.0
somaAreasEWb = 0.0
# Armazena o tempo anterior para o cálculo de E[N] e E[W]
tempoAnteriorEN = 0.0
tempoAnteriorEWa = 0.0
tempoAnteriorEWb = 0.0

# Lógica da simulação
while (tempo <= tempo_simulacao):
    # Não existe cliente sendo atendido no momento atual,
    # de modo que a simulação pode avançar no tempo para
    # a chegada do próximo cliente
    if (saida_atendimento == 0.0):
        tempo = chegada_cliente
    else:
        tempo = min(chegada_cliente, saida_atendimento)
            
    
    if (tempo == chegada_cliente):
        print("Chegada de cliente: " + str(chegada_cliente))

        # Evento de chegada de cliente
        fila += 1.0
        print("Fila: " + str(fila))

        # Indica que o caixa está ocioso
        # logo, pode-se começar a atender
        # o cliente que acaba de chegar
        if (saida_atendimento == 0.0):
            saida_atendimento = tempo
        
        # Gerar o tempo de chegada do próximo cliente
        chegada_cliente = tempo + float((-1.0/tempo_medio_clientes) * math.log(aleatorio()))

        # Cálculo de E[N]
        somaAreasEN += numEventosEN * (tempo - tempoAnteriorEN)
        tempoAnteriorEN = tempo
        numEventosEN += 1.0

        # Cálculo de E[W]
        somaAreasEWa += numEventosEWa * (tempo - tempoAnteriorEWa)
        tempoAnteriorEWa = tempo
        numEventosEWa += 1.0
    else:
        # Evento executado se houver saída de cliente
        # ou ainda se houver chegada de cliente, mas
        # o caixa estiver ocioso.
        # 
        # A cabeça da fila não consiste no cliente em atendimento.
        # O cliente que começa a ser atendido portanto, sai da fila,
        # e passa a estar ainda no comércio, mas em atendimento no caixa.

        # Verifico se há cliente na fila
        if (fila > 0.0):
            # Evento de saída de cliente
            fila -= 1.0
            print("Fila: " + str(fila))

            saida_atendimento = tempo + float((-1.0/tempo_medio_atendimento) * math.log(aleatorio()))
            print("Saida de cliente: " + str(saida_atendimento))

            utilizacao_cliente = saida_atendimento - tempo
            util += utilizacao_cliente
            print("Utilização do cliente: " + str(utilizacao_cliente))
            print("Utilização Total: " + str(util))
        else:
            saida_atendimento = 0.0

        # Se saiu alguém de fato (não quando chega alguém com o caixa ocioso)
        if (tempoAnteriorEN < tempo):
            # Cálculo de E[N]
            somaAreasEN += numEventosEN * (tempo - tempoAnteriorEN)
            tempoAnteriorEN = tempo
            numEventosEN -= 1.0

            # Cálculo de E[W]
            somaAreasEWb += numEventosEWb * (tempo - tempoAnteriorEWb)
            tempoAnteriorEWb = tempo
            numEventosEWb += 1.0
    print("=====================\n")

# Cálculo da Utilização
if (saida_atendimento > tempo):
    util -= (saida_atendimento - tempo)

util = util / tempo
print("Utilização: " + str(util) + "  ~  " + str("{:.2f}".format(util*100)) + "%")

# Tamanho médio de (fila + atendimento).
en = somaAreasEN / tempo
print("E[N]: " + str(en))

# Tempo médio que cada cliente ficou dentro da loja (fila + atendimento)
somaAreasEWa += numEventosEWa * (tempo - tempoAnteriorEWa)
somaAreasEWb += numEventosEWb * (tempo - tempoAnteriorEWb)
ew = (somaAreasEWa - somaAreasEWb) / numEventosEWa
print("E[W]: " + str(ew))

# Taxa de chegada
lamb = numEventosEWa / tempo
print("Lambda: " + str(lamb))

# Validação de Little
little = en - lamb * ew
print("Validação de Little: " + str(little))

print("")

# E[W] ainda está bugado