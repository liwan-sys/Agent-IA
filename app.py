import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Debug Mode", page_icon="🐞")
st.title("🐞 Mode Débuggage")

# 1. On affiche la version installée pour comprendre le problème
try:
    import google.generativeai as genai
    version = genai.__version__
    st.info(f"ℹ️ Version du logiciel installée sur le serveur : {version}")
except:
    st.error("Le logiciel Google n'est pas installé du tout.")

# 2. Case pour la clé
api_key = st.text_input("Colle ta clé API", type="password")

if st.button("Lancer le test"):
    if not api_key:
        st.warning("Pas de clé !")
    else:
        try:
            genai.configure(api_key=api_key.strip())
            
            # --- LE CHANGEMENT EST ICI ---
            # On force le modèle 'gemini-pro' qui existe depuis longtemps
            # et on évite 'gemini-1.5-flash' qui plante chez toi.
            model = genai.GenerativeModel('gemini-pro')
            
            response = model.generate_content("Dis juste le mot : SUCCÈS")
            st.success("✅ ÇA MARCHE ENFIN !")
            st.write(response.text)
            
        except Exception as e:
            st.error("❌ Toujours une erreur...")
            st.code(e) # Affiche l'erreur exacte pour que je puisse la lire
