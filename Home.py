import streamlit as st

# Initialisation de la session pour le thème global
from theme_utils import apply_theme

# Interface utilisateur pour choisir le thème global
if "theme" not in st.session_state:
    st.session_state["theme"] = "Clair"  # Thème par défaut

st.title("Bienvenue dans l'application avec Thèmes Dynamiques")

# Appliquer le thème
chart_template = apply_theme()
def main():
    st.header("BIENVENNUE SUR NOTRE ESPACE DE VISUALISATION DES DONNEES")
    st.title("Cette page vous donne la possibilite de naviguer entre la visualisation des donnees, les stats desc et le tableau de bord")

if __name__ == '__main__':
    main()
