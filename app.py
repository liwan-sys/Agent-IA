import streamlit as st
import google.generativeai as genai
from PIL import Image
import urllib.parse # Nécessaire pour encoder le texte en lien image

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
    st.image("https://cdn-icons-png.flaticon.com/512/4825/4825038.png", width=60)
    st.title("🍑 SVB Manager")
    st.caption("DA & Moteur Image : Actifs")
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
            
            TA BIBLE (DA, TARIFS, RÈGLES) :
            {INFO_STUDIO}
            
            TA MISSION :
            Type : {prompt_type}
            Niveau de créativité : {creative_level}
            Contexte : {context}
            
            CONSIGNES :
            - Respecte STRICTEMENT les tarifs et règles de la mémoire.
            - Utilise le vocabulaire de la DA ("Organique", "Cocon", "Premium").
            - Palette émojis : 🍑, 🌿, 🍦, 🌾, ✨.
            """
            
            response = model.generate_content(prompt)
            st.markdown("---")
            st.markdown(response.text)
            st.success("C'est prêt !")

    except Exception as e:
        st.error(f"Erreur : {e}")

def generate_real_image(description):
    if not api_key:
        st.error("Il faut la clé API pour créer la recette de l'image.")
        return

    try:
        # ETAPE 1 : On demande à Gemini de créer le prompt parfait (la recette)
        genai.configure(api_key=api_key.strip())
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        with st.spinner("🧑‍🍳 1/2 : L'IA écrit la recette visuelle (Prompt)..."):
            prompt_request = f"""
            Agis comme un expert photographe. 
            Transforme cette idée : "{description}" en un prompt court en ANGLAIS pour générer une photo réaliste.
            
            RÈGLES IMPÉRATIVES DE LA DA SVB :
            - Colors: Peach, Sage Green, Cream tones.
            - Lighting: Soft, warm, cinematic.
            - Style: High definition photography, minimalist, premium wellness studio.
            - Subject: {description}
            
            Sortie : Juste le texte du prompt en anglais, sans guillemets.
            """
            response_prompt = model.generate_content(prompt_request)
            english_prompt = response_prompt.text.strip()
            
            # On affiche le prompt pour info
            st.caption(f"Recette générée : {english_prompt}")

        # ETAPE 2 : On utilise un moteur gratuit (Pollinations) pour créer l'image
        with st.spinner("🎨 2/2 : Développement de la photo..."):
            # On encode le texte pour le mettre dans une URL
            encoded_prompt = urllib.parse.quote(english_prompt)
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=768&model=flux&nologo=true"
            
            st.markdown("---")
            st.image(image_url, caption=f"📸 Visuel généré pour : {description}", use_container_width=True)
            st.success("Image générée ! (Clic droit > Enregistrer l'image sous...)")
            
    except Exception as e:
        st.error(f"Erreur : {e}")

# --- 4. INTERFACE ---
if api_key:
    st.markdown("### 🍑 Studio Créatif & Stratégique")
    
    tab1, tab2, tab3 = st.tabs(["⚡️ Actions Rapides", "📸 Générateur PHOTO", "🛠️ Mode Manuel"])

    # --- TAB 1 : PRODUCTIVITÉ ---
    with tab1:
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("📅 Planning Semaine", use_container_width=True):
                generate_content("Planning Éditorial Tableau", "Planning semaine pro varié.", "Stratégique")
        with c2:
            if st.button("✨ Post Inspiration", use_container_width=True):
                generate_content("Post Instagram Lifestyle", "Sujet : Équilibre vie pro/perso.", "Haut")
        with c3:
            if st.button("📩 Closing Client", use_container_width=True):
                generate_content("Script de Vente", "Objection : 'C'est trop cher'.", "Expert")

    # --- TAB 2 : VISUEL ---
    with tab2:
        st.markdown("#### 📸 Studio Photo Virtuel")
        st.info("Décris ce que tu veux voir, l'IA va le créer en respectant tes couleurs (Pêche/Sauge).")
        
        desc_img = st.text_input("Je veux voir...", placeholder="Ex: Une séance de yoga calme avec une lumière pêche...")
        
        if st.button("✨ GÉNÉRER L'IMAGE", type="primary"):
            if desc_img:
                generate_real_image(desc_img)
            else:
                st.warning("Écris une description d'abord !")

    # --- TAB 3 : MANUEL ---
    with tab3:
        st.write("Mode classique (Upload Photo pour analyse)")
        uploaded_file = st.file_uploader("Analyser une photo existante", type=["jpg", "png"])
        if uploaded_file:
            st.image(uploaded_file, width=200)

else:
    st.info("👈 Connecte ta clé.")
