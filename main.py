import threading as th
import time
from datetime import datetime
import random

print(f"Seja bem-vindo ao sistema de entrega!")
print(f"Para iniciarmos, nos informe:")

S = int(input("Quantidade de pontos de distribuição: "))
C = int(input("Quantidade de veículos: "))
P = int(input("Quantidade de encomendas a serem entregues: "))
A = int(input("Espaço de carga em cada veículo: "))

print(f"\n")

threads = [] # Thread principal
max_ponto_entrega = S-1

# Inicializando arrays necessárias
pontos_distribuicao = [{"status": None, "encomendas": []} for _ in range(S)]
veiculos = [{"ponto_atual": None, "encomendas": []} for _ in range(C)]
encomendas = [{"id": None,"ponto_atual": None, "ponto_final": None, "status": 0, "acompanhamento": []} for _ in range(P)]

# Inicializando Mutex
mutex_pontos_distribuicao = th.Lock()
mutex_encomendas = th.Lock()
mutex_carregamento_encomenda = [th.Lock() for _ in range(S)]

# Inicializando variáveis de barramento
barramento_pontos_distribuicao = th.Event()
barramento_encomendas = th.Event()

# Inicializando contador para poder liberar as threads
pontos_distribuicao_faltantes = S
encomendas_faltantes = P

def salvar_rastro(encomenda):
    with open(f"encomenda_{encomenda['id']}_acompanhamento.txt", "w") as file:
        file.write("\n".join(encomenda["acompanhamento"]))

def descarregar_encomenda(ponto_distribuicao_atual, pos_veiculo):
    aux = veiculos[pos_veiculo]["encomendas"]
    for pos_encomenda, encomenda_atual in enumerate(aux):
        if encomendas[encomenda_atual]["ponto_final"] == ponto_distribuicao_atual: # Será descarregado apenas encomendas que possuem o ponto final igual ao ponto atual
            acompanhamento = f"Encomenda {encomenda_atual + 1} descarregada no ponto {ponto_distribuicao_atual + 1} às {datetime.now().time()}"
            print(acompanhamento)
            veiculos[pos_veiculo]["encomendas"].pop(pos_encomenda)
            encomendas[encomenda_atual]["acompanhamento"].append(acompanhamento)
            salvar_rastro(encomendas[encomenda_atual])
            encomendas[encomenda_atual]["status"] = 2 # Sinalizando que a encomenda foi entregue

def carregar_encomenda(ponto_distribuicao_atual, pos_veiculo):
    aux = pontos_distribuicao[ponto_distribuicao_atual]["encomendas"]
    for pos_encomenda, encomenda_atual in enumerate(aux):
        carga_atual = len(veiculos[pos_veiculo]["encomendas"])
        if carga_atual >= A:
            break

        if encomendas[encomenda_atual]["status"] == 0: # Será carregado apenas encomendas que não chegaram ao seu destino final e que não estão em transporte
            acompanhamento = f"Encomenda {encomenda_atual + 1} carregada no veículo {pos_veiculo + 1} no ponto {ponto_distribuicao_atual + 1} às {datetime.now().time()}"
            print(acompanhamento)
            veiculos[pos_veiculo]["encomendas"].append(encomenda_atual)
            pontos_distribuicao[ponto_distribuicao_atual]["encomendas"].pop(pos_encomenda)
            encomendas[encomenda_atual]["acompanhamento"].append(acompanhamento)
            encomendas[encomenda_atual]["status"] = 1 # Sinalizando que a encomenda está em transporte

def organizar_encomenda(pos_distribuicao):
    for pos_encomenda, encomenda_atual in enumerate(encomendas):
        if pos_distribuicao == encomenda_atual["ponto_atual"] and encomenda_atual["status"] == 0:
            pontos_distribuicao[pos_distribuicao]["encomendas"].append(pos_encomenda)

