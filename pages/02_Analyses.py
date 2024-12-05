import pandas as pd
import numpy as np
#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
from theme_utils import apply_theme



#import plotly.io as pio

# Définir le thème par défaut
#pio.templates.default = "plotly_dark"

# Page configuration
st.set_page_config(
    page_title="Tableau de Bord Afrique",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")
#alt.themes.enable("dark")
# Appliquer le thème global
chart_template = apply_theme()
#######################


st.title("Section sur les graphiques utilisés")
st.markdown("""
## Description du tableau de bord
Ce tableau de bord montre en ordre, les illustrations utilisées pour résoudre notre tématique. 
- Pour voir Les graphiques en plien écran, cliquer sur le carrée [ ] en haut à droite de l'illustration.
- Si vous vous interesser à l'illustration d'une catégorie spécifique mentionné dans la légende, double-cliquer dessus sur la légende
""")

# Charger le fichier Excel
fichier_excel ="https://raw.githubusercontent.com/User510991/Dashboard_App/refs/heads/main/5_Base_dv.xlsx"#"c:\Users\REYDEYSCHIAS\Desktop\Base_dv.xlsx"#"e:\0_ISSEA_Formation\Dashboard Apps_contest\Final_Base_Emploi_Insertion.xlsx"#"e:\0_ISSEA_Formation\Dashboard Apps_contest\Final_Base_Emploi_Insertion.xlsx"#"e:\0_ISSEA_Formation\Dashboard Apps_contest\Final_Def_Base_Emploi_Insertion.xlsx""c:\Users\REYDEYSCHIAS\Desktop\Base_dv.xlsx"#
# Utiliser ExcelFile pour accéder aux métadonnées du fichier
excel = pd.ExcelFile(fichier_excel)

# Liste des feuilles
feuilles = excel.sheet_names


with st.sidebar:
    st.title('Emploi Afrique')
    
###############################Traitement####################
dict_data={}

liste_variable=[]
for i in feuilles:
    dict_data[i] = pd.read_excel(fichier_excel, sheet_name=i)
    liste_variable.append(dict_data[i].iloc[0,0])

for i in range(len(feuilles)):
    df=dict_data[feuilles[i]]
    try:
        a=df["pays"].unique()
        print(feuilles[i],"pays")
    except:
        try:
            df["pays"]=df["ref_area.label"]
            df=df.drop(columns="ref_area.label")
            print(feuilles[i],"ref_area")
            dict_data[feuilles[i]]=df
            
        except:
            try:
                df["pays"]=df["Country"]
                
                df=df.drop(columns="Country")
                print(feuilles[i],"Country")
                dict_data[feuilles[i]]=df
            except:
                print(feuilles[i],"#############ERROR###########")
    #dict_df[liste_variable[i]]=df

#dict_df={}
for i in range(len(feuilles)):
    if i==0:
        #dict_df[liste_variable[i]]=df
        continue
    df=dict_data[feuilles[i]]
    try:
        a=df["year"].unique()
        print(feuilles[i],"year")
    except:
        df["year"]=df["time"]
        df=df.drop(columns="time")
        print(feuilles[i],"time")
        dict_data[feuilles[i]]=df

def scinder_str(string):
    return(string.split(": "))

def colcible(df):
    for i in df.columns:
        if df[i].dtype=="float64" and i not in ["id","year"]:
            return i
    return None

def aggregate_on_column(df, agg_column, agg_func="mean"):
    """
    Agrège les données sur une colonne donnée, en conservant les autres colonnes distinctes.

    :param df: DataFrame pandas
    :param agg_column: Colonne à agréger
    :param agg_func: Fonction d'agrégation (sum, mean, etc.)
    :return: DataFrame agrégé
    """
    # Identifier les colonnes sur lesquelles regrouper (toutes sauf la colonne à agréger)
    group_columns = [col for col in df.columns if col != agg_column]
    
    # Effectuer l'agrégation
    aggregated_df = df.groupby(group_columns, as_index=False).agg({agg_column: agg_func})
    
    return aggregated_df
def Ajout_regions(df,func="mean"):
    cible=colcible(df)
    df2=aggregate_on_column(df.drop(columns='pays'),cible,agg_func=func)
    df2["pays"]=df2["Region"]
    df2["Region"]="Afrique_RegionSeul"
    df3=aggregate_on_column(df.drop(columns=['pays',"Region"]),cible,agg_func=func)
    df3["pays"]="Afrique(All)"#df4["Region"]
    df3["Region"]="Afrique_Seul"
    df4=pd.concat([df,df2,df3],ignore_index=True)
    return df4
operation={}
for i in liste_variable[1:]:
    if 'milliers' in i:
        operation[i]='sum'
    else:
        operation[i]='mean'
dict_df={liste_variable[0]:dict_data[feuilles[0]]}
for i in range(1,len(feuilles)):
    #cible=colcible()
    dict_data[feuilles[i]]=Ajout_regions(dict_data[feuilles[i]],func=operation[liste_variable[i]])
    dict_df[liste_variable[i]]=dict_data[feuilles[i]]

def default_fixed(df, var_ouvertes=[]):
    for i in df.columns:
        try:
            if (i not in var_ouvertes) and (i not in ["year","pays","Region"]) :
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
            elif (i in ["pays","Region"]) and (i not in var_ouvertes):
                if (i=='pays') and ("Region" not in var_ouvertes):
                    val_to_fix="Afrique(All)"
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
def select_region(region:str):
    df=dict_data[feuilles[1]]
    return list(df[df["Region"]==region]["pays"])
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
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def generer_palette_couleur(color_variable):
    palette = px.colors.qualitative.Set1  # Palette prédefinie
    unique_categories = list(set(color_variable))  # Identifier les catégories uniques
    category_colors = {cat: palette[i % len(palette)] for i, cat in enumerate(unique_categories)}  # Assigner des couleurs
    marker_colors = [category_colors[cat] for cat in color_variable]
    return(marker_colors,category_colors)
#generer_palette_couleur(df["pays"])
def tracer_ligne(data,variable,couleurs,Alltitle=None,Xtitle=None,Ytitle=None):
    
    df=data
    var_x=variable
    var_y=colcible(df)
    
    if Alltitle ==None:
        Alltitle=str(df["indicator.label"][0]).split("par ")[0]
    if Xtitle==None:
        Xtitle=var_x
    if Ytitle==None:
        Ytitle=str(df["indicator.label"][0]).split("par ")[0]
    
    if type(couleurs)==list:
        color="-".join(couleurs)
        if len(couleurs)>1:
            df[color]= df[couleurs].astype(str).agg('-'.join, axis=1)
    else:
        color=couleurs
    
    fig = px.line(df, x=var_x, y=var_y, 
                title=str(df.iloc[1,0]),
                color=color,
                color_discrete_map=generer_palette_couleur(df[color])[1],
                )
    # Ajout des points (scatter plot)
    fig.add_trace(go.Scatter(
        x=df[var_x],
        y=df[var_y],
        mode='markers',
        name='Valeurs',
        marker=dict(size=5, color=generer_palette_couleur(df[color])[0])
    ))

    # Mise à jour du layout
    fig.update_layout(
        title=Alltitle,
        xaxis_title=Xtitle,
        yaxis_title=Ytitle,
        legend_title="Légende",
        xaxis=dict(
        rangeslider=dict(visible=True)),
    )
    return fig

def plot_stacked_bar_100(df, x, y, color1, facet=None, mode="stack",Alltitle=None,Xtitle=None,Ytitle=None):
    """
    Crée un diagramme en barres empilées normalisé à 100%.

    :param df: DataFrame contenant les données.
    :param x: Colonne pour l'axe x (groupes).
    :param y: Colonne pour les valeurs.
    :param color: Colonne pour les catégories (couleurs).
    :param title: Titre du graphique.
    """
    if Alltitle ==None:
        Alltitle=str(df["indicator.label"][0]).split("par ")[0]
    if Xtitle==None:
        Xtitle=x
    if Ytitle==None:
        Ytitle="Proportion"#
    
        # Jointure des colonnes avec un séparateur (par exemple, un tiret '-')
    if type(color1)==list:
        color="-".join(color1)
        if len(color1)>1:
            df[color]= df[color1].astype(str).agg('-'.join, axis=1)
    else:
        color=color1
    listg=[x]
    if not facet==None:
        listg.append(facet)
    # Normalisation des données à 100%
    df["Proportions"] = df[y] / df.groupby(listg)[y].transform("sum") * 100

    # Création du graphique
    fig = px.bar(
        df,
        x=x,
        y="Proportions",
        color=color,
        facet_col=facet,
        barmode=mode,
        #text="Proportions",  # Affiche les proportions sur les barres
    )
    fig.update_layout(
        title=Alltitle,
        xaxis_title=Xtitle,
        yaxis_title=Ytitle,
        legend_title="Légende",
    )
    fig.update_layout(
    xaxis=dict(
        tickmode='linear',  # Affiche tous les groupes
        showgrid=True,  # Supprime la grille pour plus de lisibilité
        #tickangle=-45,  # Incline les labels des groupes
        #automargin=True  # Gère automatiquement l'espace pour les labels
        rangeslider=dict(visible=True)
    ),
    bargap=0.5  # Réduit l'espacement entre les groupes pour qu'ils rentrent tous
)
    # Options de mise en forme
    #fig.update_traces(texttemplate="%{text:.1f}%", textposition="inside")
    #fig.update_layout(barmode="stack", yaxis=dict(title="Pourcentage (%)", ticksuffix="%"))
    return fig
def plot_stacked_barlinear(df, x, y, color1,facet=None, mode="stack",Alltitle=None,Xtitle=None,Ytitle=None):
    """
    Crée un diagramme en barres empilées normalisé à 100%.

    :param df: DataFrame contenant les données.
    :param x: Colonne pour l'axe x (groupes).
    :param y: Colonne pour les valeurs.
    :param color: Colonne pour les catégories (couleurs).
    :param title: Titre du graphique.
    """
    if Alltitle ==None:
        Alltitle=str(df["indicator.label"][0]).split("par ")[0]
    if Xtitle==None:
        Xtitle=x
    if Ytitle==None:
        Ytitle=str(df["indicator.label"][0]).split("par ")[0]#'Proportions'
    # Jointure des colonnes avec un séparateur (par exemple, un tiret '-')
    if type(color1)==list:
        color="-".join(color1)
        if len(color1)>1:
            df[color]= df[color1].astype(str).agg('-'.join, axis=1)
    else:
        color=color1
    # Création du graphique
    fig = px.bar(
        df,
        x=x,
        y=y,
        facet_col=facet,
        color=color,
        title=str(df["indicator.label"][0]),
        barmode=mode,
        labels=str(df["indicator.label"][0])
        #labels={"Proportions": "Pourcentage (%)"},
        #text="Proportions",  # Affiche les proportions sur les barres
    )
    
    fig.update_layout(
        title=Alltitle,
        xaxis_title=Xtitle,
        yaxis_title=Ytitle,
        legend_title="Légende",
    )
    fig.update_layout(
    xaxis=dict(
        tickmode='linear',  # Affiche tous les groupes
        showgrid=True,  # Supprime la grille pour plus de lisibilité
        #tickangle=-45,  # Incline les labels des groupes
        #automargin=True  # Gère automatiquement l'espace pour les labels
        rangeslider=dict(visible=True)
    ),
    bargap=0.5  # Réduit l'espacement entre les groupes pour qu'ils rentrent tous
)
    # Options de mise en forme
    #fig.update_traces(texttemplate="%{text:.1f}%", textposition="inside")
    #fig.update_layout(barmode="stack", yaxis=dict(title=f"{str(df.iloc[1,0])}", ticksuffix="%"))
    return fig
def tracer_bar(df,var_x,var_y,var_couleur,facet=None,type=1,typemode=0,Alltitle=None,Xtitle=None,Ytitle=None):
    liste_mode=["stack","group"]
    if type:
        return plot_stacked_bar_100(df,var_x,var_y,var_couleur,facet=facet,mode=liste_mode[typemode],Alltitle=Alltitle,Xtitle=Xtitle,Ytitle=Ytitle)
    else:
        return plot_stacked_barlinear(df,var_x,var_y,var_couleur,facet=facet,mode=liste_mode[typemode],Alltitle=Alltitle,Xtitle=Xtitle,Ytitle=Ytitle)
    
#tracer_bar(df,"year","obs_value","pays",1)

def nuage(df1,df2,var_x,var_y,color1=None,Alltitle=None,Xtitle=None,Ytitle=None):
    # Tracer un nuage de points
    if Alltitle ==None:
        Alltitle=f'{str(df1["indicator.label"][0]).split("par")[0]} & {str(df2["indicator.label"][0]).split("par")[0]}'
    if Xtitle==None:
        Xtitle=str(df1["indicator.label"][0]).split("par")[0]
    if Ytitle==None:
        Ytitle=str(df2["indicator.label"][0]).split("par")[0]
    
    if type(color1)==list:
        color="-".join(color1)
        if len(color1)>1:
            df1[color]= df.astype(str).agg('-'.join, axis=1)
            df2[color]= df.astype(str).agg('-'.join, axis=1)
    else:
        color=color1
    
    
    df_merged = pd.merge(df1, df2, on=["year", "pays","Region"], how="inner")

    
    fig = px.scatter(
        df_merged,
        x=var_x,                # Axe des x
        y=var_y,                # Axe des y
        color=color,    # Catégories pour la couleur des points
        title=f"Nuage de Points entre {str(df1['indicator.label'][0])} et {str(df2['indicator.label'])}",
        #labels={"x": str(df1["indicator.label"][0]), "y": str(df2["indicator.label"])},  # Personnalisation des labels des axes
    )
    fig.update_layout(
        title=Alltitle,
        xaxis_title=Xtitle,
        yaxis_title=Ytitle,
        legend_title="Légende",
    )
    fig.update_layout(
    xaxis=dict(
        tickmode='linear',  # Affiche tous les groupes
        showgrid=True,  # Supprime la grille pour plus de lisibilité
        #tickangle=-45,  # Incline les labels des groupes
        #automargin=True  # Gère automatiquement l'espace pour les labels
        rangeslider=dict(visible=True)
    ),
    )
    return fig

#################################GRAPHIQUES########################################################

col = st.columns(1, gap='medium')
with col[0]:
    df1=filtrer_donne_sur_graphique(dict_data["V20"],variables=["pays"],valeurs=[['Central Africa', 'East Africa', 'West Africa', 'Southern Africa','North Africa','Afrique(All)']])#,variable_ouverts=["sex.label"])
    st.plotly_chart(tracer_ligne(df1,"year","pays"))
    df1=filtrer_donne_sur_graphique(dict_data["V18"],variables=["pays","year"],valeurs=[['Central Africa', 'East Africa', 'West Africa', 'Southern Africa','North Africa'],list(range(2018,2024))])#,variable_ouverts=["sex.label"])
    st.plotly_chart(tracer_bar(df1,"year",colcible(df1),"pays",type=0,typemode=1))
    df1=filtrer_donne_sur_graphique(dict_data["V18"],variables=["Region","year"],valeurs=[['West Africa'],[2022]])#,variable_ouverts=["sex.label"])
    st.plotly_chart(tracer_bar(df1,"pays",colcible(df1),var_couleur=None,type=0,typemode=1))
    #Comparaison des salaires horaires moyens par sexe.
    df1=filtrer_donne_sur_graphique(dict_data["V18"],variables=["classif2.label","classif1.label","pays","year"],valeurs=[['Institutional sector: Public',
        'Institutional sector: Private',
        'Institutional sector: Not elsewhere classified'],['Age (Aggregate bands): 15-24',
        'Age (Aggregate bands): 25-54', 'Age (Aggregate bands): 55-64',
        'Age (Aggregate bands): 65+'],["Nigeria"],[2022]])
    st.plotly_chart(tracer_bar(df1,"classif2.label",colcible(df1),"classif1.label"))
    #SExe
    df1=filtrer_donne_sur_graphique(dict_data["V1"],variable_ouverts=["sex.label"])
    st.plotly_chart(tracer_ligne(df1,"year","sex.label"))
    #Age
    df1=filtrer_donne_sur_graphique(dict_data["V1"],variables=["pays","year"],valeurs=[['Central Africa', 'East Africa', 'West Africa', 'Southern Africa','North Africa'],list(range(2021,2024))])
    st.plotly_chart(tracer_ligne(df1,"year","pays"))#"classif1.label")
    df1=filtrer_donne_sur_graphique(dict_data["V1"],variables=["Region","year"],valeurs=[['Southern Africa'],[2021]])
    st.plotly_chart(tracer_bar(df1,"pays",colcible(df1),var_couleur=None,type=0))
    df1=filtrer_donne_sur_graphique(dict_data["V1"],variables=["pays","year","sex.label",'classif1.label'],valeurs=[['South Africa'],[2021],['Sex: Male', 'Sex: Female'],['Age (Youth, adults): 15-24','Age (Youth, adults): 25+']])
    st.plotly_chart(tracer_bar(df1,"sex.label",colcible(df1),var_couleur='classif1.label',type=0,typemode=1))
    df1=filtrer_donne_sur_graphique(dict_data["V3"],variables=["pays","year"],valeurs=[['Central Africa', 'East Africa', 'West Africa', 'Southern Africa','North Africa'],list(range(2021,2024))])
    st.plotly_chart(tracer_ligne(df1,"year","pays"))
    df1=filtrer_donne_sur_graphique(dict_data["V3"],variables=["Region","year"],valeurs=[['West Africa'],[2023]])
    st.plotly_chart(tracer_bar(df1,"pays",colcible(df1),var_couleur=None,type=0))
    df1=filtrer_donne_sur_graphique(dict_data["V3"],variables=["pays","year","sex.label"],valeurs=[['Burkina Faso'],[2023],['Sex: Male', 'Sex: Female']])
    st.plotly_chart(tracer_bar(df1,"sex.label",colcible(df1),var_couleur=None,type=0,typemode=1))
    #Proportion des femmes occupant des postes d'encadrement Sup et Intermdiaire
    df1=filtrer_donne_sur_graphique(dict_data["V6"],variables=["pays"],valeurs=[['Central Africa', 'East Africa', 'West Africa', 'Southern Africa','North Africa','Afrique(All)']])
    st.plotly_chart(tracer_ligne(df1,"year","pays"))
    df1=filtrer_donne_sur_graphique(dict_data["V17"],variable_ouverts=["sex.label"])
    st.plotly_chart(tracer_ligne(df1,"year","sex.label"))
    #Taux de participation des jeunes à l'apprentissage par le travail.
    df1=filtrer_donne_sur_graphique(dict_data["V5"],variables=["pays",'year'],valeurs=[['Central Africa', 'East Africa', 'West Africa', 'Southern Africa','North Africa','Afrique(All)'],[2016,2017,2018]])#,variable_ouverts=["sex.label"])
    st.plotly_chart(tracer_bar(df1,"year",colcible(df1),'pays',typemode=1,type=0))
#with col[1]:
    

    df1=filtrer_donne_sur_graphique(dict_data['V20'],variables=['Region'],valeurs=[['Central Africa', 'East Africa', 'West Africa', 'Southern Africa']])
    df2=filtrer_donne_sur_graphique(dict_data['V1'],variables=['Region'],valeurs=[['Central Africa', 'East Africa', 'West Africa', 'Southern Africa']])
    st.plotly_chart(nuage(df1,df2,colcible(df1)+"_x",colcible(df2)+"_y","Region"))
    
#with col[1]:
    #Comparaison des salaires horaires moyens par sexe.
    
    #Analyse du taux d'emploi informel, mettant en évidence les disparités entreles sexes.
    #df1=filtrer_donne_sur_graphique(dict_data["V3"],variables=["sex.label"],)
    #tracer_ligne(df1,"year","sex.label")
    
    #Proportion de jeunes ne suivant pas d'études, d'emploi ou de formation
    df1=filtrer_donne_sur_graphique(dict_data["V9"],variables=["pays"],valeurs=[['Central Africa', 'East Africa', 'West Africa', 'Southern Africa','North Africa','Afrique(All)']])#,variable_ouverts=["sex.label"])
    st.plotly_chart(tracer_ligne(df1,"year","pays"))
    df1=filtrer_donne_sur_graphique(dict_data["V19"],variables=["pays"],valeurs=[['Central Africa', 'East Africa', 'West Africa', 'Southern Africa','North Africa','Afrique(All)']])#,variable_ouverts=["sex.label"])
    st.plotly_chart(tracer_ligne(df1,"year","pays"))
#with col[3]:
    df1=filtrer_donne_sur_graphique(dict_data["V10"],variables=["pays"],valeurs=[['Central Africa', 'East Africa', 'West Africa', 'Southern Africa','North Africa','Afrique(All)']])#,variable_ouverts=["sex.label"])
    st.plotly_chart(tracer_ligne(df1,"year","pays"))
    df1=filtrer_donne_sur_graphique(dict_data["V5"],variables=["pays","year"],valeurs=[['Central Africa', 'East Africa', 'West Africa', 'Southern Africa','North Africa','Afrique(All)'],list(range(2000,2024))])#,variable_ouverts=["sex.label"])
    st.plotly_chart(tracer_ligne(df1,"year","pays"))
    df1=filtrer_donne_sur_graphique(dict_data["V11"],variables=["pays","year"],valeurs=[['Central Africa', 'East Africa', 'West Africa', 'Southern Africa','North Africa'],list(range(2018,2024))])#,variable_ouverts=["sex.label"])
    st.plotly_chart(tracer_bar(df1,"year",colcible(df1),"pays",type=0,typemode=1))

    df1=filtrer_donne_sur_graphique(dict_data['V20'],variables=['Region'],valeurs=[['Central Africa', 'East Africa', 'West Africa', 'Southern Africa']])
    df2=filtrer_donne_sur_graphique(dict_data['V1'],variables=['Region'],valeurs=[['Central Africa', 'East Africa', 'West Africa', 'Southern Africa']])
    st.plotly_chart(nuage(df1,df2,colcible(df1)+"_x",colcible(df2)+"_y","pays"))
#####################################################################################################

#####################################################################################################
