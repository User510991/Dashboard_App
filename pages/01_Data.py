import streamlit as st

st.subheader("Visualisation de la base de données")

import pandas as pd
import streamlit as st

# Chemin d'accès au fichier Excel
file_path = r"C:\Users\djetek_user\Desktop\ISE 3\DSM\Base_dv.xlsx"

# Charger le classeur Excel pour obtenir les noms des feuilles
xls = pd.ExcelFile(file_path)
sheet_names = xls.sheet_names  # Liste des noms de feuilles

# Titre de l'application
st.title("Visualisation des Données Excel")

# Sélecteur de feuille
selected_sheet = st.selectbox("Choisissez une feuille :", sheet_names)

# Charger les données de la feuille sélectionnée
data = pd.read_excel(file_path, sheet_name=selected_sheet)

# Afficher les données
st.write(f"Données de la feuille : {selected_sheet}")
st.dataframe(data)  # Affiche les données sous forme de tableau

# Optionnel : Afficher des statistiques descriptives
if st.checkbox("Quelques statistiques descriptives"):
    st.write(data.describe())