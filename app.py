import streamlit as st
import google.generativeai as genai
from PIL import Image

# Importation de la mémoire
try:
    from knowledge import INFO_STUDIO
except ImportError:
    INFO_STUDIO = "Erreur : Fichier knowledge.py introuvable."

st.set_page_config(page_title="Agent SVB Vision", page_icon="👁️", layout="centered")

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4825/4825038.png", width=50)
    st.title("SVB Manager")
    api_key = st.text_input("Clé API", type="password")
    
    if "Sèche-cheveux" in INFO_STUDIO:
        st.success("✅ Mémoire Studio Active")

# --- APP PRINCIPALE ---
if api_key:
    genai.configure(api_key=api_key.strip())
    # Le modèle Flash 2.5 est excellent pour voir les images !
    model = genai.GenerativeModel('gemini-2.5-flash')

    st.markdown("### 👁️ Assistant Visuel & Contenu")

    # 1. ZONE D'UPLOAD PHOTO
    with st.expander("📸 Ajouter une photo (Optionnel)", expanded=True):
        uploaded_file = st.file_uploader("Charge une photo du studio, d'une machine ou d'un exercice", type=["jpg", "jpeg", "png"])
        image_data = None
        if uploaded_file:
            image_data = Image.open(uploaded_file)
            st.image(image_data, caption="Analyse en cours...", use_container_width=True)

    # 2. CONFIGURATION
    col1, col2 = st.columns(2)
    with col1:
        action = st.selectbox("Action", ["Post Instagram (basé sur la photo)", "Analyse Posture/Correction", "Réponse Client", "Email Relance"])
    with col2:
        ton = st.selectbox("Ton", ["Motivant & Coach", "Bienveillant", "Technique & Expert", "Commercial"])

    contexte = st.text_area("Instructions supplémentaires :", placeholder="Ex: C'est le nouveau cours Crossformer, insiste sur l'intensité...", height=80)

    # 3. GÉNÉRATION
    if st.button("✨ Lancer l'analyse"):
        with st.spinner("L'IA observe et réfléchit..."):
            
            # Construction du prompt
            prompt_texte = f"""
            Tu es l'expert visuel et marketing du studio SVB.
            
            TA BIBLE (Infos Studio) :
            {INFO_STUDIO}
            
            TA MISSION :
            Action : {action}
            Ton : {ton}
            Contexte donné par l'humain : {contexte if contexte else "Décris ce que tu vois et vends-le !"}
            
            CONSIGNES VISUELLES :
            Si une image est fournie :
            1. Décris l'ambiance, la machine ou l'exercice que tu vois.
            2. Si c'est une posture, donne des corrections techniques bienveillantes.
            3. Si c'est une photo du studio, vends l'aspect "Premium / Small Group".
            """
            
            try:
                # Si on a une image, on envoie [Texte, Image] à l'IA
                if image_data:
                    inputs = [prompt_texte, image_data]
                else:
                    inputs = prompt_texte
                
                response = model.generate_content(inputs)
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Erreur : {e}")

else:
    st.info("⬅️ Connecte-toi avec ta clé API pour commencer.")
