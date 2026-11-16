# API REST

Inicie a partir da raiz do repositório, depois de download e treino:

```bash
python -m uvicorn flightlab.api:app --host 127.0.0.1 --port 8000
```

Contrato interativo: http://localhost:8000/docs. Esquema OpenAPI: `/openapi.json`.
As respostas são JSON. Distâncias estão em milhas; probabilidades vão de 0 a 1.

| Método | Rota | Entrada |
| --- | --- | --- |
| GET | `/health` | Sem parâmetros |
| GET | `/analytics` | Query opcional: `carrier`, `month` de 1 a 12 |
| GET | `/model` | Sem parâmetros |
| POST | `/predict` | Corpo do voo |
| POST | `/assistant` | Pergunta, modo e companhia opcional |

## Previsão

```json
{
  "date": "2013-11-15",
  "carrier": "AA",
  "origin": "JFK",
  "dest": "LAX",
  "distance": 2475
}
```

Resposta observada com o artefato inicial; números podem mudar após outro treinamento:

```json
{
  "probability": 0.24809795394005263,
  "delayed": false,
  "threshold_minutes": 15,
  "unknown_categories": [],
  "warning": "Estimativa educacional baseada em 2013; não é previsão operacional atual."
}
```

`delayed` representa a decisão com limiar 0,5, e não o estado observado de um voo real.
Categorias não vistas no treino são aceitas pelo encoder e listadas em
`unknown_categories`. O backend não valida a existência da combinação de companhia/rota;
essa verificação adicional aparece na interface do dashboard.

## Assistente

```json
{
  "question": "Qual a taxa de atraso neste recorte?",
  "use_llm": false,
  "carrier": "AA"
}
```

O retorno tem `mode`, `answer` e `context`. `local_summary` é resumo fixo; `llm` é
resposta do provedor sobre os agregados fornecidos. A pergunta deve ter de 1 a 2000
caracteres, incluindo pelo menos um não branco.

Quando `FLIGHTLAB_ENABLE_LLM=false`, o pedido com `use_llm=true` retorna 422.
A flag não impede analytics, previsão ou resumo local.

## Erros e operação

| HTTP | Significado |
| --- | --- |
| 200 | Operação concluída; recorte vazio em analytics também é 200 |
| 422 | Corpo/query inválido, pergunta vazia ou configuração de LLM indisponível |
| 503 | Dados ou modelo ainda não preparados |
| 502 | Falha no provedor LLM; detalhes internos não são enviados ao cliente |

`/health` confirma que o processo responde, não que os artefatos estejam preparados.
A API mantém cache em memória: reinicie o processo depois de atualizar dados ou modelo.
Esta versão não inclui autenticação, rate limiting ou quota de chamadas.
