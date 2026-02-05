import streamlit as st
import google.generativeai as genai

st.title("🚀 Test Final de Connexion")

# Champ pour la clé
api_key = st.text_input("Colle ta NOUVELLE clé API ici", type="password")

if st.button("Lancer le test"):
    if not api_key:
        st.warning("⚠️ Il faut coller la clé d'abord !")
    else:
        st.info("1. Clé reçue, configuration en cours...")
        
        try:
            # On nettoie la clé et on configure
            genai.configure(api_key=api_key.strip())
            
            st.info("2. Envoi du message à Gemini (ça peut prendre 5-10 sec)...")
            
            # On utilise le modèle le plus fiable
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content("Réponds juste par : BRAVO CA MARCHE")
            
            st.success("✅ VICTOIRE ! Connexion réussie.")
            st.header(response.text)
            
        except Exception as e:
            st.error("❌ Échec de la connexion.")
            st.write(f"Détail de l'erreur : {e}")
            st.info("Conseil : Vérifie que tu as bien copié toute la clé (elle commence souvent par 'AIza...')")
