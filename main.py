# %% Libraries
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
# import squarify
import numpy as np
from datetime import datetime
import plotly.express as px
import streamlit as st
# %% URL

# TON URL ORIGINALE
url_originale = "https://docs.google.com/spreadsheets/d/1ZuJmHM5Si2NCUJ3sS2XOklB73WZom3LvwbZQ9xGTp-8/edit?gid=522928352#gid=522928352"

# CONVERTIR EN URL D'EXPORT CSV
# Format : /export?format=csv&gid=SHEET_ID
sheet_id = "1ZuJmHM5Si2NCUJ3sS2XOklB73WZom3LvwbZQ9xGTp-8"
gid = "522928352"  # L'ID de ton onglet spécifique
url_csv1 = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"

# %% Data cleaning
def create_clean_data(url_csv=url_csv1) :
    """
    Prends un l'URL google Drive au bon format ( f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}" )
    Selon le modèle prédèfinis
    et renvoie un DataFrame avec les dates en index et les valeurs des différents valeurs en colonnes
    """
    df = pd.read_csv(url_csv)
    df = df.T 
    lignes_a_supp = ["Répartition", "Produit", "Banque", "+/- values latentes"] + [ind for ind in df.index if ind.startswith('Unnamed')]
    df = df.drop(lignes_a_supp) #tous els df ) sont remplacables par des inplace=True
    df = df.drop(0, axis="columns")
    df = df.reset_index()
    df = df.drop(df.columns[-1] , axis="columns")
    colonnes = ["index", "BB_Courant", "BB_PEA", "BB_PEA_PME", "BB_AV_MSCIWorld", "BB_AV_FE", "HB_Courant", "HB_Gab_Mat", "HB_LEP", "HB_LDDS", "HB_LivretA", "HB_LivretJeune", "MT_AV_SP500", "MT_AV_STOXX50","MT_AV_MSCIEM", "MT_AV_FE", "TR_Titre_Or", "TR_Titre_Argent", "TR_courant"]
    df.columns = colonnes
    df = df.set_index("index")
    Invest_Inital = []
    Invest_Inital = df.loc["Invest initial"]
    df= df.drop("Invest initial")
    #la c'est singe mais je crois que c'est le seul moyen sans devoir changer la local francaisset donc s'adapter a un environemment linux/macOS et windows différement
    mois = {
    'janvier': 'January', 'février': 'February', 'mars': 'March',
    'avril': 'April', 'mai': 'May', 'juin': 'June',
    'juillet': 'July', 'août': 'August', 'septembre': 'September',
    'octobre': 'October', 'novembre': 'November', 'décembre': 'December'
    }
    df.index = df.index.to_series().replace(mois, regex=True)
    df.index = pd.to_datetime(df.index, dayfirst=True)
    df = df.fillna(0)
    df = df.replace({' ': ''}, regex=True)
    df = df.apply(pd.to_numeric)
    Invest_Inital = Invest_Inital.replace({' ': ''}, regex=True)
    Invest_Inital = Invest_Inital.apply(pd.to_numeric)
    return df, Invest_Inital

df, Invest_Inital = create_clean_data()

# %% Configurations (Colors, classes)

Classe = {
    "Monetaire": ['BB_Courant', 'HB_Courant', 'HB_Gab_Mat', 'TR_courant'],
    "Livrets": ['HB_LEP', 'HB_LDDS', 'HB_LivretA', 'HB_LivretJeune'],
    "Fonds_Euro": ['BB_AV_FE', 'MT_AV_FE'],
    "Matieres_Premieres": ['TR_Titre_Or', 'TR_Titre_Argent'],
    "Actions": ['BB_PEA', 'BB_PEA_PME', 'BB_AV_MSCIWorld','MT_AV_SP500', 'MT_AV_STOXX50', 'MT_AV_MSCIEM']
}

couleurs_classes = {
    "Monetaire": "#4e79a7",     # Bleu nuit doux (stabilité)
    "Livrets": "#59a14f",       # Vert émeraude (sécurisé)
    "Fonds_Euro": "#f28e2b",    # Orange chaleureux (garanti)
    "Matieres_Premieres": "#bab0ac",  # Gris taupe (commodities neutre)
    "Actions": "#e15759"        # Rouge corail (risque)
}

