#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
from theme_utils import apply_theme


# Appliquer le thème global
chart_template = apply_theme()
#######################
# Page configuration
st.set_page_config(
    page_title="Tableau de Bord Afrique",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

#alt.themes.enable("dark")

#######################
# CSS styling
st.markdown("""
<style>

[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-bottom: -7rem;
}

[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}

[data-testid="stMetric"] {
    background-color: #000000;
    color: #FFFFFF;
    text-align: center;
    padding: 15px 0;
}

[data-testid="stMetricLabel"] {
  display: flex;
  justify-content: center;
  align-items: center;
}

[data-testid="stMetricDeltaIcon-Up"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

[data-testid="stMetricDeltaIcon-Down"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

</style>
""", unsafe_allow_html=True)

#################################Description du Tableau de Bord########################################
st.title("Tableau de Bord de la Situation de L'emploi en AFrique")
st.markdown("""
## Description du tableau de bord
Ce tableau de bord met en lumière un ensemble de 4 indicateurs pour une année donnée. 
- **Carte d'Afrique** : Analyse la situation du chomage dans chaque pays pour ceux ayant les données disponibles.
- **Le Tableau à droite** : Donne la proportion des jeunes qui ne fréquentent pas, qui sont sans emploi ou qui ne cherchent pas à se former.
- **Les deux carrés à gauche** : Ressortent le pays ayant le pib le plus élevé et celui le plus bas.
- **La barre en bas** : Ressortent la proportion du secteur informel par pays pour l'année choisi.

Vous avez en plus la possibilité de selectionner une année de votre choix et une couleur aussi.
""")
######################## Definition des fonctions #######################################
def arranger_data(data):
    df=data
    try:
        a=df["pays"].unique()
        print("pays:",a)
    except:
        try:
            df["pays"]=df["ref_area.label"]
            df=df.drop(columns="ref_area.label")
            print("ref_area",a)  
        except:
            try:
                df["pays"]=df["Country"]
                df=df.drop(columns="Country")
                print("Country",a)
                
            except:
                print("#############ERROR###########")
    try:
        a=df["year"].unique()
        print("year",a)
    except:
        df["year"]=df["time"]
        df=df.drop(columns="time")
    return df
def scinder_str(string):
    return(string.split(": "))
def colcible(df):
    for i in df.columns:
        if df[i].dtype=="float64" and i not in ["id","year"]:
            return i
    return None

def default_fixed(df, var_ouvertes=[]):
    for i in df.columns:
        try:
            if (i not in var_ouvertes) and (i not in ["year","pays"]) :
                l=df[i].unique()
                #print(l)
                a=1
                for j in l:
                    a=scinder_str(j)
                    #print(a)
                    if ("Total" in a) or ("Total" in a[1]) :
                        val_to_fix=j
                        a=0
                        print(j)
                        break
                    
                if a:
                    val_to_fix=l[0]
                df1=df[df[i]==val_to_fix]
                p=df1[i][df1[i].index[0]]
                df=df1        
        except:
            #print("##########",i,df[i][0])
            continue
    return(df)
def valeur_fixe(df, variables=[],values=[]):
    for i in range(len(variables)):
        df=df[df[variables[i]].isin(values[i])]
    return df
# Exemple de filtration des données
def filtrer_donne_sur_graphique(df,variables=[],valeurs=[],variable_ouverts=[],manquantes:bool=True):
    df1=valeur_fixe(df,variables,valeurs)
    df2=default_fixed(df1,var_ouvertes=variables+variable_ouverts)
    if manquantes:
        if list(df2["year"])==[]:
            return df2
        print(df2["year"].min())
        annees_completes = pd.DataFrame({"year": range(int(df2["year"].min()), int(df2["year"].max()) + 1)})
        df2 = pd.merge(annees_completes, df2, on="year", how="left")
    return df2

######################## Charger la base de donnees#############################

file_path = "https://raw.githubusercontent.com/User510991/Dashboard_App/main/Base_dv.xlsx"
feuille1 = pd.read_excel(file_path, sheet_name='V1')
feuille1=filtrer_donne_sur_graphique(arranger_data(feuille1))

####################### Configuration de la page #################################
# Sidebar
with st.sidebar:
    st.title('🏂 Emploi Afrique')

     # Accéder à la colonne 'year' sans parenthèses
    year_list = sorted(feuille1['year'].unique().tolist(), reverse=True)
    
    selected_year = st.selectbox('Selectionner une année', year_list, index=len(year_list)-1)
    
    #feuille1_selected_year = feuille1[feuille1.year == selected_year]
    #feuille1_selected_year_sorted = feuille1_selected_year.sort_values(by= "indicator.label", ascending=False)

    color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    selected_color_theme = st.selectbox('Selectionner une couleur', color_theme_list)


#######################     Heatmap #################################################################
# Heatmap
def make_heatmap(input_df, input_y, input_x, input_color, input_color_theme):
    heatmap = alt.Chart(input_df).mark_rect().encode(
            y=alt.Y(f'{input_y}:O', axis=alt.Axis(title="Year", titleFontSize=18, titlePadding=15, titleFontWeight=900, labelAngle=0)),
            x=alt.X(f'{input_x}:O', axis=alt.Axis(title="", titleFontSize=18, titlePadding=15, titleFontWeight=900)),
            color=alt.Color(f'max({input_color}):Q',
                             legend=None,
                             scale=alt.Scale(scheme=input_color_theme)),
            stroke=alt.value('red'),#modif ici de black
            strokeWidth=alt.value(0.25),
        ).properties(width=900
        ).configure_axis(
        labelFontSize=12,
        titleFontSize=12
        ) 
    # height=300
    return heatmap

######################################################## Choropleth map########################
def make_choropleth(input_df, input_id, input_column, input_color_theme):
    choropleth = px.choropleth(input_df, locations=input_id, color=input_column, locationmode="country names",
                               color_continuous_scale=input_color_theme,
                               range_color=(0, max(input_df[input_column])),
                               scope="africa",
                               labels={input_column: input_column}  # Étiquette pour la légende
                              )
    choropleth.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=400
    )
    return choropleth

