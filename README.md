# Projeto final de Sistemas Operacionais I - UNESP 2024
**Alunos**: Felipe Silva Alves de Oliveira, Gabriella Alves de Oliveira, João Pedro Bastasini Garcia de Souza.<br>
**Docente**: Prof. Dr. Caetano Mazzoni Ranieri

## Sobre o projeto 💻

O projeto propõe a criação de um algoritmo de uma aplicação concorrente que simule o comportamento de uma rede de entregas, em que encomendas são transportadas por veículos de um ponto de redistribuição até outro. Ao longo do projeto, utilizamos artifícios importantes estudados na disciplina de Sistemas Operacionais I como o barramento, para a inicialização de tarefas, e o mutex como semáforo, para restringir certas ações a fim de impedir a sobreposição de dados.

## Fluxo Básico 🚚

A principio inicializamos as threads, os pontos de distribuição, os veículos e as encomendas.<br>
Os pontos de distribuição aguardam as encomendas estarem inicializadas, para começar o carregamento dos veículos.<br>
A partir do momento em que os veículos são carregados com as primeiras encomendas, eles começam a se locomover entre os pontos de distribuição.<br>
Quando um veículo chega a um ponto de distribuição, nenhum outro veículo pode carregar/descarregar no ponto até que o esse seja descarregado.

## Descrição do Código 📦

O código em Python simula uma rede de pontos de distribuição interconectados, com encomendas que precisam ser transportadas de um ponto de redistribuição a outro por uma frota de veículos. A sincronização entre os pontos de redistribuição e os veículos é feita por meio de semáforos e mutexes, garantindo que apenas um veículo por vez seja atendido em cada ponto.

### Estrutura

- **Pontos de Distribuição:** Representados por uma lista de dicionários que armazena o status e a fila de encomendas em cada ponto.
- **Veículos:** Representados por uma lista de dicionários que indicam o ponto atual em que o veículo está e as encomendas transportadas.
- **Encomendas:** Representadas por uma lista de dicionários contendo as informações de ponto inicial, ponto final e status da entrega.
- **Threading e Sincronização:** Cada veículo, encomenda e ponto de distribuição é gerenciado por uma thread, que são iniciadas simultaneamente, simulando o ambiente concorrente.

Os veículos se deslocam entre os pontos de redistribuição em uma ordem sequencial (fila circular), carregando encomendas disponíveis e descarregando-as nos destinos finais. A movimentação dos veículos e a organização das encomendas são feitas de maneira assíncrona, com tempos de viagem aleatórios para cada veículo.

Os principais métodos incluem:
- **iniciar_pontos_distribuicao:** Inicializa os pontos de distribuição, organizando as encomendas que chegam.
- **circular_veiculo:** Controla o movimento dos veículos entre os pontos e as operações de carga e descarga.
- **iniciar_encomenda:** Define os pontos de origem e destino de cada encomenda e gerencia seu status.
- **carregar_encomenda** e **descarregar_encomenda:** Gerenciam as operações de carga e descarga das encomendas em cada veículo.

### Saídas

A aplicação gera dois tipos de saída:
1. **Monitoramento em Tempo Real:** Mensagens são exibidas no console para indicar o progresso dos veículos e encomendas.
2. **Arquivos de Acompanhamento:** Cada encomenda gera um arquivo de rastro que registra o número da encomenda, seus pontos de origem e destino, e os horários de carregamento e descarregamento.

## Como Executar o Código

1. **Requisitos:**
   - Python 3.x

2. **Execução do Programa:**
   - Clone o repositório do projeto.
   - Execute o código principal com Python:
     ```bash
     python main.py
     ```
   - Ao iniciar a aplicação, você será solicitado a fornecer os seguintes parâmetros de entrada:
     - Quantidade de pontos de distribuição (S)
     - Quantidade de veículos (C)
     - Quantidade de encomendas (P)
     - Espaço de carga em cada veículo (A)

3. **Monitoramento e Arquivos de Saída:**
   - A aplicação irá exibir no console o progresso das entregas, incluindo quando encomendas são carregadas e descarregadas.
   - Arquivos de acompanhamento serão gerados para cada encomenda na pasta do projeto, registrando o histórico completo da entrega.

## Observações
- O programa foi projetado para simular um ambiente concorrente, com sincronização apropriada usando mutexes e semáforos.
- Certifique-se de fornecer valores apropriados para S, C, P e A, de modo a observar claramente a concorrência e a sincronização entre as threads.

