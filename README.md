# Minimizador Lógico - Algoritmo de Quine-McCluskey

Este projeto foi desenvolvido como parte do **Lab 06 de Práticas em Sistemas Digitais** do Departamento de Computação (DCOMP) da Universidade Federal de Sergipe (UFS). Trata-se de uma ferramenta EDA funcional escrita em Python para a minimização exata de funções booleanas utilizando o clássico algoritmo de Quine-McCluskey.

## Funcionalidades

* **Parser de Arquivos PLA:** Suporte nativo à leitura de funções booleanas no formato tabular `.pla` do Espresso.
* **Expansão de Don't Cares:** Resolução recursiva de termos irrelevantes (`-`) nas strings de entrada do formato PLA.
* **Geração de Implicantes Primos:** Agrupamento sistemático por distância de Hamming.
* **Tabela de Cobertura:** Resolução automatizada com identificação de implicantes essenciais e algoritmo guloso (*greedy*) para os termos restantes.
* **Métrica de Desempenho:** Cronometragem interna integrada para análise de tempo de execução (Benchmarking).

## Estrutura do Código

O algoritmo principal está estruturado nas seguintes funções:
* `parse_pla()`: Realiza o *parsing* do cabeçalho (`.i`, `.o`) e corpo do arquivo.
* `expand_dont_cares()`: Expande recursivamente entradas com `-[dont-care]` em mintermos inteiros.
* `combine_terms()`: Avalia a adjacência lógica entre termos.
* `find_prime_implicants()`: Agrupa os mintermos em busca de todas as quadras/oitavas (Implicantes Primos).
* `select_minimum_implicants()`: Resolve a tabela de cobertura eliminando termos redundantes.
* `format_expression()`: Converte a saída binária em uma string booleana convencional (ex: `A'B + CD`).

## Pré-requisitos

Você só precisa do Python 3.x instalado em sua máquina. Nenhuma biblioteca externa é necessária.


Como Executar
Coloque os seus arquivos .pla na pasta do projeto.  
Altere o caminho do arquivo alvo na variável arquivo_benchmark dentro do script.Execute o programa:
```bash
python fase1.py
```