""" couleurs_classes = {
    "Monetaire": "#1f77b4",           # bleu
    "Livrets": "#2ca02c",             # vert
    "Fonds_Euro": "#ff7f0e",          # orange
    "Matieres_Premieres": "#9467bd",  # violet
    "Actions": "#d62728"              # rouge
} """

AV = {
    "FE": ['BB_AV_FE', 'MT_AV_FE'],
    'Actions': ['BB_AV_MSCIWorld', 'MT_AV_SP500', 'MT_AV_STOXX50', 'MT_AV_MSCIEM']
}
# %% Data processing (Calculations)

dic_Total_Par_Classe = {}
for classe in Classe  : 
    dic_Total_Par_Classe[classe] = df[Classe[classe]].sum(axis=1)

df_Total_Par_Classe = pd.DataFrame(dic_Total_Par_Classe)

df_Total_Par_Classe = df_Total_Par_Classe.sort_values(
    by=df_Total_Par_Classe.index[0],  # dernière date
    axis=1,                            # trier les colonnes (et non les lignes)
    ascending=False                    # du plus grand au plus petit
)

Total_Par_Classe_last_sorted = df_Total_Par_Classe.iloc[0]

# %% Charts functions
def Montant_par_classes_Bar(ax, nb=0) :
    barres = ax[nb].bar(df_Total_Par_Classe.columns,
                        Total_Par_Classe_last_sorted,
                        color=[couleurs_classes[col] for col in df_Total_Par_Classe.columns])
    ax[nb].bar_label(barres, fmt='%d')
    ax[nb].set_title("Montant par classes")
    ax[nb].set_xticklabels(Total_Par_Classe_last_sorted.index, rotation=20)

def Repartition_par_classe_pie(ax, nb=0):
    ax[nb].pie(Total_Par_Classe_last_sorted,
               labels=Total_Par_Classe_last_sorted.index,
               autopct = "%d",
               colors=[couleurs_classes[col] for col in Total_Par_Classe_last_sorted.index],)
    ax[nb].set_title("Répartition par classe")

def Repartition_AV(ax, nb=0):
    ax[nb].pie([df[AV["Actions"]].sum(axis="columns")[0], df[AV["FE"]].sum(axis="columns")[0]], labels=["Actions", "Fonds Euros"], autopct = "%d", colors=[couleurs_classes["Actions"], couleurs_classes["Fonds_Euro"]])
    ax[nb].set_title("Répartition AV")

def Evolution_totale_classe_stackplot(ax, nb=0):
    ax[nb].stackplot(
        df_Total_Par_Classe.index,                    # axe des X
        [df_Total_Par_Classe[col] for col in df_Total_Par_Classe.columns],  # valeurs empilées
        labels=df_Total_Par_Classe.columns,           # légende
        alpha=0.8,
        colors=[couleurs_classes[col] for col in df_Total_Par_Classe.columns]
    )
    ax[nb].set_title("Évolution totale par classe")
    ax[nb].set_xlabel("Date")
    ax[nb].set_ylabel("Valeur(€)")
    ax[nb].legend(loc="upper left")
    ax[nb].set_xticks(df_Total_Par_Classe.index)
    ax[nb].set_xticklabels(df_Total_Par_Classe.index.strftime('%b %y'), rotation=45, ha='center')

def Evolution_totale_par_classe_bar(ax, nb=0):
    bottom = [0 for i in range(len(df.index))]
    for classe in df_Total_Par_Classe.columns :
        height = df[Classe[classe]].sum(axis="columns")
        barres = ax[nb].bar(df.index, height, bottom=bottom, width=13, color=couleurs_classes[classe])
        bottom += height
    ax[nb].set_xticks(df_Total_Par_Classe.index)
    ax[nb].set_xticklabels(df_Total_Par_Classe.index.strftime('%b %y'), rotation=45, ha='center')
    ax[nb].set_title("Evolution totale par classe")

