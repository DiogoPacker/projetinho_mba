# Documentação do FlightLab

O [README principal](../README.md) apresenta o produto. Aqui estão os detalhes para
usar a demonstração, entender o experimento e continuar o desenvolvimento.

| Quero… | Leia |
| --- | --- |
| Experimentar os filtros, gráficos e simulador | [Dashboard interativo](dashboard.md) |
| Publicar uma demonstração no Render | [Deploy e operação](deployment-render.md) |
| Entender a passagem do notebook para o produto | [Evolução do projeto](development.md) |
| Entender módulos e decisões técnicas | [Arquitetura](architecture.md) |
| Conferir as métricas e limitações da previsão | [Model card](model-card.md) |
| Conhecer campos, alvo e tratamento dos dados | [Dados e métricas](data.md) |
| Consumir a API de outro programa | [Contrato da API](api.md) |
| Apresentar o projeto em uma entrevista | [Roteiro de demonstração](portfolio.md) |

## Caminho sugerido para avaliar o projeto

1. Entenda o problema e as entregas das quatro áreas no README.
2. Explore indicadores com filtros; observe a diferença entre taxa e contagem.
3. Veja a separação temporal e compare o modelo com seu baseline.
4. Simule um voo e confira as limitações antes de interpretar a probabilidade.
5. Inspecione o contexto enviado ao assistente e o contrato da API.
6. Consulte testes, CI e configuração de deploy para avaliar a engenharia.

## Estado da entrega

Dashboard, pipeline, treinamento, API e assistente estão implementados. O primeiro
treino foi executado com a base real; os números estão no relatório versionável.
A integração LLM é testada com provedor simulado. O uso real depende de credencial.
A demonstração foi publicada pelo responsável pelo projeto no Render:
https://flightlab-dashboard.onrender.com. A execução remota do CI pode ser consultada
no badge e na aba Actions do GitHub.
