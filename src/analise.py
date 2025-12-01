# ------------------------------
# ANÁLISE DE RENDA (PIZZA)
# ------------------------------
if menu == "📊 Renda":
    st.header("📊 Distribuição de Renda por Gênero (Pizza)")

    st.write("Gráfico em formato de pizza mostrando a distribuição da coluna escolhida separada por gênero.")

    # Identificar colunas numéricas
    numeric_cols = renda.select_dtypes(include="number").columns.tolist()
    
    # Identificar colunas categóricas (para tentar achar 'gênero')
    cat_cols = renda.select_dtypes(exclude="number").columns.tolist()

    # Tentar detectar automaticamente uma coluna de gênero
    possiveis_generos = ["sexo", "genero", "gênero", "Gender", "gender", "Sexo"]
    genero_col = None
    for col in cat_cols:
        if col.lower() in possiveis_generos:
            genero_col = col
            break

    if genero_col is None:
        st.error("Não foi possível identificar automaticamente uma coluna de gênero no CSV.")
    else:
        st.success(f"Coluna de gênero detectada: **{genero_col}**")

        if len(numeric_cols) == 0:
            st.warning("Nenhuma coluna numérica encontrada na tabela de renda.")
        else:
            coluna = st.selectbox("Selecione a coluna de valores:", numeric_cols)

            # Agrupar os dados por gênero
            renda_grouped = renda.groupby(genero_col)[coluna].sum().reset_index()

            fig = px.pie(
                renda_grouped,
                names=genero_col,
                values=coluna,
                color=genero_col,   # 🔥 GERA A LEGENDA AUTOMÁTICA
                hole=0.4,
                title=f"Distribuição da coluna '{coluna}' por gênero"
            )

            # Labels + porcentagem + legenda ativa
            fig.update_traces(textposition="inside", textinfo="percent+label")

            st.plotly_chart(fig, use_container_width=True)
