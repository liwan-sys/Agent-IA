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
    st.info("💡 Astuce : Une fois collée, appuie sur Entrée.")
    st.markdown("---")
    st.write("🤖 Modèle : **Gemini 1.5 Flash**")

# --- CŒUR DE L'APPLICATION ---
if api_key:
    # Configuration sécurisée
    try:
        genai.configure(api_key=api_key.strip())
        
        # On utilise Flash pour la vitesse (si erreur, change par 'gemini-pro')
        model = genai.GenerativeModel('gemini-1.5-flash')

        # --- INTERFACE UTILISATEUR ---
        col1, col2 = st.columns(2)
        
        with col1:
            platform = st.selectbox(
                "📢 Plateforme",
                ["Post Instagram", "Script Réel/TikTok", "Newsletter Email", "Réponse Client Mécontent"]
            )
        
        with col2:
            tone = st.selectbox(
                "🎭 Ton",
                ["Motivant & Énergique", "Éducatif & Scientifique", "Direct & Hardcore", "Bienveillant"]
            )

        topic = st.text_area(
            "📝 De quoi on parle aujourd'hui ?",
            placeholder="Ex: Les bienfaits du soulevé de terre pour le dos..."
        )

        # Bouton d'action
        if st.button("✨ Générer le contenu", type="primary"):
            if not topic:
                st.warning("Il faut donner un sujet au coach !")
            else:
                with st.spinner("Le coach rédige ton post..."):
                    # LE PROMPT (C'est ici qu'on donne l'intelligence)
                    prompt_complet = f"""
                    Tu es un expert en coaching sportif et marketing digital.
                    Tâche : Rédige un contenu pour {platform}.
                    Sujet : {topic}
                    Ton : {tone}
                    
                    Instructions :
                    - Utilise des emojis pertinents.
                    - Structure le texte pour qu'il soit lisible (puces, paragraphes courts).
                    - Ajoute un appel à l'action clair à la fin (ex: "Réserve ta séance").
                    - Si c'est Instagram, ajoute 10 hashtags pertinents.
                    """
                    
                    response = model.generate_content(prompt_complet)
                    
                    st.success("C'est prêt !")
                    st.markdown("### 📋 Résultat :")
                    st.markdown(response.text)
                    st.balloons()

    except Exception as e:
        st.error(f"Erreur de connexion : {e}")
        st.info("Vérifie que ta clé est bien copiée sans espace.")

else:
    # Écran d'accueil quand il n'y a pas de clé
    st.warning("⬅️ Pour commencer, colle ta clé API Google dans le menu à gauche.")
    st.image("https://images.unsplash.com/photo-1517836357463-d25dfeac3438?q=80&w=1000&auto=format&fit=crop", caption="Ton assistant est prêt.")
