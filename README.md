# EP2-IA-Algoritmos-Geneticos

## Requisitos

Para rodar este código, você precisará dos seguintes requisitos:

- **Python**: Instale a versão 3.7 ou superior do Python.
- **Bibliotecas**: O código depende das bibliotecas `numpy` e `matplotlib`. Você pode instalá-las usando o `pip`.

## Como Rodar

1. **Instale o Python**: Se você ainda não tem o Python instalado, faça o download [aqui](https://www.python.org/downloads/) e siga as instruções de instalação.

2. **Instale as bibliotecas necessárias**:

    Abra o terminal ou prompt de comando e execute os seguintes comandos:

    ```bash
    pip install numpy
    pip install matplotlib
    ```

3. **Baixe o código**: Clone ou faça o download deste repositório em seu computador.

4. **Execute o código**:

    Navegue até o diretório onde o código está localizado e execute o script Python:

    ```bash
    python nome_do_arquivo.py
    ```

5. **Verifique os resultados**: O cronograma de uso dos equipamentos será gerado com base nas restrições fornecidas.

# Cronograma de Uso de Equipamentos de Laboratório

Este projeto tem como objetivo criar um cronograma eficiente para a utilização dos equipamentos de um laboratório de química, garantindo que todas as análises sejam realizadas dentro do prazo, respeitando as restrições de capacidade e segurança dos equipamentos.

## Enunciado do Problema

Suponha que um laboratório de química precisa organizar o uso de seus equipamentos para garantir que todas as análises necessárias possam ser realizadas dentro do prazo esperado e que as restrições de segurança e capacidade dos equipamentos sejam cumpridas. O laboratório possui um conjunto de equipamentos, como balanças, espectrômetros e microscópios, que são usados para realizar diferentes tipos de análises químicas.

Existem várias análises que precisam ser realizadas, cada uma com seus próprios requisitos de equipamentos e tempo de execução. Alguns equipamentos só podem ser usados para uma análise específica, enquanto outros podem ser compartilhados entre diferentes análises.

As restrições a serem satisfeitas incluem:

1. Cada equipamento tem uma capacidade máxima de uso diário e só pode ser usado para uma análise por vez.
2. Uma análise não pode estar em 2 equipamentos ao mesmo tempo.
3. Cada análise fica 1 hora em cada equipamento.

O objetivo é encontrar um cronograma de uso de equipamentos que atenda a todas as restrições e minimize o tempo total necessário para concluir todas as análises.

### Tabela de Análises

| **Análise** | **Equipamentos Necessários** |
| --- | --- |
| Análise 1 | Espectrofotômetro UV-VIS, Cromatógrafo Gasoso |
| Análise 2 | Cromatógrafo Líquido, Espectrômetro Infravermelho |
| Análise 3 | Microscópio, Balança Analítica |
| Análise 4 | Espectrômetro de Massa |
| Análise 5 | Agitador Magnético, Espectrômetro Infravermelho |
| Análise 6 | Cromatógrafo Líquido, Espectrofotômetro UV-VIS |
| Análise 7 | Espectrofotômetro UV-VIS, Microscópio |
| Análise 8 | Cromatógrafo Gasoso |
| Análise 9 | Espectrômetro Infravermelho, Balança Analítica |
| Análise 10 | Espectrômetro de Massa, Cromatógrafo Gasoso |

### Tabela de Restrições

| **Equipamento** | **Tempo Máximo de Uso por Dia** |
| --- | --- |
| Balança Analítica | 6 horas |
| Agitador Magnético | 4 horas |
| Cromatógrafo Líquido | 8 horas |
| Cromatógrafo Gasoso | 6 horas |
| Espectrofotômetro UV-VIS | 4 horas |
| Espectrômetro Infravermelho | 6 horas |
| Espectrômetro de Massa | 4 horas |
| Microscópio | 6 horas |

O objetivo é gerar um plano de uso de cada equipamento durante a semana, garantindo que todas as análises sejam concluídas.
