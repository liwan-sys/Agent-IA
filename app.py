import streamlit as st
import google.generativeai as genai

# Configuration de la page
st.set_page_config(page_title="Coach IA Hub", page_icon="💪")
st.title("🏋️‍♂️ Mon Assistant Studio Coaching")

# Barre latérale
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Clé API Gemini", type="password")

if api_key:
    try:
        # 1. Configuration de l'API
        genai.configure(api_key=api_key.strip())
        
        # 2. Le modèle STANDARD (celui qui marche à 100%)
        model = genai.GenerativeModel('gemini-pro')

        # 3. Interface utilisateur
        option = st.selectbox("Action", ["Post Instagram", "Script de Reel", "Réponse Client"])
        sujet = st.text_area("Sujet du contenu", "")

        if st.button("Générer"):
            if not sujet:
                st.warning("Écris un sujet d'abord !")
            else:
                with st.spinner('L\'IA réfléchit...'):
                    # Le prompt
                    prompt = f"Agis comme un coach sportif expert. Crée un contenu pour : {option}. Sujet : {sujet}. Ton motivant."
                    
                    # Génération
                    response = model.generate_content(prompt)
                    
                    # Affichage
                    st.success("Voici le résultat :")
                    st.write(response.text)

    except Exception as e:
        # Gestion propre des erreurs
        st.error(f"Une erreur est survenue : {e}")
        st.info("Vérifie que ta clé API est correcte et qu'elle n'a pas d'espace au début ou à la fin.")

else:
    st.warning("⬅️ Entre ta clé API dans la barre latérale pour commencer.")