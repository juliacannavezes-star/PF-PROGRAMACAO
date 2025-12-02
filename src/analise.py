import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------
# TÍTULO
# ------------------------------
st.title("Análise Interativa dos Dados sobre o Perfil da Advocacia Brasileira – PF Programação")
st.write(" Esse site é um projeto elaborado pelas alunas Julia Fleury e Luiza Beyruth com o intuito de fornecer uma visualização dos dados do Perfil da Advocacia Brasileira, de uma maneira mais clara e nítida para os usuários, com base nos critérios de renda e de raça/idade a partir das tabelas de dados disponibilizadas pelo estudo da FGV disponível nesse link: https://conhecimento.fgv.br/sites/default/files/2025-01/publicacoes/perfil_adv_1o-estudo_demografico_da_advocacia_brasileira.pdf")

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
    st.header("📊 Distribuição de Renda")

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
    st.header("🧑🏽‍🧒🏿 Análise por Raça e Idade")

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
