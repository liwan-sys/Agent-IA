import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. IMPORTATION DE LA MÉMOIRE (Ton Site) ---
try:
    from knowledge import INFO_STUDIO
except ImportError:
    INFO_STUDIO = "Erreur : Fichier knowledge.py introuvable."

# --- 2. CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Manager SVB", page_icon="🧡", layout="centered")

# --- 3. GESTION AUTOMATIQUE DE LA CLÉ ---
api_key = None
try:
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
except:
    pass

# --- 4. BARRE LATÉRALE ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4825/4825038.png", width=60)
    st.title("SVB Manager")
    st.markdown("---")
    
    if api_key:
        st.success("🔑 Clé connectée (Auto)")
    else:
        st.warning("Mode manuel")
        api_key = st.text_input("Colle ta clé API ici", type="password")

    if "Sèche-cheveux" in INFO_STUDIO:
        st.info("🧠 Mémoire Studio : Active")
    else:
        st.error("🧠 Mémoire : Vide")

# --- 5. FONCTION DE GÉNÉRATION (Le Cerveau) ---
def generate_content(action_type, ton_style, user_context, image=None):
    if not api_key:
        st.error("Il manque la clé API !")
        return

    try:
        genai.configure(api_key=api_key.strip())
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        with st.spinner(f"🤖 Action : {action_type}..."):
            prompt = f"""
            Tu es l'assistant IA officiel du studio SVB (Santez-Vous Bien).
            
            DONNÉES MÉMOIRE DU STUDIO :
            {INFO_STUDIO}
            
            TA TÂCHE :
            Action : {action_type}
            Ton : {ton_style}
            Contexte : {user_context}
            
            CONSIGNES :
            1. Utilise les infos réelles (tarifs, règles, horaires).
            2. Si c'est un PLANNING : Fais un tableau Markdown propre.
            3. Si c'est un MESSAGE CLIENT : Sois empathique et termine par une question.
            4. Si c'est un POST : Mets des émojis et des hashtags.
            """
            
            if image:
                response = model.generate_content([prompt, image])
            else:
                response = model.generate_content(prompt)
            
            st.markdown("---")
            st.markdown(f"### 🎯 Résultat ({action_type})")
            st.markdown(response.text)
            st.success("Terminé ! Copie le texte ci-dessus.")

    except Exception as e:
        st.error(f"Erreur technique : {e}")

# --- 6. APPLICATION PRINCIPALE ---
if api_key:
    st.markdown("### ⚡️ Tableau de Bord Rapide")
    
    # --- A. BOUTONS RAPIDES (1 Clic = Résultat) ---
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📅 Planning Semaine", use_container_width=True):
            generate_content(
                "Planning Éditorial (Tableau Lundi-Dimanche)", 
                "Stratégique & Varié", 
                "Crée le planning Instagram de la semaine prochaine. Alterne Reformer, Cross, Kids et Motivation."
            )
            
    with col2:
        if st.button("📸 Idée Post du Jour", use_container_width=True):
            generate_content(
                "Post Instagram (Caption + Idée Visuelle)", 
                "Motivant & Viral", 
                "Donne-moi une idée de post impactant pour aujourd'hui pour vendre du Pass Starter."
            )
            
    with col3:
        if st.button("📩 Relance Impayé", use_container_width=True):
            generate_content(
                "Message Privé (WhatsApp)", 
                "Courtois mais Ferme", 
                "Le client a un échec de paiement sur son abonnement. Relance-le gentiment avec un lien de régularisation."
            )

    st.markdown("---")
    
    # --- B. MODE MANUEL & VISION (Pour le sur-mesure) ---
    with st.expander("🛠️ Mode Manuel & Vision (Cliquer pour ouvrir)", expanded=True):
        
        # Upload Photo
        uploaded_file = st.file_uploader("Glisse une photo (Salle, Posture, Machine...)", type=["jpg", "jpeg", "png"])
        image_data = None
        if uploaded_file:
            image_data = Image.open(uploaded_file)
            st.image(image_data, width=200)

        # Formulaire
        c1, c2 = st.columns(2)
        with c1:
            custom_action = st.selectbox("Action", ["Réponse Client", "Post Instagram", "Analyse Posture", "Email Newsletter"])
        with c2:
            custom_ton = st.selectbox("Ton", ["Bienveillant", "Coach Direct", "Commercial", "Humoristique"])
            
        # Zone de texte intelligente (Brouillon)
        custom_context = st.text_area("Ton brouillon ou message client :", 
                                    placeholder="Ex: Elle demande si le yoga c'est bon pour le stress...", height=100)

        if st.button("✨ Générer le contenu sur-mesure", type="primary"):
            final_context = custom_context if custom_context else "Analyse cette image et propose du contenu adapté."
            generate_content(custom_action, custom_ton, final_context, image_data)

else:
    st.info("👈 Connecte ta clé API pour accéder au tableau de bord.")
