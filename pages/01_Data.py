import streamlit as st
# Appliquer le thème global
chart_template = apply_theme()
st.subheader("Visualisation de la base de données")

import pandas as pd
import streamlit as st

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


# Chemin d'accès au fichier Excel
file_path = "https://raw.githubusercontent.com/User510991/Dashboard_App/main/Base_dv.xlsx"

# Charger le classeur Excel pour obtenir les noms des feuilles
xls = pd.ExcelFile(file_path)
sheet_names = xls.sheet_names  # Liste des noms de feuilles

variables_names=[' Taux de chômage (%)', 
                 "Taux d'activité par sexe, âge et état civil (%)", 
                 "Taux d'emploi informel par sexe (%)", 
                 "Emploi par sexe, âge et niveau d'études (en milliers)", 
                 "Taux de participation des jeunes à l'apprentissage par le travail, par sexe et par type (pour 1000 personnes)", 
                 "Proportion de femmes occupant des postes d'encadrement supérieur et intermédiaire (%)", 
                 'Informal employment rate by sex, age and marital status (%)', 
                 'Emploi par sexe, âge et situation de handicap (en milliers)', 
                 "Proportion de jeunes (âgés de 15 à 24 ans) ne suivant pas d'études, d'emploi ou de formation", 
                 'Taux de croissance annuel de la production par travailleur (PIB en dollars internationaux constants de 2017 à PPA) (%)', 
                 "Emploi par sexe, âge et statut dans l'emploi (en milliers)", 
                 "Taux d'activité de la population active la main-d’œuvre par sexe, type de ménage et zone rurale/urbaine (%)", 
                 "Emploi par sexe et par taille d'établissement (en milliers)", 
                 'Proportion de la population couverte par des socles/systèmes de protection sociale (%)', 
                 'Salaire horaire moyen des employés par sexe (monnaie locale)', 
                 'Emploi par sexe, âge et secteur public/privé (milliers)', 
                'Croissance du PIB (%) annuel']

# Titre de l'application
st.title("Visualisation des Données Excel")

# Sélecteur de feuille
selected_sheet = st.selectbox("Choisissez une feuille :", variables_names)
p=variables_names.index(selected_sheet)
# Charger les données de la feuille sélectionnée
data = pd.read_excel(file_path, sheet_name=sheet_names[p])

# Afficher les données
st.write(f"Données de la feuille : {selected_sheet}")
st.dataframe(data)  # Affiche les données sous forme de tableau

# Optionnel : Afficher des statistiques descriptives
data1=filtrer_donne_sur_graphique(arranger_data(data))
if st.checkbox("Quelques statistiques descriptives"):
    st.write(data1.describe())
