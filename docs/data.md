# Dados, alvo e métricas

## Fonte

O projeto conserva o [CSV utilizado no notebook original](https://raw.githubusercontent.com/JackyP/testing/master/datasets/nycflights.csv).
Download explícito: `flightlab download`. O arquivo fica em `data/raw/nycflights.csv`.
`flightlab quality` mostra contagens, exclusões e SHA-256 do conteúdo baixado.
A URL pode mudar de conteúdo; o hash permite distinguir execuções.

## Campos usados

| Campo | Significado | Papel |
| --- | --- | --- |
| `year`, `month`, `day` | Data de operação | Construção de data; mês também é feature |
| `carrier` | Código da companhia | Feature e agrupamento |
| `origin`, `dest` | Aeroportos de origem e destino | Features e construção da rota |
| `distance` | Distância em milhas | Feature numérica |
| `arr_delay` | Desvio da chegada em minutos; negativo significa antecipação | Construção do alvo e análise descritiva |
| `date` | Data construída no pipeline | Ordenação e separação temporal |
| `day_of_week` | Segunda=0 até domingo=6 | Feature derivada |
| `delayed` | 1 quando `arr_delay >= 15`; 0 nos demais casos válidos | Alvo da classificação |
| `route` | Origem e destino combinados | Agrupamento da análise |

Outras colunas do CSV original podem ser carregadas, mas não entram nas features
do modelo. A lista explícita está em `src/flightlab/config.py`.

## Tratamento

O pipeline exige as colunas do contrato, converte campos numéricos e constrói datas.
Remove registros com valores ausentes nas features, data ou alvo e distâncias não positivas.
Não preenche um atraso desconhecido com zero: isso inventaria um rótulo de pontualidade.

No primeiro experimento: 336.776 linhas originais, 327.346 utilizáveis e 9.430 exclusões.
As exclusões coincidem com a ausência de `arr_delay` na fonte utilizada. Isso não
permite afirmar que todas as linhas excluídas sejam cancelamentos.

## Indicadores de negócio

- **Voos:** quantidade de registros válidos no recorte.
- **Taxa de atraso:** número de registros com `delayed=1` dividido pelo total válido.
- **Desvio médio de chegada:** média de `arr_delay`, incluindo antecipações.
- **Ranking:** agrupamento com taxa, contagem e desvio médio; grupos abaixo do mínimo
  são excluídos. Amostra mínima não elimina viés ou demonstra causalidade.

## Métricas do modelo

| Métrica | Como interpretar |
| --- | --- |
| ROC AUC | Capacidade de ordenar positivos acima de negativos; 0,5 é referência sem discriminação |
| Average precision (AP) | Resumo da relação precisão/recall; a prevalência do teste é uma referência útil |
| Brier | Erro quadrático das probabilidades; menor é melhor |
| Precisão | Entre os voos classificados como atraso, quantos realmente atrasaram |
| Recall | Entre os atrasos reais, quantos o modelo classificou como atraso |

Precisão e recall usam limiar 0,5. Sem previsões positivas, precisão é registrada como
zero. Veja o [model card](model-card.md) para os resultados e suas implicações.
