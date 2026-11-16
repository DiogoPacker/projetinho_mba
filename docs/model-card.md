# Primeiro experimento — regressão logística

Treino executado em 16/11/2026 sobre o CSV histórico usado no projeto original.
O relatório completo, incluindo hash da base, está em [metrics.json](../artifacts/metrics.json).

## Dados e períodos

336.776 registros originais; 327.346 utilizáveis; 9.430 excluídos por ausência de atraso
de chegada. Alvo positivo: atraso na chegada >=15 minutos.

| Partição | Datas de 2013 | Voos |
| --- | --- | ---: |
| Treino | 01/01 a 25/08 | 212.287 |
| Validação | 26/08 a 26/10 | 56.341 |
| Teste | 27/10 a 31/12 | 58.718 |

## Resultado em teste

| Métrica | Regressão logística | Baseline constante |
| --- | ---: | ---: |
| ROC AUC ↑ | 0,5768 | 0,5000 |
| Precisão média (AP) ↑ | 0,3074 | 0,2504 |
| Brier ↓ | 0,1943 | 0,1880 |
| Precisão com limiar 0,5 | 0,3918 | 0,0000 |
| Recall com limiar 0,5 | 0,0421 | 0,0000 |

O modelo ordena os riscos um pouco melhor que o baseline, mas suas probabilidades têm
erro quadrático maior. Com o limiar fixo de 0,5, identifica somente cerca de 4,2% dos
atrasos reais. O baseline sempre estima a prevalência do treino e nunca cruza 0,5.
Precisão zero nesse caso é a convenção adotada para ausência de previsões positivas.

Em validação, o modelo também perde no Brier (0,1602 contra 0,1452). A proporção de
atrasos muda entre os períodos: 15,9% na validação e 25,0% no teste. Isso reforça a
necessidade de lidar com sazonalidade e mudança de distribuição.

## Interpretação

Este experimento serve como primeiro modelo auditável de portfólio. Não sustenta
uma recomendação operacional. Uma previsão produzida pela interface não significa
que o modelo foi aprovado para uso real.

As features disponíveis não incluem horário programado, clima, congestionamento ou
efeitos de voos anteriores. Mês e dia da semana entram como valores numéricos, uma
simplificação que não representa toda a estrutura cíclica do calendário.

## Próximo experimento

Adicionar dados pré-voo mais informativos, representar calendário de forma cíclica,
comparar modelos não lineares em janelas temporais e verificar calibração. Definir
limiar pela relação entre custos de falsos positivos e falsos negativos na validação.
Como o teste deste experimento já foi consultado, novos ajustes precisam de um novo
holdout temporal para uma avaliação final independente.