""" def Repartition_par_ligne_Mondrian(ax, nb=0):
    "Mondrian, aussi appelé Treemap"
    squarify.plot(
        sizes=df.iloc[0],
        label=[col if df.iloc[0][col] > df.iloc[0].max() * 0.03 else "" for col in df.columns],
        ax = ax[nb],
        pad = 1,
        alpha = 0.8,
        text_kwargs={'fontsize': 8, "wrap":True}
    )
    ax[nb].set_title("Répartition par ligne")
    ax[nb].axis("off") """

def Evolution_titres_stackplot(ax, nb=0):
    df_titre = df[Classe["Actions"]+Classe["Matieres_Premieres"]]
    df_titre = df_titre.sort_values(by=df_titre.index[0], axis="columns")
    ax[nb].stackplot(
        df_titre.index,
        [df_titre[col] for col in df_titre.columns],
        labels=df_titre.columns,
        alpha=0.8
    )
    ax[nb].set_title("Evolution des titres cotées")
    ax[nb].legend(loc="upper left")
    ax[nb].set_xlabel("Date")
    ax[nb].set_ylabel("Valeur(€)")
    ax[nb].set_xticks(df_Total_Par_Classe.index)
    ax[nb].set_xticklabels(df_Total_Par_Classe.index.strftime('%b %y'), rotation=45, ha='center')

def performance_ligne_bar(ax, nb=0, date1="2025-01-26", date2="2025-04-15"):
    df_titre = df[Classe["Actions"]+Classe["Matieres_Premieres"]]
    df_titre = df_titre.sort_values(by=df_titre.index[0], axis="columns")
    Invest_Inital_titre = Invest_Inital[Classe["Actions"]+Classe["Matieres_Premieres"]]

    def perf(ref):
        """retourne la listes des perf actuel en pourcentage p/r à ref"""
        return (df_titre.iloc[0] / ref - 1 ) *100

    df_titre_perf = pd.concat([perf(Invest_Inital_titre), perf(df_titre.loc[date1]), perf(df_titre.loc[date2])], axis=1)
    df_titre_perf.columns = ["Invest_init", date1, date2]
    df_titre_perf = df_titre_perf.where(df_titre_perf <= 100, 0) #élimine les valeurs aberrants

    x = np.arange(len(df_titre_perf.index))  # positions sur l'axe x
    width = 0.25

    multiplier = 0
    for col in df_titre_perf.columns:
        offset = width * multiplier
        rects = ax[nb].bar(x + offset, df_titre_perf[col], width, label=col)
        ax[nb].bar_label(rects, padding=3, fmt='%.1f')
        multiplier += 1

    ax[nb].set_xticks(x + width)  # pour centrer les labels sous les groupes
    ax[nb].set_xticklabels(df_titre_perf.index, rotation=45, ha='right')
    ax[nb].set_ylabel("Rendement en %")
    ax[nb].set_title("Performances par ligne")
    ax[nb].legend()

def Evolution_totale_classe_stackplot_plotly(selected_classes=None):
    # rest à faire en sorte que la légende, et le graphique s'adapte toujours pour mettre les classes les plus importantes en dessous des classes plus légères pour l'esthétique du graphique
    if selected_classes is None or len(selected_classes) == 0:
        selected_classes = df_Total_Par_Classe.columns.tolist()

    selected_classes = [c for c in selected_classes if c in df_Total_Par_Classe.columns]
    if len(selected_classes) == 0:
        selected_classes = df_Total_Par_Classe.columns.tolist()

    # Trier les classes par valeur décroissante à la dernière date pour l'empilement
    selected_classes = sorted(selected_classes, key=lambda c: df_Total_Par_Classe.iloc[0][c], reverse=True)

    data = df_Total_Par_Classe.loc[:, selected_classes]

    fig = px.area(
        data,
        x=data.index,
        y=data.columns,
        markers=True,
        title="Évolution totale par classe",
        labels={"value": "Valeur(€)", "index": "Date"},
        color_discrete_map=couleurs_classes
    )

    fig.update_layout(legend_title_text='Classes')
    return fig

