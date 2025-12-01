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
# ANÁLISE DE RENDA
# ------------------------------
if menu == "📊 Renda":
    st.header("📊 Distribuição de Renda")

    st.write("Visualização interativa da tabela de renda.")

    # Se existir uma coluna numérica de renda:
    numeric_cols = renda.select_dtypes(include="number").columns.tolist()

    if len(numeric_cols) == 0:
        st.warning("Nenhuma coluna numérica encontrada na tabela de renda.")
    else:
        coluna = st.selectbox("Selecione a coluna para visualizar:", numeric_cols)

        fig = px.histogram(
            renda,
            x=coluna,
            nbins=20,
            title=f"Distribuição da coluna: {coluna}"
        )
        st.plotly_chart(fig, use_container_width=True)

        fig2 = px.box(
            renda,
            y=coluna,
            title=f"Boxplot da coluna: {coluna}"
        )
        st.plotly_chart(fig2, use_container_width=True)

# ------------------------------
# ANÁLISE DE RAÇA E IDADE
# ------------------------------
else:
    st.header("🧑🏽‍🧒🏿 Análise por Raça e Idade")

    st.write("Dados extraídos da tabela de raça por idade.")

    # tenta identificar automaticamente colunas categóricas e numéricas
    cat_cols = raca_idade.select_dtypes(exclude="number").columns.tolist()
    num_cols = raca_idade.select_dtypes(include="number").columns.tolist()

    if len(cat_cols) < 1 or len(num_cols) < 1:
        st.warning("Não foi possível identificar colunas categóricas e numéricas automaticamente.")
    else:
        cat = st.selectbox("Escolha a variável categórica:", cat_cols)
        num = st.selectbox("Escolha a variável numérica:", num_cols)

        # ------------------------------
        # GRÁFICO DE PIZZA
        # ------------------------------
        fig_pizza = px.pie(
            raca_idade,
            names=cat,
            values=num,
            title=f"Distribuição de {num} por {cat}",
            hole=0.3  # donut bonito 😎 (pode remover se quiser pizza completa)
        )
        st.plotly_chart(fig_pizza, use_container_width=True)

        # ------------------------------
        # SCATTER (mantido)
        # ------------------------------
        fig2 = px.scatter(
            raca_idade,
            x=cat,
            y=num,
            color=cat,
            title=f"Relação entre {cat} e {num}",
        )
        st.plotly_chart(fig2, use_container_width=True)

st.success("App carregado com sucesso!")
