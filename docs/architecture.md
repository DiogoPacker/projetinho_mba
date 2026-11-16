# Decisões de arquitetura

## Monólito modular

Um pacote Python central concentra regras; Streamlit e FastAPI são adaptadores.
Para este volume e objetivo de portfólio, microserviços, filas e um banco vetorial
adicionariam operação sem benefício demonstrado. CSV local e joblib bastam para
um primeiro produto reproduzível. Dados e artefatos ficam no diretório de execução,
ou no caminho configurado em `FLIGHTLAB_HOME`. Eles não dependem de onde o pacote
foi instalado. No Docker, o diretório de execução é `/app`.

## Contrato de previsão

O usuário informa data, companhia, origem, destino e distância em milhas. Data gera mês
e dia da semana da mesma forma no treino e na inferência. A resposta é uma probabilidade
de chegada >=15 minutos atrasada, não uma quantidade de minutos. O limiar 0,5 é fixo e
não representa um custo operacional otimizado. A pouca informação pré-voo limita o modelo.

## Separação temporal

Separar aleatoriamente voos do mesmo ano pode mascarar mudança de distribuição.
O pipeline separa datas inteiras em ordem. O preprocessamento aprende no treino;
validação e teste são transformados sem reestimar categorias ou médias. O artefato
publicado é o mesmo avaliado em teste, sem retreino sobre o conjunto completo.

## Assistente com contexto

O assistente injeta agregados calculados no prompt. Não é RAG vetorial, não gera SQL
e não tem ferramentas que executam código. A pergunta não modifica o pipeline.
Chaves do JSON permitem conferir a resposta. Perguntas fora das tabelas agregadas
exigem ampliar o contexto no código. As instruções não eliminam alucinações.

## Operação e evolução

Download e treino são comandos explícitos. Abrir o dashboard não treina modelo nem
gera cobranças. Chave fica no ambiente do servidor; o navegador não recebe o segredo.
Reiniciar processos após atualização limpa caches de dados e modelo.

No Render, `scripts/render-build.sh` faz download e treino durante cada build.
Os arquivos resultantes são usados pelo processo web. O serviço padrão publica
somente o dashboard: ele chama os serviços Python diretamente, sem depender da API.
O LLM fica desativado por `FLIGHTLAB_ENABLE_LLM=false`; resumo local e previsão
continuam disponíveis. Consulte o [guia de deploy](deployment-render.md).

O próximo ciclo deve priorizar dados recentes e horários programados, validação temporal
em múltiplas janelas, modelo não linear comparado ao baseline, calibração e limiar definido
por custo de negócio. Depois: contratos de dados mais estritos, monitoramento de drift,
registry de modelos, autenticação e limites por usuário para chamadas LLM.
