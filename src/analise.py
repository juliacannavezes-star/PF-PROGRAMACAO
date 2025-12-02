import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------
# TÍTULO
# ------------------------------
st.title("Análise Interativa dos Dados – PF Programação")
st.write("Esse site é um projeto elaborado pelas alunas Julia Fleury e Luiza Beyruth com o intuito de fornecer uma visualização dos dados do Perfil da Advocacia Brasileira, de uma maneira mais clara e nítida para os usuários, com base nos critérios de renda e de raça/idade a partir das tabelas de dados disponibilizadas pelo estudo da FGV disponível nesse link: https://conhecimento.fgv.br/sites/default/files/2025-01/publicacoes/perfil_adv_1o-estudo_demografico_da_advocacia_brasileira.pdf")

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

    # mantém somente escolha numérica
    numeric_cols = renda.select_dtypes(include="number").columns.tolist()

    if len(numeric_cols) == 0:
        st.warning("Nenhuma coluna numérica encontrada na tabela de renda.")
    else:
        coluna = st.selectbox("Selecione a variável numérica:", numeric_cols)

        # verifica se existe coluna de gênero
        if "Genero" in renda.columns:
            categoria = "Genero"
        elif "Gênero" in renda.columns:
            categoria = "Gênero"
        else:
            st.warning("Nenhuma coluna de gênero encontrada.")
            categoria = None

        if categoria:
            fig = px.pie(
                renda,
                names=categoria,
                values=coluna,
                title=f"Distribuição de {coluna} por {categoria}"
            )

            fig.update_layout(showlegend=True)
            st.plotly_chart(fig, use_container_width=True)

# ------------------------------
# ANÁLISE DE RAÇA E IDADE
# ------------------------------
else:
    st.header("🧑🏽‍🧒🏿 Análise por Raça e Idade")

    num_cols = raca_idade.select_dtypes(include="number").columns.tolist()

    if len(num_cols) < 1:
        st.warning("Nenhuma coluna numérica encontrada.")
    else:
        num = st.selectbox("Escolha a variável numérica:", num_cols)

        # legenda automática com faixa etária
        if "Faixa Etária" in raca_idade.columns:
            categoria = "Faixa Etária"
        elif "Faixa_etaria" in raca_idade.columns:
            categoria = "Faixa_etaria"
        else:
            st.warning("Nenhuma coluna de faixa etária encontrada.")
            categoria = None

        if categoria:
            fig = px.pie(
                raca_idade,
                names=categoria,
                values=num,
                title=f"{num} distribuído por {categoria}"
            )

            fig.update_layout(showlegend=True)
            st.plotly_chart(fig, use_container_width=True)

st.success("App carregado com sucesso!")