def Repartition_par_classe_pie_plotly(selected_classes=None, date=None):
    if selected_classes is None or len(selected_classes) == 0:
        selected_classes = df_Total_Par_Classe.columns.tolist()

    selected_classes = [c for c in selected_classes if c in df_Total_Par_Classe.columns]
    if len(selected_classes) == 0:
        selected_classes = df_Total_Par_Classe.columns.tolist()

    if date is None:
        date = df_Total_Par_Classe.index.max()
    else:
        date = pd.to_datetime(date)

    # Prendre la date la plus proche (<= sélectionnée)
    available_dates = df_Total_Par_Classe.index[df_Total_Par_Classe.index <= date]
    if len(available_dates) == 0:
        # Si date trop petite, prendre la plus petite
        date = df_Total_Par_Classe.index.min()
    else:
        date = available_dates.max()

    values = df_Total_Par_Classe.loc[date, selected_classes]

    fig = px.pie(
        data_frame=pd.DataFrame({'classes': values.index, 'values': values.values}),
        names='classes',
        values='values',
        color='classes',
        color_discrete_map=couleurs_classes,
        title=f"Répartition par classe au {date.strftime('%d/%m/%Y')}"
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

def Performance_par_classe_glissante(selected_classes=None, date_debut=None, date_fin=None):
    """
    Calcule la performance de chaque classe sur :
    - 3 mois glissant
    - 6 mois glissant
    - 1 an glissant
    - Depuis date_debut (ou depuis début si None)
    
    Retourne un DataFrame avec ces performances
    """
    if selected_classes is None or len(selected_classes) == 0:
        selected_classes = df_Total_Par_Classe.columns.tolist()
    
    selected_classes = [c for c in selected_classes if c in df_Total_Par_Classe.columns]
    
    if date_fin is None:
        date_fin = df_Total_Par_Classe.index.max()
    else:
        date_fin = pd.to_datetime(date_fin)
    
    if date_debut is None:
        date_debut = df_Total_Par_Classe.index.min()
    else:
        date_debut = pd.to_datetime(date_debut)
    
    # Trouver les dates les plus proches
    idx_fin = df_Total_Par_Classe.index.get_indexer([date_fin], method='nearest')[0]
    date_fin = df_Total_Par_Classe.index[idx_fin]
    
    # Trouver la date 3 mois avant (approximativement 90 jours)
    date_3m = date_fin - pd.Timedelta(days=90)
    idx_3m = df_Total_Par_Classe.index.get_indexer([date_3m], method='nearest')[0]
    date_3m = df_Total_Par_Classe.index[idx_3m]
    
    # Trouver la date 6 mois avant (approximativement 180 jours)
    date_6m = date_fin - pd.Timedelta(days=180)
    idx_6m = df_Total_Par_Classe.index.get_indexer([date_6m], method='nearest')[0]
    date_6m = df_Total_Par_Classe.index[idx_6m]
    
    # Trouver la date 1 an avant (approximativement 365 jours)
    date_1y = date_fin - pd.Timedelta(days=365)
    idx_1y = df_Total_Par_Classe.index.get_indexer([date_1y], method='nearest')[0]
    date_1y = df_Total_Par_Classe.index[idx_1y]
    
    # Trouver la date de début la plus proche
    idx_debut = df_Total_Par_Classe.index.get_indexer([date_debut], method='nearest')[0]
    date_debut = df_Total_Par_Classe.index[idx_debut]
    
    # Calculer les performances
    performances = []
    for classe in selected_classes:
        val_fin = df_Total_Par_Classe.loc[date_fin, classe]
        val_3m = df_Total_Par_Classe.loc[date_3m, classe]
        val_6m = df_Total_Par_Classe.loc[date_6m, classe]
        val_1y = df_Total_Par_Classe.loc[date_1y, classe]
        val_debut = df_Total_Par_Classe.loc[date_debut, classe]
        
        perf_3m = ((val_fin / val_3m) - 1) * 100
        perf_6m = ((val_fin / val_6m) - 1) * 100
        perf_1y = ((val_fin / val_1y) - 1) * 100
        perf_depuis_debut = ((val_fin / val_debut) - 1) * 100
        
        performances.append({
            'Classe': classe,
            'Perf 3M (%)': round(perf_3m, 2),
            'Perf 6M (%)': round(perf_6m, 2),
            'Perf 1Y (%)': round(perf_1y, 2),
            f'Perf depuis {date_debut.strftime("%d/%m/%Y")} (%)': round(perf_depuis_debut, 2)
        })
    
    df_perf = pd.DataFrame(performances)
    return df_perf


def Evolution_totale_ligne_plotly(selected_lignes=None):
    # Filtrage des lignes sélectionnées
    if selected_lignes is None or len(selected_lignes) == 0:
        selected_lignes = df.columns.tolist()

    selected_lignes = [l for l in selected_lignes if l in df.columns]
    if len(selected_lignes) == 0:
        selected_lignes = df.columns.tolist()

    # Trier les lignes par valeur décroissante à la dernière date pour l'empilement
    selected_lignes = sorted(selected_lignes, key=lambda l: df.iloc[0][l], reverse=True)

    data = df.loc[:, selected_lignes]

    fig = px.area(
        data,
        x=data.index,
        y=data.columns,
        markers=True,
        title="Évolution totale par ligne",
        labels={"value": "Valeur(€)", "index": "Date"}
    )
    fig.update_layout(legend_title_text='Lignes')
    return fig


def Repartition_par_ligne_pie_plotly(selected_lignes=None, date=None):
    if selected_lignes is None or len(selected_lignes) == 0:
        selected_lignes = df.columns.tolist()

    selected_lignes = [l for l in selected_lignes if l in df.columns]
    if len(selected_lignes) == 0:
        selected_lignes = df.columns.tolist()

    if date is None:
        date = df.index.max()
    else:
        date = pd.to_datetime(date)

    # Prendre la date la plus proche (<= sélectionnée)
    available_dates = df.index[df.index <= date]
    if len(available_dates) == 0:
        # Si date trop petite, prendre la plus petite
        date = df.index.min()
    else:
        date = available_dates.max()

    values = df.loc[date, selected_lignes]

    fig = px.pie(
        data_frame=pd.DataFrame({'lignes': values.index, 'values': values.values}),
        names='lignes',
        values='values',
        title=f"Répartition par ligne au {date.strftime('%d/%m/%Y')}"
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig


def Performance_par_ligne_glissante(selected_lignes=None, date_debut=None, date_fin=None):
    """
    Calcule la performance de chaque ligne sur :
    - 3 mois glissant
    - 6 mois glissant
    - 1 an glissant
    - Depuis date_debut (ou depuis début si None)

    Retourne un DataFrame avec ces performances
    """
    if selected_lignes is None or len(selected_lignes) == 0:
        selected_lignes = df.columns.tolist()

    selected_lignes = [l for l in selected_lignes if l in df.columns]
    if len(selected_lignes) == 0:
        selected_lignes = df.columns.tolist()

    if date_fin is None:
        date_fin = df.index.max()
    else:
        date_fin = pd.to_datetime(date_fin)

    if date_debut is None:
        date_debut = df.index.min()
    else:
        date_debut = pd.to_datetime(date_debut)

    # Trouver les dates les plus proches
    idx_fin = df.index.get_indexer([date_fin], method='nearest')[0]
    date_fin = df.index[idx_fin]

    # Trouver la date 3 mois avant (approximativement 90 jours)
    date_3m = date_fin - pd.Timedelta(days=90)
    idx_3m = df.index.get_indexer([date_3m], method='nearest')[0]
    date_3m = df.index[idx_3m]

    # Trouver la date 6 mois avant (approximativement 180 jours)
    date_6m = date_fin - pd.Timedelta(days=180)
    idx_6m = df.index.get_indexer([date_6m], method='nearest')[0]
    date_6m = df.index[idx_6m]

    # Trouver la date 1 an avant (approximativement 365 jours)
    date_1y = date_fin - pd.Timedelta(days=365)
    idx_1y = df.index.get_indexer([date_1y], method='nearest')[0]
    date_1y = df.index[idx_1y]

    # Trouver la date de début la plus proche
    idx_debut = df.index.get_indexer([date_debut], method='nearest')[0]
    date_debut = df.index[idx_debut]

    # Calculer les performances
    performances = []
    for ligne in selected_lignes:
        val_fin = df.loc[date_fin, ligne]
        val_3m = df.loc[date_3m, ligne]
        val_6m = df.loc[date_6m, ligne]
        val_1y = df.loc[date_1y, ligne]
        val_debut = df.loc[date_debut, ligne]

        perf_3m = ((val_fin / val_3m) - 1) * 100 if val_3m != 0 else 0
        perf_6m = ((val_fin / val_6m) - 1) * 100 if val_6m != 0 else 0
        perf_1y = ((val_fin / val_1y) - 1) * 100 if val_1y != 0 else 0
        perf_depuis_debut = ((val_fin / val_debut) - 1) * 100 if val_debut != 0 else 0

        performances.append({
            'Ligne': ligne,
            'Perf 3M (%)': round(perf_3m, 2),
            'Perf 6M (%)': round(perf_6m, 2),
            'Perf 1Y (%)': round(perf_1y, 2),
            f'Perf depuis {date_debut.strftime("%d/%m/%Y")} (%)': round(perf_depuis_debut, 2)
        })

    df_perf = pd.DataFrame(performances)
    return df_perf

# %% Main visualisation function

def Visualisation(nb_ligne=2, nb_colonne=3):
    plt.style.use('ggplot')

    fig, ax = plt.subplots(nb_ligne,nb_colonne)

    if nb_ligne * nb_colonne == 1:
        ax = [ax]  # transforme en liste 1D
    else:
        ax = ax.ravel()  # aplati le tableau 2D en 1D

    Repartition_par_classe_pie(ax, 0)
    # Repartition_par_ligne_Mondrian(ax, 1) # pas trop convaincu par celui la mais bon
    Evolution_titres_stackplot(ax, 2)
    Evolution_totale_classe_stackplot(ax, 3)
    performance_ligne_bar(ax, 4)

    plt.show()
# %% Simple visualisation test plotly by classes
fig, ax = plt.subplots(figsize=(12, 6))
# Evolution_totale_classe_stackplot_plotly([ax], nb=0)

# %% some performance calculations
def perf_par_classe(Invest_Inital=Invest_Inital):
    perf_classe = {}
    for classe in Classe :
        invest_init_classe = Invest_Inital[Classe[classe]].sum()
        valeur_actuelle_classe = df[Classe[classe]].iloc[0].sum()
        perf_classe[classe] = (valeur_actuelle_classe / invest_init_classe - 1) * 100
    return perf_classe

perf_classe = perf_par_classe()
perf_classe

def performance_totale(Invest_Inital=Invest_Inital):
    invest_init_total = Invest_Inital[Classe["Actions"] + Classe["Matieres_Premieres"] + Classe["Fonds_Euro"] + Classe["Livrets"]].sum()
    valeur_actuelle_total = df.iloc[0][Classe["Actions"] + Classe["Matieres_Premieres"] + Classe["Fonds_Euro"] + Classe["Livrets"]].sum()
    performance_totale = (valeur_actuelle_total / invest_init_total - 1) * 100
    return performance_totale

performance_totale = performance_totale()
performance_totale

# Bilan
today = datetime.now().strftime("%d/%m/%Y")
last_date = df.index[-1].strftime("%d/%m/%Y")

# Calcul des gains par classe
gains_details = ", ".join([
    f"{classe}: {perf_classe[classe]:.2f}% ({df[Classe[classe]].iloc[0].sum() - Invest_Inital[Classe[classe]].sum():.2f}€)" 
    for classe in perf_classe if classe != "Monetaire"  # Enlève le monétaire
])

gains_realises = sum(df[Classe[classe]].iloc[0].sum() - Invest_Inital[Classe[classe]].sum() for classe in perf_classe if classe != "Monetaire")

performance_message = (
    f"Au {today}, mon portefeuille affiche "
    f"une performance globale de {performance_totale:.2f}%, soit {gains_realises:.2f}€."
)

# Enlève les .00 des valeurs en euros
performance_message = performance_message.replace('.00€', '€')
gains_details = gains_details.replace('.00€', '€')

print(performance_message)
print(f"Détails par classe: {gains_details}.")
print(f"N.B.: Principal Assurance vie ouverte en janvier 2025, placements progressifs en ETF action à partir de mars 2025.")

if __name__ == "__main__":
    st.title("Mon Portofolio d'Investissement")
    st.write("Finary du Pauvre")
    st.write("Dernière mise à jour : " + today)
    st.write(performance_message)

# %%
