from datetime import date

import pandas as pd
import plotly.express as px
import streamlit as st
from openai import OpenAIError

from flightlab.analytics import ranking, summary
from flightlab.assistant import answer, llm_enabled
from flightlab.data import load
from flightlab.loading import LOADING_HTML
from flightlab.model import load_model, predict

st.set_page_config(page_title="FlightLab | Dados & IA", page_icon="✈️", layout="wide")


@st.cache_data(show_spinner=False)
def get_data():
    return load()


@st.cache_resource(show_spinner=False)
def get_model():
    return load_model()


st.title("✈️ FlightLab")
st.caption("Um laboratório de análise, ciência de dados e engenharia de IA com Python")
st.info("Dados históricos de 2013. Atraso = chegada com 15 minutos ou mais. Uso educacional.")
loading = st.empty()
if not st.session_state.get("flightlab_ready", False):
    loading.markdown(LOADING_HTML, unsafe_allow_html=True)
try:
    df, quality = get_data()
except (FileNotFoundError, ValueError) as error:
    loading.empty()
    st.error(str(error))
    st.stop()

with st.sidebar:
    st.header("Explorar a base")
    carriers = st.multiselect("Companhias", sorted(df.carrier.unique()))
    origins = st.multiselect("Origens", sorted(df.origin.unique()))
    months = st.slider("Meses", 1, 12, (1, 12))
    minimum = st.number_input("Mínimo de voos por grupo", 1, 10000, 100)
    st.caption("Os filtros afetam a análise e o assistente. O simulador usa o modelo completo.")

filtered = df.loc[df.month.between(*months)]
if carriers:
    filtered = filtered.loc[filtered.carrier.isin(carriers)]
if origins:
    filtered = filtered.loc[filtered.origin.isin(origins)]

eda, ml, chat, about = st.tabs(["Análise de dados", "Previsão de atraso", "Assistente", "Projeto"])
with eda:
    if filtered.empty:
        st.warning("Nenhum voo corresponde aos filtros.")
    else:
        stats = summary(filtered, int(minimum))
        a, b, c = st.columns(3)
        a.metric("Voos analisados", f"{stats['flights']:,}")
        b.metric("Taxa de atraso ≥15 min", f"{stats['delay_rate']:.1%}")
        c.metric("Desvio médio de chegada", f"{stats['mean_arrival_deviation_minutes']:.1f} min")
        st.caption(
            "O desvio médio inclui chegadas antecipadas. Grupos pequenos são excluídos dos rankings."
        )
        col1, col2 = st.columns(2)
        with col1:
            grouped = ranking(filtered, "carrier", int(minimum))
            st.plotly_chart(
                px.bar(
                    grouped,
                    x="carrier",
                    y="delay_rate",
                    hover_data=["flights"],
                    title="Taxa de atraso por companhia",
                ),
                width="stretch",
            )
        with col2:
            monthly = ranking(filtered, "month", 1).sort_values("month")
            st.plotly_chart(
                px.line(
                    monthly, x="month", y="delay_rate", markers=True, title="Taxa de atraso por mês"
                ),
                width="stretch",
            )
        st.subheader("Rotas com maior taxa de atraso")
        st.dataframe(ranking(filtered, "route", int(minimum)).head(20), hide_index=True)
        st.download_button(
            "Exportar indicadores por companhia",
            grouped.to_csv(index=False),
            "companhias.csv",
            "text/csv",
        )

with ml:
    st.subheader("Simule um voo antes da partida")
    try:
        bundle = get_model()
    except FileNotFoundError as error:
        st.warning(str(error))
    else:
        with st.form("prediction"):
            a, b, c = st.columns(3)
            flight_date = a.date_input("Data do cenário histórico", date(2013, 11, 15))
            carrier = b.selectbox("Companhia do voo", sorted(df.carrier.unique()))
            origin = c.selectbox("Origem do voo", sorted(df.origin.unique()))
            dest = a.selectbox("Destino", sorted(df.dest.unique()))
            distance = b.number_input("Distância (milhas)", 1.0, 15000.0, 1000.0)
            submitted = st.form_submit_button("Estimar probabilidade")
        if submitted:
            result = predict(
                bundle,
                {
                    "date": flight_date,
                    "carrier": carrier,
                    "origin": origin,
                    "dest": dest,
                    "distance": distance,
                },
            )
            st.metric("Probabilidade estimada de atraso ≥15 min", f"{result['probability']:.1%}")
            st.warning(result["warning"])
            if df.loc[(df.carrier == carrier) & (df.origin == origin) & (df.dest == dest)].empty:
                st.warning("Combinação de companhia e rota não observada na base histórica.")
            if result["unknown_categories"]:
                st.warning(f"Categorias ausentes no treino: {result['unknown_categories']}")
        st.subheader("Avaliação fora do período de treino")
        metrics = bundle["metrics"]
        if metrics["test"]["brier"] >= metrics["baseline_test"]["brier"]:
            st.warning(
                "Neste teste, o modelo teve erro de probabilidade (Brier) maior que o "
                "baseline constante. A discriminação acima de 0,5 em ROC AUC não basta "
                "para concluir que suas probabilidades são melhores."
            )
        st.dataframe(
            pd.DataFrame(
                {"Modelo — teste": metrics["test"], "Baseline — teste": metrics["baseline_test"]}
            )
        )
        st.caption(
            "ROC AUC e precisão média: maior é melhor. Brier: menor é melhor. "
            "Precisão e recall usam limiar 0,5. Baseline prevê a prevalência do treino."
        )
        with st.expander("Períodos, coeficientes e limitações"):
            st.json(metrics)

with chat:
    st.subheader("Converse com os indicadores do recorte")
    enabled = llm_enabled()
    use_llm = st.toggle("Usar LLM (requer OPENAI_API_KEY e consome a API)", disabled=not enabled)
    if not enabled:
        st.info("Demonstração com resumo local. Chamadas ao LLM estão desativadas neste ambiente.")
    st.caption(
        "Modo local: resumo fixo dos filtros. LLM: perguntas livres sobre agregados; "
        "os dados agregados e a pergunta são enviados ao provedor."
    )
    question = st.text_input(
        "Pergunta", placeholder="Quais companhias têm maior taxa de atraso?", max_chars=2000
    )
    if st.button("Consultar", disabled=not question.strip()):
        try:
            with st.spinner("Consultando os indicadores..."):
                result = answer(question, filtered, use_llm)
            st.write(result["answer"])
            with st.expander("Contexto usado na resposta"):
                st.json(result["context"])
        except ValueError as error:
            st.error(str(error))
        except OpenAIError:
            st.error("Não foi possível consultar o provedor de IA. Confira a configuração.")

with about:
    st.markdown("""
    **Analista de dados:** qualidade da base, definição de métricas, filtros e indicadores.

    **Cientista de dados:** regressão logística, baseline e avaliação temporal sem dados futuros.

    **Engenheiro de IA:** contexto calculado para LLM, limites de entrada e integração com provedor.

    **Desenvolvedor Python:** pacote, CLI, API FastAPI, validação de contratos e testes.
    """)
    st.json(quality)

loading.empty()
st.session_state["flightlab_ready"] = True
