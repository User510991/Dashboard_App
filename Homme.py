import streamlit as st

# Définir le titre de la page
st.set_page_config(
    page_title="Home",  # Titre affiché dans l'onglet du navigateur
)

def main():
    st.header("BIENVENNUE SUR NOTRE ESPACE DE VISUALISATION DES DONNEES")
    st.title("Cette page vous donne la possibilite de naviguer entre la visualisation des donnees, les stats desc et le tableau de bord")

if __name__ == '__main__':
    main()
