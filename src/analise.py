import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------
# TÍTULO
# ------------------------------
st.title("Análise Interativa dos Dados – PF Programação")
st.write("Visualização interativa das tabelas de renda e raça/idade usando gráficos de pizza com legenda.")

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
# ANÁLISE DE RENDA (PIZZA)
# ------------------------------
if menu == "📊 Renda":
    st.header("📊 Distribuição de Renda (Pizza)")

    st.write("Gráfico em formato de pizza com legenda completa e percentuais internos.")

    numeric_cols = renda.select_dtypes(include="number").columns.tolist()

    if len(numeric_cols) == 0:
        st.warning("Nenhuma coluna numérica encontrada na tabela de renda.")
    else:
        coluna = st.selectbox("Selecione a coluna para visualizar:", numeric_cols)

        # Agrupamento dos valores
        renda_grouped = renda[coluna].value_counts().reset_index()
        renda_grouped.columns = ["Categoria", "Valor"]

        fig = px.pie(
            renda_grouped,
            names="Categoria",
            values="Valor",
            hole=0.35,
            title=f"Distribuição da coluna: {coluna}",
        )

        # -----------------------------------------------
        # >>>>>>> LEGENDA MELHORADA <<<<<<<<
        # -----------------------------------------------
        fig.update_layout(
            legend=dict(
                title="Categorias",
                orientation="v",
                yanchor="top",
                y=0.98,
                xanchor="left",
                x=1.05,  # legenda à direita do gráfico
                bgcolor="rgba(240,240,240,0.4)",
                bordercolor="gray",
                borderwidth=1
            )
        )

        # Labels internas
        fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
        )

        st.plotly_chart(fig, use_container_width=True)

# ------------------------------
# ANÁLISE DE RAÇA E IDADE (PIZZA)
# ------------------------------
else:
    st.header("🧑🏽‍🧒🏿 Raça e Idade (Pizza)")

    st.write("Gráfico em formato de pizza com legenda automática e percentuais.")

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
            hole=0.35
        )

        fig_pizza.update_traces(textposition="inside", textinfo="percent+label")

        st.plotly_chart(fig_pizza, use_container_width=True)

st.success("App carregado com sucesso!")
