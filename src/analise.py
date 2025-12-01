# ------------------------------
# ANÁLISE DE RENDA (PIZZA)
# ------------------------------
if menu == "📊 Renda":
    st.header("📊 Distribuição de Renda (Pizza)")

    st.write("Gráfico de pizza com legenda indicando a cor correspondente a cada gênero.")

    numeric_cols = renda.select_dtypes(include="number").columns.tolist()

    # tentativa de identificar automaticamente uma coluna de gênero
    genero_colunas_possiveis = ["sexo", "Sexo", "SEXO", "genero", "Genero", "Gênero", "gênero", "gender"]
    genero_col = None

    for col in renda.columns:
        if col in genero_colunas_possiveis:
            genero_col = col
            break

    if genero_col is None:
        st.warning("Nenhuma coluna de gênero identificada automaticamente. A legenda será baseada na categoria da coluna selecionada.")

    if len(numeric_cols) == 0:
        st.warning("Nenhuma coluna numérica encontrada na tabela de renda.")
    else:
        coluna = st.selectbox("Selecione a coluna para visualizar:", numeric_cols)

        # agrega valores para o gráfico
        if genero_col:
            renda_grouped = renda.groupby(genero_col)[coluna].sum().reset_index()
            renda_grouped.columns = ["Gênero", "Valor"]

            fig = px.pie(
                renda_grouped,
                names="Gênero",
                values="Valor",
                hole=0.4,
                title=f"Distribuição da coluna: {coluna} por gênero",
                color="Gênero"
            )
        else:
            renda_grouped = renda[coluna].value_counts().reset_index()
            renda_grouped.columns = ["Categoria", "Valor"]

            fig = px.pie(
                renda_grouped,
                names="Categoria",
                values="Valor",
                hole=0.4,
                title=f"Distribuição da coluna: {coluna}"
            )

        # labels internas e legenda automática
        fig.update_traces(textposition="inside", textinfo="percent+label")

        # posiciona a legenda ao lado
        fig.update_layout(
            legend=dict(
                title="Legenda",
                orientation="v",
                x=1.05,
                y=0.5
            )
        )

        st.plotly_chart(fig, use_container_width=True)