def circular_veiculo(pos_veiculo):
    global S, A, encomendas, pontos_distribuicao, max_ponto_entrega

    # Inicializando carros
    if veiculos[pos_veiculo]["ponto_atual"] is None:
        veiculos[pos_veiculo]["ponto_atual"] = random.randint(0, max_ponto_entrega)

    # Somente irá começar a rodar após os pontos de distribuição estarem liberados para coleta
    barramento_pontos_distribuicao.wait()

    while any(e["status"] != 2 for e in encomendas):  # Continua enquanto houver encomendas a entregar
        print(f"O veículo {pos_veiculo + 1} chegou ao ponto inicial {veiculos[pos_veiculo]['ponto_atual'] + 1}")
        ponto_distribuicao_atual = veiculos[pos_veiculo]["ponto_atual"]
        with mutex_carregamento_encomenda[ponto_distribuicao_atual]:
            descarregar_encomenda(ponto_distribuicao_atual, pos_veiculo)
            carregar_encomenda(ponto_distribuicao_atual, pos_veiculo)

        # Simula o tempo de viagem
        time.sleep(random.uniform(1, 10))
        veiculos[pos_veiculo]["ponto_atual"] = (ponto_distribuicao_atual + 1) % S
        print(f"Veículo {pos_veiculo + 1} movendo-se para o ponto {veiculos[pos_veiculo]['ponto_atual'] + 1}")

def iniciar_encomenda(pos_encomenda):
    global S, encomendas_faltantes, max_ponto_entrega

    if encomendas[pos_encomenda]["ponto_atual"] is None:
        encomendas[pos_encomenda]["id"] = pos_encomenda
        encomendas[pos_encomenda]["ponto_atual"] = random.randint(0, max_ponto_entrega)
        # Garantindo que o ponto de entrega inicial não seja o mesmo do ponto de entrega final
        while True:
            encomendas[pos_encomenda]["ponto_final"] = random.randint(0, max_ponto_entrega)
            if encomendas[pos_encomenda]["ponto_final"] != encomendas[pos_encomenda]["ponto_atual"]:
                break

        acompanhamento = f"Encomenda {pos_encomenda + 1} criada no ponto {encomendas[pos_encomenda]['ponto_atual'] + 1} com destino ao ponto {encomendas[pos_encomenda]['ponto_final'] + 1} às {datetime.now().time()}"
        encomendas[pos_encomenda]["acompanhamento"].append(acompanhamento)
        print(acompanhamento)

        with mutex_encomendas:
            if encomendas_faltantes:
                encomendas_faltantes -= 1
                if not encomendas_faltantes:
                    barramento_encomendas.set()

def iniciar_pontos_distribuicao(pos_distribuicao):
    global pontos_distribuicao_faltantes

    if pontos_distribuicao[pos_distribuicao]["status"] is None:
        pontos_distribuicao[pos_distribuicao]["status"] = 0 # 0 = esperando veículo, 1 = carregando um veículo
        print(f"Ponto de distribuição {pos_distribuicao + 1} aberto!")

        barramento_encomendas.wait() # Somente irá começar quando todas as encomendas estiverem prontas
        print(f"Organizando encomendas por ordem de chegada")
        organizar_encomenda(pos_distribuicao)

        with mutex_pontos_distribuicao:
            if pontos_distribuicao_faltantes:
                pontos_distribuicao_faltantes -= 1
                if not pontos_distribuicao_faltantes:
                    barramento_pontos_distribuicao.set()

for i in range(C):
    veiculo = th.Thread(target=circular_veiculo, args=(i,))
    threads.append(veiculo)
    veiculo.start()

for i in range(P):
    encomenda = th.Thread(target=iniciar_encomenda, args=(i,))
    threads.append(encomenda)
    encomenda.start()

for i in range(S):
    ponto_distribuicao = th.Thread(target=iniciar_pontos_distribuicao, args=(i,))
    threads.append(ponto_distribuicao)
    ponto_distribuicao.start()

for thread in threads:
    thread.join()
