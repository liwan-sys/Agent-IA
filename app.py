import streamlit as st
import google.generativeai as genai
import sys

st.title("👨‍⚕️ Diagnostic Agent IA")

# 1. Vérification de la version des outils
st.subheader("1. Vérification du Système")
try:
    version = genai.__version__
    st.write(f"📚 Version de l'outil Google installée : **{version}**")
    
    # On vérifie si la mise à jour a marché
    if version < "0.7.2":
        st.error("❌ ERREUR CRITIQUE : La mise à jour n'a pas fonctionné. Le serveur utilise une vieille version.")
        st.info("Solution : Vérifie que ton fichier s'appelle bien 'requirements.txt' (avec un 's' à la fin) sur GitHub.")
    else:
        st.success("✅ Système à jour (Version compatible Gemini Flash)")
except Exception as e:
    st.error(f"Erreur système : {e}")

# 2. Vérification de la Clé
st.subheader("2. Test de la Clé API")
api_key = st.text_input("Colle ta clé API ici pour tester", type="password")

if st.button("Lancer le test de connexion"):
    if not api_key:
        st.warning("Il faut coller la clé d'abord !")
    else:
        try:
            genai.configure(api_key=api_key.strip())
            
            # On demande la liste des modèles disponibles pour cette clé
            st.write("📡 Connexion à Google...")
            models = list(genai.list_models())
            noms_modeles = [m.name for m in models]
            
            st.success("✅ CONNEXION RÉUSSIE ! Ta clé fonctionne.")
            st.write("Modèles accessibles :")
            st.code(noms_modeles)
            
        except Exception as e:
            st.error("❌ La clé ne fonctionne pas.")
            st.error(f"Message d'erreur : {e}")
