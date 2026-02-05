import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Coach IA Hub", page_icon="💪")
st.title("🏋️‍♂️ Mon Assistant Studio Coaching")

# Barre latérale
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Clé API Gemini", type="password")

if api_key:
    # On ouvre le bloc de sécurité (try)
    try:
        # Configuration de l'API
        genai.configure(api_key=api_key.strip())
        
        # CORRECTION ICI : On utilise le modèle standard gemini-pro
        model = genai.GenerativeModel('gemini-pro')

        # L'interface
        option = st.selectbox("Action", ["Post Instagram", "Script de Reel", "Réponse Client"])
        sujet = st.text_area("Sujet du contenu", "")

        if st.button("Générer"):
            if not sujet:
                st.warning("Écris un sujet d'abord !")
            else:
                with st.spinner('L\'IA réfléchit...'):
                    prompt = f"Agis comme un coach sportif expert. Crée un contenu pour : {option}. Sujet : {sujet}. Ton motivant."
                    response = model.generate_content(prompt)
                    st.success("Voici le résultat :")
                    st.write(response.text)

    # Voici le bloc 'except' qui manquait ou était mal placé
    except Exception as e:
        st.error(f"Une erreur est survenue : {e}")
        st.info("Vérifie que ta clé API est correcte.")

else:
    st.warning("⬅️ Entre ta clé API dans la barre latérale pour commencer.")