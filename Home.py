import streamlit as st

# Initialisation de la session pour le thème global
if "theme" not in st.session_state:
    st.session_state["theme"] = "Clair"  # Thème par défaut

# Page principale pour choisir le thème
st.title("Choix du thème global")

theme = st.radio(
    "Choisissez un thème global :",
    ("Clair", "Sombre"),
    index=0 if st.session_state["theme"] == "Clair" else 1
)
def main():
    st.header("BIENVENNUE SUR NOTRE ESPACE DE VISUALISATION DES DONNEES")
    st.title("Cette page vous donne la possibilite de naviguer entre la visualisation des donnees, les stats desc et le tableau de bord")

if __name__ == '__main__':
    main()
