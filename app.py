import streamlit as st
import google.generativeai as genai

st.title("🕵️ Scanner de Modèles Google")

# 1. On rentre la clé
api_key = st.text_input("Colle ta clé API", type="password")

if st.button("🔍 Scanner les modèles disponibles"):
    if not api_key:
        st.warning("Il faut la clé !")
    else:
        try:
            genai.configure(api_key=api_key.strip())
            
            st.info("Interrogation de Google en cours...")
            
            # C'est la commande magique demandée par l'erreur
            liste_modeles = []
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    liste_modeles.append(m.name)
            
            if len(liste_modeles) > 0:
                st.success(f"✅ J'ai trouvé {len(liste_modeles)} modèles accessibles avec ta clé !")
                st.write("Voici les noms EXACTS à utiliser dans le code :")
                st.code(liste_modeles)
                
                # Test immédiat avec le premier de la liste
                premier_modele = liste_modeles[0].replace("models/", "")
                st.markdown(f"--- \n **Test automatique avec : `{premier_modele}`**")
                
                model = genai.GenerativeModel(premier_modele)
                response = model.generate_content("Si tu me lis, écris 'VICTOIRE'")
                st.write(f"🤖 Réponse de l'IA : **{response.text}**")
                
            else:
                st.error("Aucun modèle trouvé. Ta clé est valide mais n'a accès à rien (problème de compte Google ?).")
                
        except Exception as e:
            st.error(f"Erreur technique : {e}")
