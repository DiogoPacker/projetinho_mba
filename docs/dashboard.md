# Dashboard interativo

O ponto de entrada é [apps/dashboard.py](../apps/dashboard.py). Streamlit organiza a
interface; Plotly fornece os gráficos interativos. Não é necessário iniciar a API
para usar o dashboard.

## Análise de dados

Na barra lateral, selecione companhias, origens e intervalo de meses. Seleções vazias
de companhia/origem significam todas as opções. O mínimo de voos por grupo exclui
grupos pequenos dos rankings; ele não remove voos do cálculo dos indicadores gerais.

Os indicadores mostram quantidade de voos, taxa de atraso >=15 minutos e desvio médio
na chegada. Esse último inclui valores negativos de voos que chegaram antecipados.

Os gráficos comparam companhias e meses. Passe o mouse para detalhes, arraste para
selecionar uma região e use os controles Plotly para zoom e restauração da visualização.
O gráfico mensal é uma descrição de 2013, sem previsão de meses futuros.

A tabela lista as vinte rotas com maior taxa entre os grupos elegíveis. O botão de
exportação baixa os indicadores por companhia do recorte atual, em CSV.
Quando nenhum voo corresponde aos filtros, a interface informa que o recorte está vazio.

## Previsão de atraso

Informe data, companhia, origem, destino e distância **em milhas**. Clique em
**Estimar probabilidade** para processar o formulário. Os valores são enviados juntos
ao clicar; mudar um campo não retreina o modelo.

O retorno é a probabilidade estimada de atraso >=15 minutos. Não é uma previsão do
número de minutos nem uma garantia de que o voo atrasará. Os seletores permitem
combinações não observadas; a interface avisa quando a companhia/rota não aparece na base.

O formulário não deriva a distância automaticamente: informe um valor coerente com a rota.
Os filtros laterais não alteram o modelo nem o formulário. A avaliação compara regressão
logística e baseline em um período posterior ao treino. O aviso de Brier informa que
o modelo inicial tem erro de probabilidade maior que o baseline.

## Assistente

O resumo local mostra estatísticas calculadas a partir dos filtros. É determinístico:
a pergunta serve como entrada da interface, mas não é interpretada nesse modo.

Com LLM habilitado e uma chave válida, a pergunta e os agregados são enviados ao
provedor. Abra **Contexto usado na resposta** para conferir o JSON disponível ao LLM.
O contexto inclui companhias e as dez rotas de maior taxa com pelo menos 100 voos,
além dos meses. O mínimo configurado no ranking lateral não altera esse limite fixo
do assistente. Perguntas sobre outras rotas, clima ou causas podem ficar sem resposta.

Na demonstração Render padrão, o seletor LLM fica desabilitado. Isso é independente
do resumo local, que continua disponível. Não há histórico de conversa persistente.

## Projeto

Explica o que foi desenvolvido em cada área profissional e mostra quantidade de
linhas originais, linhas válidas, exclusões e hash da fonte.

## Roteiro rápido

1. Compare companhias por taxa, observando também o número de voos.
2. Selecione uma origem e os meses de verão de 2013; observe o novo recorte.
3. Exporte os indicadores e confira a tabela de rotas.
4. Simule um voo e abra as métricas do modelo.
5. Solicite um resumo e confira o contexto fornecido ao assistente.
