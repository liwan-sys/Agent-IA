import streamlit as st
import google.generativeai as genai
import urllib.parse

# --- 1. IMPORTATION MÉMOIRE (Le Cerveau) ---
try:
    from knowledge import INFO_STUDIO
except ImportError:
    INFO_STUDIO = "Erreur : Fichier knowledge.py introuvable."

# Configuration de la page
st.set_page_config(page_title="SVB Manager", page_icon="🍑", layout="wide")

# --- 2. GESTION CLÉ API (La Sécurité) ---
api_key = None
try:
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
except:
    pass

# Barre latérale
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4825/4825038.png", width=60)
    st.title("🍑 SVB Manager")
    st.markdown("---")
    
    if api_key:
        st.success("✅ Clé connectée")
    else:
        st.warning("Mode manuel")
        api_key = st.text_input("Colle ta clé API ici", type="password")

    if "Pêche" in INFO_STUDIO:
        st.caption("🧠 Mémoire DA : Chargée")

# --- 3. FONCTIONS INTELLIGENTES ---

def generate_text(prompt_type, context):
    """Génère du texte (Posts, Planning, Scripts)"""
    if not api_key:
        st.error("Il manque la clé API.")
        return

    try:
        genai.configure(api_key=api_key.strip())
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        with st.spinner(f"✍️ Rédaction en cours ({prompt_type})..."):
            prompt = f"""
            Tu es le Responsable Marketing et DA du studio SVB.
            
            TA MÉMOIRE (DA & OFFRES) :
            {INFO_STUDIO}
            
            MISSION :
            Action : {prompt_type}
            Contexte : {context}
            
            CONSIGNES :
            - Utilise le ton "Cocon Sportif" (Bienveillant mais Expert).
            - Respecte la palette : 🍑, 🌿, 🍦, 🌾.
            - Sois structuré et pro.
            """
            
            response = model.generate_content(prompt)
            st.markdown("---")
            st.markdown(response.text)
            st.success("Contenu généré !")
            
    except Exception as e:
        st.error(f"Erreur : {e}")

def generate_image_link(description):
    """Génère un lien vers une image HD"""
    if not api_key:
        st.error("Il manque la clé API.")
        return

    try:
        # ETAPE 1 : On demande à Gemini de créer le prompt parfait (Anglais)
        genai.configure(api_key=api_key.strip())
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        with st.spinner("🎨 Fabrication de la recette visuelle (Prompt)..."):
            # On force un style très "Magazine Déco" pour imiter la qualité Nano Banana
            prompt_request = f"""
            Act as a high-end architectural photographer.
            Convert this idea: "{description}" into a strict English prompt for an image generator.
            
            MANDATORY SVB AESTHETIC:
            - Colors: Soft Peach (#EBC6A6), Sage Green, Cream, Warm Beige.
            - Lighting: Golden hour, soft cinematic light, volumetric lighting, no harsh shadows.
            - Style: Award-winning interior photography, 8k resolution, highly detailed, photorealistic.
            - Vibe: Serene, Organic, Premium, Wellness, "Cocon Sportif".
            
            Output: ONLY the English prompt.
            """
            response = model.generate_content(prompt_request)
            english_prompt = response.text.strip()
            
            # Affichage discret du prompt pour info
            st.caption(f"🔧 Recette technique : {english_prompt}")

        # ETAPE 2 : Génération via Pollinations (Moteur Flux - Très réaliste)
        with st.spinner("📸 Développement de la photo..."):
            encoded_prompt = urllib.parse.quote(english_prompt)
            # On utilise le modèle "Flux" qui est le meilleur gratuit actuel
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=768&model=flux&nologo=true"
            
            st.markdown("---")
            st.subheader("📸 Votre Visuel SVB")
            
            # On affiche le lien EN PREMIER (Sécurité si l'image ne charge pas)
            st.markdown(f"👉 **[CLIQUE ICI pour ouvrir l'image en Grand (HD)]({image_url})**")
            
            # On essaie d'afficher l'image
            st.image(image_url, caption=description, use_container_width=True)
            
    except Exception as e:
        st.error(f"Erreur technique : {e}")

# --- 4. INTERFACE UTILISATEUR ---
if api_key:
    st.markdown("### 🍑 Studio Créatif & Stratégique")
    
    # Onglets
    tab1, tab2, tab3 = st.tabs(["⚡️ Actions Rapides", "📸 Générateur Visuel", "🛠️ Mode Manuel"])

    # --- TAB 1 : PRODUCTIVITÉ (TEXTE) ---
    with tab1:
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("📅 Planning Semaine (Tableau)", use_container_width=True):
                generate_text("Planning Éditorial", "Fais le planning de la semaine prochaine. Varie les plaisirs (Reformer, Yoga, Kids).")
        with c2:
            if st.button("✨ Post Inspiration (Lifestyle)", use_container_width=True):
                generate_text("Post Instagram", "Sujet : L'importance de prendre du temps pour soi. Ton doux et motivant.")
        with c3:
            if st.button("📩 Closing Vente (Objection)", use_container_width=True):
                generate_text("Script Commercial", "Le client trouve que c'est trop cher. Utilise l'argument Investissement vs Dépense.")

    # --- TAB 2 : VISUEL (IMAGE) ---
    with tab2:
        st.markdown("#### 📸 Studio Photo IA")
        st.info("Décris l'image. L'IA appliquera automatiquement les couleurs Pêche & Sauge.")
        
        col_input, col_btn = st.columns([3, 1])
        with col_input:
            desc_img = st.text_input("Je veux voir...", placeholder="Ex: Une salle de reformer vide avec une belle lumière douce...")
        with col_btn:
            st.write("") # Espace
            st.write("") # Espace
            if st.button("✨ GÉNÉRER", type="primary"):
                if desc_img:
                    generate_image_link(desc_img)
                else:
                    st.warning("Écris une description !")

    # --- TAB 3 : MANUEL (ANALYSIS) ---
    with tab3:
        st.write("Mode classique : Analyse de photos")
        # Code simplifié pour l'analyse photo si besoin
        st.caption("Fonctionnalité d'analyse photo disponible sur demande.")

else:
    st.info("👈 Connecte ta clé API pour commencer.")
