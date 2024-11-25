# Projeto final de Sistemas Operacionais I - UNESP 2024
**Alunos**: Felipe Silva Alves de Oliveira, Gabriella Alves de Oliveira, João Pedro Bastasini Garcia de Souza.<br>
**Docente**: Prof. Dr. Caetano Mazzoni Ranieri
## Sobre o projeto
O projeto propõe a criação de um algoritmo de uma aplicação concorrente que simule o comportamento de uma rede de entregas, em que encomendas são transportadas por veículos de um ponto de redistribuição até outro.
## Funcionamento
A principio inicializamos as threads, os pontos de distribuição, os veículos e as encomendas.<br>
Os pontos de distribuição aguardam as encomendas estarem inicializadas, para começar o carregamento dos veículos.<br>
A partir do momento em que os veículos são carregados com as primeiras encomendas, eles começam a se locomover entre os pontos de distribuição.<br>
Quando um veículo chega a um ponto de distribuição, nenhum outro veículo pode carregar/descarregar no ponto até que o esse seja descarregado.<br>
Ao longo do projeto, utilizamos artifícios importantes estudados na disciplina de Sistemas Operacionais I como o barramento, para a inicialização de tarefas, e o mutex como semáforo, para restringir certas ações a fim de impedir a sobreposição de dados.<br>