##################################### Donut chart ################################################################

def make_donut(input_response, input_text, input_color):
  if input_color == 'blue':
      chart_color = ['#29b5e8', '#155F7A']
  if input_color == 'green':
      chart_color = ['#27AE60', '#12783D']
  if input_color == 'orange':
      chart_color = ['#F39C12', '#875A12']
  if input_color == 'red':
      chart_color = ['#E74C3C', '#781F16']
    
  source = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100-input_response, input_response]
  })
  source_bg = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100, 0]
  })
    
  plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          #domain=['A', 'B'],
                          domain=[input_text, ''],
                          # range=['#29b5e8', '#155F7A']),  # 31333F
                          range=chart_color),
                      legend=None),
  ).properties(width=130, height=130)
    
  text = plot.mark_text(align='center', color="#29b5e8", font="Lato", fontSize=32, fontWeight=700, fontStyle="italic").encode(text=alt.value(f'{input_response} %'))
  plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=40, cornerRadius=15).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          # domain=['A', 'B'],
                          domain=[input_text, ''],
                          range=chart_color),  # 31333F
                      legend=None),
  ).properties(width=130, height=130)# 130 et 130
  return plot_bg + plot + text

####################### Conception du Tableau de bord proprement dit ############################
#*********                                                                                       #
################################# Taux de croissance max et min ################################################
# Charger le fichier Excel
with st.sidebar:
    year_list = sorted(pd.read_excel(file_path, sheet_name='V17')['year'].unique().tolist(), reverse=True)
    #selected_year = st.selectbox('Select a year', year_list)

# Créer des colonnes pour l'affichage
col = st.columns((2, 6, 3), gap='medium')

