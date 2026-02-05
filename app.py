import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Studio Coach Manager",
    page_icon="🏋️‍♂️",
    layout="centered"
)

st.title("🏋️‍♂️ Studio Coach - Créateur de Contenu")
st.markdown("---")

# --- BARRE LATÉRALE (CLÉ API) ---
with st.sidebar:
    st.header("🔑 Accès Sécurisé")
    api_key = st.text_input("Colle ta clé API ici", type="password")
    st.info("Une fois collée, appuie sur Entrée.")
    st.markdown("---")
    # On affiche le modèle puissant que tu as trouvé !
    st.write("🚀 Moteur : **Gemini 2.5 Flash**")

# --- CŒUR DE L'APPLICATION ---
if api_key:
    try:
        # 1. Connexion
        genai.configure(api_key=api_key.strip())
        
        # 2. On utilise LE modèle qui a marché dans ton test
        model = genai.GenerativeModel('gemini-2.5-flash')

        # 3. Interface Utilisateur
        col1, col2 = st.columns(2)
        
        with col1:
            platform = st.selectbox(
                "📢 Plateforme",
                ["Post Instagram", "Script TikTok/Reel", "Newsletter Email", "Message de Relance Client"]
            )
        
        with col2:
            tone = st.selectbox(
                "🎭 Ton",
                ["Motivant & Énergique", "Éducatif & Scientifique", "Direct & Strict", "Bienveillant"]
            )

        topic = st.text_area(
            "📝 De quoi on parle aujourd'hui ?",
            placeholder="Ex: Les bienfaits du Pilates pour le mal de dos..."
        )

        # 4. Le Bouton Magique
        if st.button("✨ Générer le contenu", type="primary"):
            if not topic:
                st.warning("Donne-moi un sujet d'abord !")
            else:
                with st.spinner("Le coach rédige..."):
                    
                    # Le "Cerveau" du prompt
                    prompt = f"""
                    Agis comme un expert en coaching sportif et marketing.
                    ACTION : Rédige un contenu pour {platform}.
                    SUJET : {topic}
                    TON : {tone}
                    
                    CONSIGNES :
                    - Fais des paragraphes courts et lisibles.
                    - Utilise des emojis sportifs.
                    - Termine par une question engageante ou un appel à l'action.
                    - Si c'est pour Instagram/TikTok, ajoute 5 hashtags pertinents.
                    """
                    
                    # Génération
                    response = model.generate_content(prompt)
                    
                    st.success("C'est prêt !")
                    st.markdown("### 📋 Ton Résultat :")
                    st.write(response.text)
                    st.balloons()

    except Exception as e:
        st.error("Oups, petite erreur technique...")
        st.warning(f"Message d'erreur : {e}")
        st.info("Vérifie que ta clé API est bien collée sans espace.")

else:
    # Message d'accueil
    st.info("⬅️ Colle ta clé API dans le menu de gauche pour activer le coach.")
