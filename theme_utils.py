import streamlit as st

def apply_theme():
    """Appliquer le thème basé sur le choix stocké dans la session."""
    if "theme" not in st.session_state:
        st.session_state["theme"] = "Clair"  # Thème par défaut

    if st.session_state["theme"] == "Clair":
        st.markdown(
            """
            <style>
            body {
                background-color: white;
                color: black;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        return "plotly"  # Thème clair pour les graphiques
    else:
        st.markdown(
            """
            <style>
            body {
                background-color: #0e1117;
                color: white;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        return "plotly_dark"  # Thème sombre pour les graphiques
