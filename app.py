import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuration de la page (Ce qui s'affiche dans l'onglet du navigateur)
st.set_page_config(page_title="SalesFlow Analytics", page_icon="🚀", layout="wide")

# 2. En-tête de l'application
st.title("📊 SalesFlow Analytics")
st.markdown("*Plateforme automatisée d'analyse de données e-commerce.*")
st.markdown("---") # Ligne de séparation

# 3. La barre latérale (Sidebar) pour l'upload du fichier
st.sidebar.header("📂 Importation")
st.sidebar.write("Uploadez le fichier CSV de l'entreprise.")
fichier_upload = st.sidebar.file_uploader("Choisissez un fichier CSV", type=['csv'])

# 4. Le cœur de l'application (Si un fichier est uploadé)
if fichier_upload is not None:
    
    # Lecture dynamique du fichier CSV avec Pandas
    df = pd.read_csv(fichier_upload)
    
    st.success("✅ Données chargées avec succès !")
    
    # Affichage des données brutes
    with st.expander("👁️ Voir les données brutes"):
        st.dataframe(df)
        
    # Vérification : Est-ce le fichier avec les bonnes colonnes ?
    colonnes_pfa = ['ID', 'Prix', 'Quantite', 'Remise']
    
    if all(col in df.columns for col in colonnes_pfa):
        st.header("⚙️ Analyse Automatisée")
        
        # Les calculs Pandas pour les indicateurs clés
        df['CA_Brut'] = df['Prix'] * df['Quantite']
        df['CA_Net'] = df['CA_Brut'] * (1 - (df['Remise'] / 100))
        df['TVA (20%)'] = df['CA_Net'] * 0.20
        
        #  SECTION DASHBOARD
        st.subheader("📈 Indicateurs Clés de Performance (KPI)")
        
        # On crée 3 colonnes alignées pour faire un beau dashboard
        col1, col2, col3 = st.columns(3)
        
        ca_total = df['CA_Net'].sum()
        meilleur_id = df.loc[df['CA_Net'].idxmax(), 'ID']
        
        # st.metric crée les gros blocs de chiffres qui font très "Business"
        col1.metric("CA Net Total", f"{ca_total:.2f} €")
        col2.metric("TVA Totale", f"{df['TVA (20%)'].sum():.2f} €")
        col3.metric("Produit Star (ID)", str(meilleur_id), "Meilleur Vendeur")
        
        st.markdown("---")
        
        # --- SECTION GRAPHIQUE INTERACTIF ---
        st.subheader("📊 Visualisation Interactive")
        # On remplace Matplotlib par Plotly Express pour l'interactivité
        fig = px.bar(df, x='ID', y='CA_Net', 
                     title="Chiffre d'Affaires Net par Produit",
                     color='CA_Net', # Ajoute un dégradé de couleur selon le CA
                     color_continuous_scale='Blues') 
        
        # Affiche le graphique en prenant toute la largeur
        st.plotly_chart(fig, use_container_width=True)
        
        # --- SECTION EXPORT ---
        st.markdown("---")
        st.subheader("📥 Exporter les Résultats")
        # On convertit le dataframe en CSV pour le téléchargement
        csv_export = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Télécharger le rapport d'analyse final",
            data=csv_export,
            file_name='rapport_ventes_final.csv',
            mime='text/csv',
        )
        
    else:
        st.warning("⚠️ Ce fichier ne contient pas les colonnes du PFA (ID, Prix, Quantite, Remise). Affichage en mode exploratoire simple.")

else:
    # Message d'accueil si aucun fichier n'est uploadé
    st.info("👈 Veuillez uploader un fichier CSV dans le menu de gauche pour lancer l'analyse.")