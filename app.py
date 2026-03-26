import streamlit as st
from streamlit_option_menu import option_menu
from main import Evolution_totale_classe_stackplot_plotly, df_Total_Par_Classe, Repartition_par_classe_pie_plotly, Performance_par_classe_glissante, Evolution_totale_ligne_plotly, Repartition_par_ligne_pie_plotly, Performance_par_ligne_glissante, df

st.set_page_config(
    page_title="Portofolio",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
)

with st.sidebar:
    selected = option_menu(
        menu_title = "Analyse du portofolio",
        options = ["Par Classes","Par Lignes"],
        icons = ["envelope","activity"],
        menu_icon = "cast",
        default_index = 0)

if selected == "Par Classes":
    st.title("Mon Portofolio d'Investissement")
    st.subheader("Dernière mise à jour : " + df_Total_Par_Classe.index.max().strftime("%d/%m/%Y"))

    min_date = df_Total_Par_Classe.index.min().to_pydatetime()
    max_date = df_Total_Par_Classe.index.max().to_pydatetime()

    with st.sidebar:
        classes = st.multiselect(
            "Classes d'actifs à afficher :",
            options=df_Total_Par_Classe.columns.tolist(),
            default=df_Total_Par_Classe.columns.tolist()
        )

    date_debut = st.slider(
        "Date de début du graphique :",
        min_value=min_date,
        max_value=max_date,
        value=min_date,
        format="DD/MM/YYYY"
    )

    fig = Evolution_totale_classe_stackplot_plotly(selected_classes=classes)
    fig.update_xaxes(range=[date_debut, max_date])
    st.plotly_chart(fig)

    st.markdown("---")

    df_perf = Performance_par_classe_glissante(selected_classes=classes, date_debut=date_debut, date_fin=max_date)

    # Formater les colonnes de performance à 2 décimales
    perf_columns = df_perf.columns[1:]
    for col in perf_columns:
        df_perf[col] = df_perf[col].apply(lambda x: f"{x:.2f}" if isinstance(x, (int, float)) else x)

    # Coloration conditionnelle simple
    def color_performance(val):
        try:
            num_val = float(val)
            color = 'green' if num_val > 0 else 'red' if num_val < 0 else 'black'
            return f'color: {color}; font-weight: bold;'
        except (ValueError, TypeError):
            return ''

    styled = df_perf.style.applymap(color_performance, subset=df_perf.columns[1:])
    st.write(styled.to_html(), unsafe_allow_html=True)

    st.markdown("---")

    date_pie = st.slider(
        "Date de la répartition par classe :",
        min_value=min_date,
        max_value=max_date,
        value=max_date,
        format="DD/MM/YYYY"
    )

    fig_pie = Repartition_par_classe_pie_plotly(selected_classes=classes, date=date_pie)
    st.plotly_chart(fig_pie)


elif selected == "Par Lignes":
    st.title("Mon Portofolio d'Investissement")
    st.subheader("Dernière mise à jour : " + df_Total_Par_Classe.index.max().strftime("%d/%m/%Y"))

    min_date = df_Total_Par_Classe.index.min().to_pydatetime()
    max_date = df_Total_Par_Classe.index.max().to_pydatetime()

    with st.sidebar:
        lignes = st.multiselect(
            "Lignes à afficher :",
            options=df.columns.tolist(),
            default=df.columns.tolist()
        )

    date_debut = st.slider(
        "Date de début du graphique :",
        min_value=min_date,
        max_value=max_date,
        value=min_date,
        format="DD/MM/YYYY"
    )

    fig = Evolution_totale_ligne_plotly(selected_lignes=lignes)
    fig.update_xaxes(range=[date_debut, max_date])
    st.plotly_chart(fig)

    st.markdown("---")
    st.subheader("Performance par ligne")
    df_perf = Performance_par_ligne_glissante(selected_lignes=lignes, date_debut=date_debut, date_fin=max_date)

    # Formater les colonnes de performance à 2 décimales
    perf_columns = df_perf.columns[1:]
    for col in perf_columns:
        df_perf[col] = df_perf[col].apply(lambda x: f"{x:.2f}" if isinstance(x, (int, float)) else x)

    # Coloration conditionnelle simple
    def color_performance(val):
        try:
            num_val = float(val)
            color = 'green' if num_val > 0 else 'red' if num_val < 0 else 'black'
            return f'color: {color}; font-weight: bold;'
        except (ValueError, TypeError):
            return ''

    styled = df_perf.style.applymap(color_performance, subset=df_perf.columns[1:])
    st.write(styled.to_html(), unsafe_allow_html=True)

    st.markdown("---")

    date_pie = st.slider(
        "Date de la répartition par ligne :",
        min_value=min_date,
        max_value=max_date,
        value=max_date,
        format="DD/MM/YYYY"
    )

    fig_pie = Repartition_par_ligne_pie_plotly(selected_lignes=lignes, date=date_pie)
    st.plotly_chart(fig_pie)