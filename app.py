import streamlit as st
import google.generativeai as genai

# --- IMPORTATION DE LA MÉMOIRE ---
try:
    from knowledge import INFO_STUDIO
except ImportError:
    INFO_STUDIO = "Erreur : Fichier knowledge.py introuvable."

# --- CONFIGURATION ---
st.set_page_config(page_title="Agent SVB", page_icon="💪", layout="centered")
st.title("💪 Agent SVB - Santez-Vous Bien")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Connexion")
    api_key = st.text_input("Clé API", type="password")
    
    # Indicateur visuel
    if "SVB" in INFO_STUDIO:
        st.success("✅ Données SVB chargées")
    else:
        st.error("⚠️ Données manquantes")

# --- APP PRINCIPALE ---
if api_key:
    genai.configure(api_key=api_key.strip())
    # On garde le modèle qui marche chez toi
    model = genai.GenerativeModel('gemini-2.5-flash')

    col1, col2 = st.columns(2)
    with col1:
        action = st.selectbox("Action", ["Réponse WhatsApp/DM", "Post Instagram", "Script Vidéo", "Email Relance"])
    with col2:
        ton = st.selectbox("Ton", ["Bienveillant & Pro", "Dynamique & Coach", "Direct & Vendeur"])

    contexte = st.text_area("Question du client ou Sujet du post :", height=100)

    if st.button("Générer la réponse"):
        if not contexte:
            st.warning("Écris quelque chose d'abord !")
        else:
            with st.spinner("Consultation des règles du studio..."):
                prompt = f"""
                Tu es l'assistant virtuel expert du studio SVB (Santez-Vous Bien).
                
                SOURCE DE VÉRITÉ (Tes connaissances) :
                {INFO_STUDIO}
                
                TA MISSION :
                Type de contenu : {action}
                Ton : {ton}
                Sujet / Question : {contexte}
                
                RÈGLES CRUCIALES :
                1. Si on parle de prix, sois précis au centime près selon la grille.
                2. Si la question porte sur un retard, rappelle gentiment mais fermement la règle des 5 min.
                3. Pousse toujours l'offre "Pass Starter" aux débutants.
                4. N'invente jamais d'offre qui n'est pas dans la liste.
                """
                
                response = model.generate_content(prompt)
                st.markdown(response.text)
