import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------
# TÍTULO
# ------------------------------
st.title("Análise Interativa dos Dados – PF Programação")
st.write("Visualização dos dados de renda e raça/idade a partir dos arquivos CSV fornecidos.")

# ------------------------------
# LEITURA DOS DADOS
# ------------------------------
@st.cache_data
def load_data():
    renda = pd.read_csv("tabela2_renda.csv")
    raca_idade = pd.read_csv("tabela_9_raca-idade.csv")
    return renda, raca_idade

renda, raca_idade = load_data()

# ------------------------------
# MENU LATERAL
# ------------------------------
menu = st.sidebar.selectbox(
    "Selecione a análise:",
    ["📊 Renda", "🧑🏽‍🧒🏿 Raça e Idade"]
)

# ------------------------------
# ANÁLISE DE RENDA (AJUSTADO)
# ------------------------------
if menu == "📊 Renda":
    st.header("📊 Distribuição de Renda (Gráfico de Pizza)")

    # seleciona apenas colunas numéricas
    numeric_cols = renda.select_dtypes(include="number").columns.tolist()

    if len(numeric_cols) == 0:
        st.warning("Nenhuma coluna numérica encontrada na tabela de renda.")
    else:
        coluna = st.selectbox("Selecione a coluna numérica para visualizar:", numeric_cols)

        # gráfico de pizza
        fig = px.pie(
            renda,
            names=renda.index,
            values=coluna,
            title=f"Distribuição da coluna: {coluna}",
        )

        fig.update_layout(showlegend=True)
        st.plotly_chart(fig, use_container_width=True)

# ------------------------------
# ANÁLISE DE RAÇA E IDADE (AJUSTADO)
# ------------------------------
else:
    st.header("🧑🏽‍🧒🏿 Análise por Raça e Idade (Gráfico de Pizza)")

    # identifica colunas numéricas
    num_cols = raca_idade.select_dtypes(include="number").columns.tolist()

    if len(num_cols) < 1:
        st.warning("Não foi possível identificar colunas numéricas.")
    else:
        num = st.selectbox("Escolha a variável numérica:", num_cols)

        # gráfico de pizza SOMENTE com variável numérica
        fig = px.pie(
            raca_idade,
            names=raca_idade.index,
            values=num,
            title=f"Distribuição da variável: {num}",
        )

        fig.update_layout(showlegend=True)
        st.plotly_chart(fig, use_container_width=True)

st.success("App carregado com sucesso!")