with col[0]:
    st.markdown('#### PIB(%)')

    # Charger la feuille V17
    feuille17 = pd.read_excel(file_path, sheet_name='V17')
    feuille17=filtrer_donne_sur_graphique(arranger_data(feuille17))
    # Remplacer les valeurs manquantes par 0 dans la colonne PIB
    feuille17['PIB'] = feuille17['PIB'].fillna(0)

    if not feuille17.empty:
        # Filtrer les données pour l'année sélectionnée
        feuille17 = feuille17[feuille17['year'] == selected_year]

        if not feuille17.empty:
            # Trier les données par PIB
            feuille17 = feuille17.sort_values(by="PIB", ascending=False)

            # Trouver l'index du PIB maximum
            index_max_pib = feuille17['PIB'].idxmax()
            # Récupérer le pays correspondant au PIB maximum
            pays_max_pib = feuille17['pays'][index_max_pib]

            # Trouver l'index du PIB minimum
            index_min_pib = feuille17['PIB'].idxmin()
            # Récupérer le pays correspondant au PIB minimum
            pays_min_pib = feuille17['pays'][index_min_pib]

            # Calculer les valeurs max et min pour PIB
            max_pib = round(feuille17['PIB'].max(), 1)
            min_pib = round(feuille17['PIB'].min(), 1)

            # Afficher les résultats
            st.metric(label=f"{pays_max_pib} (Haut)", 
                       value=str(max_pib),
                       delta="Max")  # Flèche montante pour le max

            st.metric(label=f"{pays_min_pib} (Bas)", 
                       value=str(min_pib),
                       delta="-Min")  # Flèche descendante pour le min
        else:
            st.warning("Aucune donnée disponible pour l'année sélectionnée.")
    else:
        st.warning("La feuille de données est vide.")
####################### Situation du chomage en Afrique  ##########################################
with col[1]:
    st.markdown("#### Situation Chomage")
    feuille1_selected_year = feuille1[feuille1.year == selected_year]
    feuille1_selected_year_sorted = feuille1_selected_year.sort_values(by= "Taux_de_chômage", ascending=False)
    choropleth = make_choropleth(feuille1_selected_year, 'pays', 'Taux_de_chômage', selected_color_theme)
    st.plotly_chart(choropleth, use_container_width=True)

####################### Poids de l'informel en afrique ##########################################
    feuille3 = pd.read_excel(file_path, sheet_name='V3')
    feuille3=filtrer_donne_sur_graphique(arranger_data(feuille3))
    feuille3_selected_year = feuille3[feuille3.year == selected_year]
    feuille3_selected_year_sorted = feuille3_selected_year.sort_values(by= "Emploi_informel", ascending=False)
    st.markdown("#### Part de L'informel")
    heatmap = make_heatmap(feuille3_selected_year, 'year', 'pays', 'Emploi_informel', selected_color_theme)
    st.altair_chart(heatmap, use_container_width=True)
    
#Stats sur la proportion des jeunes de 15 a 24 ans sans emploi, mais qui ne frequentent pas ou suivent une formation  ####################################################################
feuille9 = pd.read_excel(file_path, sheet_name='V9')
feuille9=filtrer_donne_sur_graphique(arranger_data(feuille9))
feuille9_selected_year = feuille9[feuille9.year == selected_year]
feuille9_selected_year_sorted = feuille9_selected_year.sort_values(by= "Jeune_sans_emploi", ascending=False)
with col[2]:
    st.markdown("#### Jeunes inactifs")
    #st.markdown("#### des jeunes(15-24 ans)")
    st.dataframe(feuille9_selected_year_sorted,
                 column_order=("pays", "Jeune_sans_emploi"),
                 hide_index=True,
                 width=None,
                 column_config={  
                    "Pays": st.column_config.TextColumn(
                        "Pays",
                    ),
                    "Jeune_sans_emploi": st.column_config.ProgressColumn(
                        "Jeune_sans_emploi",
                        format="%f",
                        min_value=0,
                        max_value=max(feuille9_selected_year_sorted.Jeune_sans_emploi),
                     )}
                 )
