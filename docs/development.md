# Evolução do projeto

Este documento explica as etapas técnicas. Ele complementa o histórico Git: não
representa commits que ainda não foram criados ou enviados ao GitHub.

## 1. Ponto de partida: estudo acadêmico

A pasta `nyflights-model/` contém um notebook com análise exploratória de atrasos,
gráficos por companhia, rota e aeronave, além de uma apresentação. O projeto dependia
da execução das células e não tinha modelo preditivo, API ou interface de produto.

`decode_morse_project/` é um exercício Python independente que traduz Morse e grava
mensagens em CSV. Foi preservado como material original; não faz parte do domínio de voos.

## 2. Produto de análise

A lógica saiu das células para módulos Python reutilizáveis. O pipeline passou a
validar colunas, converter tipos, registrar exclusões e identificar a versão da base
por hash. Taxas e contagens aparecem juntas, com mínimo de voos nos rankings.

A definição de atraso mudou: o notebook contava qualquer valor positivo; o produto
considera chegada >=15 minutos atrasada. Isso foi documentado para evitar comparações
incompatíveis entre os dois trabalhos.

## 3. Experimento de ciência de dados

Foi implementada uma regressão logística com features anteriores à partida. O treino
não recebe atraso na partida, horário real de chegada ou tempo real de voo. O pipeline
aprende o preprocessamento somente no treino e separa datas inteiras entre partições.

O baseline constante dá um referencial de comparação. O primeiro resultado mostra
alguma discriminação, mas desempenho pior em Brier e recall baixo. O relatório registra
o resultado completo, sem tratar um experimento inicial como modelo aprovado.

## 4. Engenharia de IA

O LLM recebe estatísticas que o Python já calculou. Ele atua como camada de explicação,
sem gerar código executável ou consultar bancos livremente. Há resumo local sem chave,
limites de tamanho, timeout, tratamento de erro e testes com cliente simulado.

Não foi treinado um LLM nem implementado um mecanismo de busca vetorial. A solução
usa contexto agregado para uma tarefa delimitada, mantendo visível a origem dos números.

## 5. Engenharia de software e publicação

O pacote instalável compartilha serviços entre Streamlit, FastAPI e CLI. Testes cobrem
alvo, separação temporal, artefatos, categorias novas, contratos HTTP e interação com a UI.
Há lint, formatação, CI, Docker e configuração declarativa do Render.

O caminho dos dados é independente da instalação do pacote. O build do Render gera
os artefatos antes de iniciar a aplicação, e a demonstração pública bloqueia o LLM pago.
Publicação remota e integração com contas continuam sendo etapas operacionais.

## Próximas entregas propostas

- [x] Publicar a demo no Render e registrar sua URL no README: https://flightlab-dashboard.onrender.com.
- [ ] Adicionar o link público ao campo Website da seção About do GitHub.
- [ ] Registrar capturas reais ou um vídeo curto da demonstração.
- [ ] Adicionar features de horário programado e calendário cíclico.
- [ ] Comparar modelos não lineares com validação em múltiplas janelas temporais.
- [ ] Avaliar calibração e escolher limiar com base em custo de negócio.
- [ ] Definir novo holdout independente para o próximo experimento.
- [ ] Versionar datasets e modelos fora do filesystem efêmero.
- [ ] Adicionar controle de acesso, quotas e monitoramento antes de liberar LLM público.

## Como evidenciar isso no GitHub

Use o README como entrada e os documentos como aprofundamento. Mantenha commits
futuros pequenos, com descrição do problema, decisão e validação. Quando existirem
execuções remotas de CI e uma demo publicada, vincule os resultados reais.

Na seção About, uma descrição possível é:

> Pipeline de dados de voos com dashboard interativo, ML avaliado temporalmente,
> API FastAPI e assistente LLM. Python, análise de dados e engenharia de IA.

Topics sugeridos: `python`, `data-analysis`, `data-science`, `machine-learning`,
`streamlit`, `fastapi`, `llm`, `portfolio`, `render`.
