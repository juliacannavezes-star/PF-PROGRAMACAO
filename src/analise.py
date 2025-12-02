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

# ------------------------------------------------------------
# ANÁLISE DE RENDA (SEM FILTROS, LEGENDA = GÊNERO)
# ------------------------------------------------------------
if menu == "📊 Renda":
    st.header("📊 Distribuição de Renda (Gráfico de Pizza)")

    # Procurar coluna de gênero automaticamente
    possible_gender_names = ["genero", "sexo", "gênero", "Gender", "Sexo"]
    genero_col = None
    for col in renda.columns:
        if col.lower() in possible_gender_names:
            genero_col = col
            break

    # Procurar uma coluna numérica automaticamente
    num_cols = renda.select_dtypes(include="number").columns.tolist()

    if genero_col is None:
        st.error("Não foi encontrada uma coluna de gênero no CSV de renda.")
    elif len(num_cols) == 0:
        st.error("Não foi encontrada nenhuma coluna numérica na tabela de renda.")
    else:
        valor_col = num_cols[0]  # escolhe automaticamente a primeira numérica

        fig = px.pie(
            renda,
            names=genero_col,
            values=valor_col,
            title=f"Distribuição da coluna '{valor_col}' por gênero",
        )

        fig.update_layout(
            showlegend=True,
            legend_title="Gênero"
        )

        st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------------
# ANÁLISE DE RAÇA E IDADE (SEM FILTROS, LEGENDA = FAIXA ETÁRIA)
# ------------------------------------------------------------
else:
    st.header("🧑🏽‍🧒🏿 Análise por Raça e Idade (Gráfico de Pizza)")

    # Procurar coluna categórica (faixa etária)
    cat_cols = raca_idade.select_dtypes(exclude="number").columns.tolist()

    # Procura automaticamente por uma coluna numérica
    num_cols = raca_idade.select_dtypes(include="number").columns.tolist()

    if len(cat_cols) == 0:
        st.error("Não foi encontrada nenhuma coluna categórica (ex.: faixa etária).")
    elif len(num_cols) == 0:
        st.error("Não foi encontrada nenhuma coluna numérica na base de raça e idade.")
    else:
        categoria = cat_cols[0]  # primeira categórica automaticamente
        valor = num_cols[0]      # primeira numérica automaticamente

        fig = px.pie(
            raca_idade,
            names=categoria,
            values=valor,
            title=f"Distribuição da variável '{valor}' por {categoria}",
        )

        fig.update_layout(
            showlegend=True,
            legend_title="Faixa Etária"
        )

        st.plotly_chart(fig, use_container_width=True)

st.success("App carregado com sucesso!")
