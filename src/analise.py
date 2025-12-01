import pandas as pd
import plotly.express as px
from pathlib import Path

# ================================
# Carregar arquivos
# ================================
DATA_DIR = Path("./data")

df_renda = pd.read_csv(DATA_DIR / "tabela2_renda.csv")
df_raca_idade = pd.read_csv(DATA_DIR / "tabela_9_raca-idade.csv")

print("Arquivos carregados com sucesso!")
print(df_renda.head())
print(df_raca_idade.head())

# ================================
# Gráfico 1 – Distribuição de renda
# ================================
fig1 = px.bar(
    df_renda,
    x=df_renda.columns[0],      # primeira coluna como eixo X
    y=df_renda.columns[1],      # segunda como Y
    title="Distribuição da renda (Tabela 2)",
    labels={"x": "Categoria", "y": "Valor"}
)
fig1.show()

# ================================
# Gráfico 2 – População por raça e idade
# ================================
colunas = df_raca_idade.columns
fig2 = px.line(
    df_raca_idade,
    x=colunas[1],  # Idade
    y=colunas[2],  # População
    color=colunas[0],  # Raça
    title="População por raça e idade (Tabela 9)"
)
fig2.show()

# ================================
# Gráfico 3 – Heatmap raça × faixa etária
# ================================
if df_raca_idade[colunas[1]].dtype != "object":
    df_raca_idade["faixa_etaria"] = pd.cut(
        df_raca_idade[colunas[1]],
        bins=10
    )

pivot = df_raca_idade.pivot_table(
    values=colunas[2],
    index="faixa_etaria",
    columns=colunas[0],
    aggfunc="sum"
)

fig3 = px.imshow(
    pivot,
    labels=dict(x="Raça", y="Faixa Etária", color="População"),
    title="Heatmap – População por raça e faixa etária"
)
fig3.show()
