# Roteiro de demonstração — 5 a 10 minutos

1. **Problema:** companhias com mais atrasos absolutos podem apenas operar mais voos.
   Mostrar contagens e taxas lado a lado e explicar o limiar de 15 minutos.
2. **Dados:** mostrar o relatório de qualidade, exclusões e origem do CSV. Explicar
   por que voos sem chegada conhecida não podem receber o rótulo do modelo.
3. **Análise:** filtrar companhia e mês; inspecionar rotas com amostra mínima.
   Separar associação descritiva de causa operacional.
4. **Ciência de dados:** abrir as datas de treino/validação/teste, comparar modelo e
   baseline, discutir recall no limiar 0,5 e limitações dos preditores disponíveis.
5. **Produto:** simular um voo e explicar probabilidade versus minutos de atraso.
6. **IA generativa:** pedir um resumo do recorte, inspecionar o JSON de contexto e
   explicar por que o LLM não calcula a previsão nem pode consultar dados ausentes.
7. **Engenharia:** abrir `/docs`, executar uma previsão via API e mostrar os testes/CI.

Mensagem central: transformar uma pergunta de negócio em dados validados, indicadores,
um experimento preditivo avaliado honestamente e interfaces utilizáveis em Python.
