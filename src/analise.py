import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------
# FUNÇÃO PARA PADRONIZAR GÊNERO
# ------------------------------
def padronizar_genero(df):
    genero_cols = [col for col in df.columns if "sex" in col.lower() or 
                   "gênero" in col.lower() or 
                   "genero" in col.lower() or 
                   "sexo" in col.lower()]
    
    for col in genero_cols:
        df[col] = df[col].astype(str).str.lower().map({
            "f": "Feminino",
            "0": "Feminino",
            "feminino": "Feminino",
            "m": "Masculino",
            "1": "Masculino",
            "masculino": "Masculino"
        }).fillna(df[col])  # mantém valores que não se encaixam

    return df

# ------------------------------
# TÍTULO
# ------------------------------
st.title("Análise Interativa dos Dados – PF Programação")
st.write("Visualização com gráficos de pizza e legendas de gênero padronizadas.")

# ------------------------------
# LEITURA DOS DADOS
# ------------------------------
@st.cache_data
def load_data():
    renda = pd.read_csv("tabela2_renda.csv")
    raca_idade = pd.read_csv("tabela_9_raca-idade.csv")

    renda = padronizar_genero(renda)
    raca_idade = padronizar_genero(raca_idade)

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
    st.header("📊 Distribuição de Renda (Pizza)")

    numeric_cols = renda.select_dtypes(include="number").columns.tolist()

    if len(numeric_cols) == 0:
        st.warning("Nenhuma coluna numérica encontrada.")
    else:
        coluna = st.selectbox("Selecione a coluna para visualizar:", numeric_cols)

        renda_grouped = renda[coluna].value_counts().reset_index()
        renda_grouped.columns = ["Categoria", "Valor"]

        fig = px.pie(
            renda_grouped,
            names="Categoria",
            values="Valor",
            hole=0.35,
            title=f"Distribuição da coluna: {coluna}",
        )

        # Legenda fixa + labels internas
        fig.update_layout(
            legend=dict(
                title="Categorias",
                orientation="v",
                yanchor="top",
                y=0.98,
                xanchor="left",
                x=1.05,
                bgcolor="rgba(240,240,240,0.4)",
                bordercolor="gray",
                borderwidth=1
            )
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")

        st.plotly_chart(fig, use_container_width=True)

# ------------------------------
# ANÁLISE DE RAÇA E IDADE
# ------------------------------
else:
    st.header("🧑🏽‍🧒🏿 Raça e Idade (Pizza)")

    cat_cols = raca_idade.select_dtypes(exclude="number").columns.tolist()
    num_cols = raca_idade.select_dtypes(include="number").columns.tolist()

    cat = st.selectbox("Escolha a variável categórica:", cat_cols)
    num = st.selectbox("Escolha a variável numérica:", num_cols)

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
