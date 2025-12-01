import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------
# TÍTULO
# ------------------------------
st.title("Análise Interativa dos Dados – PF Programação")
st.write("Visualização interativa das tabelas de renda e raça/idade usando gráficos de pizza.")

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
# ANÁLISE DE RENDA (AGORA SOMENTE PIZZA)
# ------------------------------
if menu == "📊 Renda":
    st.header("📊 Distribuição de Renda (Pizza)")

    st.write("Todos os gráficos de renda foram convertidos para pizza. Selecione uma coluna numérica para visualizar sua distribuição.")

    numeric_cols = renda.select_dtypes(include="number").columns.tolist()

    if len(numeric_cols) == 0:
        st.warning("Nenhuma coluna numérica encontrada na tabela de renda.")
    else:
        coluna = st.selectbox("Selecione a coluna para visualizar:", numeric_cols)

        # Criando proporções da coluna selecionada
        renda_grouped = renda[coluna].value_counts().reset_index()
        renda_grouped.columns = ["Categoria", "Valor"]

        fig = px.pie(
            renda_grouped,
            names="Categoria",
            values="Valor",
            hole=0.4,
            title=f"Distribuição da coluna: {coluna} (Pizza)"
        )
        st.plotly_chart(fig, use_container_width=True)

# ------------------------------
# ANÁLISE DE RAÇA E IDADE (AGORA SOMENTE PIZZA)
# ------------------------------
else:
    st.header("🧑🏽‍🧒🏿 Raça e Idade (Pizza)")

    st.write("Todos os gráficos desta seção foram substituídos por gráficos de pizza.")

    cat_cols = raca_idade.select_dtypes(exclude="number").columns.tolist()
    num_cols = raca_idade.select_dtypes(include="number").columns.tolist()

    if len(cat_cols) < 1 or len(num_cols) < 1:
        st.warning("Não foi possível identificar colunas categóricas e numéricas automaticamente.")
    else:
        cat = st.selectbox("Escolha a variável categórica:", cat_cols)
        num = st.selectbox("Escolha a variável numérica (valor para o gráfico):", num_cols)

        fig_pizza = px.pie(
            raca_idade,
            names=cat,
            values=num,
            title=f"Distribuição de {num} por {cat}",
            hole=0.4
        )
        st.plotly_chart(fig_pizza, use_container_width=True)

st.success("App carregado com sucesso!")
