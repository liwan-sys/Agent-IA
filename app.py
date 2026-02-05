import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. IMPORTATION MÉMOIRE ---
try:
    from knowledge import INFO_STUDIO
except ImportError:
    INFO_STUDIO = "Erreur : Fichier knowledge.py introuvable."

st.set_page_config(page_title="SVB Manager DA", page_icon="🍑", layout="wide")

# --- 2. GESTION CLÉ (Auto ou Manuel) ---
api_key = None
try:
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
except:
    pass

# --- SIDEBAR ---
with st.sidebar:
    st.title("🍑 SVB Manager")
    st.caption("Direction Artistique : Active")
    st.markdown("---")
    
    if api_key:
        st.success("🔑 Clé connectée")
    else:
        st.warning("Mode manuel")
        api_key = st.text_input("Colle ta clé API", type="password")

# --- 3. FONCTIONS INTELLIGENTES ---
def generate_content(prompt_type, context, creative_level="Normal"):
    if not api_key:
        st.error("Besoin de la clé API !")
        return

    try:
        genai.configure(api_key=api_key.strip())
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        with st.spinner(f"🎨 Création en cours ({prompt_type})..."):
            prompt = f"""
            Tu es le Directeur Artistique et Marketing du studio SVB.
            
            TA BIBLE (DA & OFFRES) :
            {INFO_STUDIO}
            
            TA MISSION :
            Type : {prompt_type}
            Niveau de créativité : {creative_level}
            Contexte : {context}
            
            CONSIGNES VISUELLES IMPÉRATIVES (DA) :
            - Utilise un vocabulaire "Organique", "Fluide", "Cocon", "Premium".
            - Si tu suggères des émojis, utilise la palette : 🍑, 🌿, 🍦, 🌾, ✨.
            - Bannis les termes agressifs ("No Pain No Gain", "Guerre"). Préfère "Flow", "Ancrage", "Sculpter".
            """
            
            response = model.generate_content(prompt)
            st.markdown("---")
            st.markdown(response.text)
            st.success("C'est prêt !")

    except Exception as e:
        st.error(f"Erreur : {e}")

def generate_image_prompt(description):
    if not api_key:
        return
    try:
        genai.configure(api_key=api_key.strip())
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        with st.spinner("🎨 Calcul du prompt visuel SVB..."):
            prompt = f"""
            Agis comme un expert en Prompt Engineering pour Midjourney ou DALL-E.
            
            TA MISSION :
            Transforme cette idée : "{description}" en un prompt de génération d'image ultra-détaillé qui respecte STRICTEMENT la DA de SVB.
            
            RÈGLES DE LA DA À INCLURE DANS LE PROMPT :
            - Couleurs : Peach (#EBC6A6), Sage Green (#88C0A6), Cream (#F3EBD4), Warm lighting.
            - Ambiance : Soft, Organic, Premium, Glassmorphism elements, Cinematic lighting, High grain texture.
            - Style : Editorial photography, highly detailed, 8k.
            
            Sortie attendue : Juste le prompt en Anglais, prêt à copier.
            """
            response = model.generate_content(prompt)
            st.info("💡 Copie ce texte dans un générateur d'image (Midjourney, etc) pour avoir le visuel parfait :")
            st.code(response.text, language="bash")
            
    except Exception as e:
        st.error(f"Erreur : {e}")

# --- 4. INTERFACE UTILISATEUR ---
if api_key:
    st.markdown("### 🍑 Studio Créatif & Stratégique")
    
    tab1, tab2, tab3 = st.tabs(["⚡️ Actions Rapides", "🎨 Générateur Visuel (DA)", "🛠️ Mode Manuel"])

    # --- TAB 1 : PRODUCTIVITÉ ---
    with tab1:
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("📅 Planning Semaine (Tableau)", use_container_width=True):
                generate_content("Planning Éditorial Tableau", "Planning semaine prochaine varié (Reformer, Yoga, Kids).", "Stratégique")
        with c2:
            if st.button("✨ Post 'Inspiration' (DA)", use_container_width=True):
                generate_content("Post Instagram Lifestyle", "Sujet : L'équilibre vie pro / santé. Ton : Doux et motivant.", "Haut")
        with c3:
            if st.button("📩 Closing Client (Prix)", use_container_width=True):
                generate_content("Script de Vente", "Objection : 'C'est trop cher'. Utilise l'argument 'Investissement vs Dépense'.", "Expert")

    # --- TAB 2 : VISUEL & IMAGE ---
    with tab2:
        st.markdown("#### 📸 Créateur de Visuels (Respectant la Charte #EBC6A6)")
        st.caption("Décris l'image que tu veux, l'IA va créer la 'recette' parfaite avec tes couleurs.")
        
        desc_img = st.text_input("Idée de l'image :", placeholder="Ex: Une coach qui ajuste une posture sur le Reformer avec une lumière douce...")
        
        if st.button("Générer le Prompt Image"):
            generate_image_prompt(desc_img)

    # --- TAB 3 : MANUEL ---
    with tab3:
        st.write("Mode classique pour uploader des photos et analyser.")
        uploaded_file = st.file_uploader("Analyser une photo", type=["jpg", "png"])
        if uploaded_file:
            st.image(uploaded_file, width=200)
            if st.button("Analyser cette photo"):
                # Fonction simplifiée pour l'exemple
                st.write("Analyse en cours... (Fonction à connecter si besoin)")

else:
    st.info("👈 Connecte ta clé pour activer le Studio DA.")
