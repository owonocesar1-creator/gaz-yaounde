import streamlit as st
import urllib.parse
import os
import csv
from datetime import datetime

# --- CONFIG PAGE ---
st.set_page_config(
    page_title="Gaz Yaoundé - Boutique",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- TON NUMERO WHATSAPP ICI ---
NUMERO_WHATSAPP = "237690000000"  # <-- MET TON VRAI NUMERO ICI, ex: 237690123456

# --- COMPTEUR VISITEURS ---
def compter_visite():
    fichier = "visites.txt"
    try:
        if os.path.exists(fichier):
            with open(fichier, "r") as f:
                total = int(f.read().strip() or 0)
        else:
            total = 0
    except:
        total = 0
    if "visite_comptee" not in st.session_state:
        total += 1
        try:
            with open(fichier, "w") as f:
                f.write(str(total))
        except:
            pass
        st.session_state["visite_comptee"] = True
    return total

nb_visites = compter_visite()

# --- STYLE ---
st.markdown("""
<style>
.stApp { background-color: #FFF8F0; }
.titre { text-align:center; color:#E65100; font-size:42px; font-weight:900; margin-bottom:0; }
.sous-titre { text-align:center; color:#555; font-size:18px; margin-top:0; }
.carte { background:white; padding:20px; border-radius:15px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); text-align:center; min-height:210px; }
.prix { color:#E65100; font-size:22px; font-weight:800; }
.total-box { background:#FFE0B2; padding:20px; border-radius:15px; text-align:center; font-size:26px; font-weight:900; color:#BF360C; }
</style>
""", unsafe_allow_html=True)

# --- DONNEES ---
produits = [
    {"nom": "OLA Energy", "taille": "12.5kg", "desc": "Gaz domestique", "prix": 6500, "emoji": "🟠"},
    {"nom": "Tradex Gaz", "taille": "12.5kg", "desc": "Gaz domestique", "prix": 6500, "emoji": "🔵"},
    {"nom": "TotalEnergies", "taille": "12.5kg", "desc": "Gaz domestique", "prix": 6500, "emoji": "🔴"},
    {"nom": "Neptune Gaz", "taille": "12.5kg", "desc": "Gaz domestique", "prix": 6500, "emoji": "🟢"},
]

tailles = {
    "6kg - 3 500 FCFA": 3500,
    "12.5kg - 6 500 FCFA": 6500,
    "32kg - 16 000 FCFA": 16000,
}

def format_fcfa(n):
    return f"{n:,}".replace(",", " ") + " FCFA"

# --- EN-TETE ---
st.markdown('<p class="titre">🔥 GAZ YAOUNDÉ</p>', unsafe_allow_html=True)
st.markdown('<p class="sous-titre">Livraison rapide à Yaoundé • Commande en 30 secondes • Paiement à la livraison</p>', unsafe_allow_html=True)
st.caption(f"👀 {nb_visites} personnes ont déjà visité la boutique")
st.divider()

# --- CARTES PRODUITS ---
st.subheader("Nos Bouteilles")
cols = st.columns(4)
for i, p in enumerate(produits):
    with cols[i]:
        st.markdown(f"""
        <div class="carte">
        <div style="font-size:50px;">{p['emoji']}</div>
        <h3>{p['nom']} - {p['taille']}</h3>
        <p>{p['desc']}</p>
        <p class="prix">{format_fcfa(p['prix'])}</p>
        <p style="color:green;">✅ En stock</p>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# --- FORMULAIRE COMMANDE ---
st.subheader("🛒 Commander ici")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 1. Tes infos")
    nom = st.text_input("Ton nom", placeholder="Ex: Jean Paul")
    telephone = st.text_input("Ton téléphone / WhatsApp", placeholder="Ex: 690 00 00 00")
    quartier = st.text_input("Ton quartier à Yaoundé", placeholder="Ex: Mokolo, Bastos, Odza...")

    st.markdown("### 2. Ta bouteille")
    bouteille_choisie = st.selectbox(
        "Choisir ta bouteille",
        [f"{p['nom']} {p['taille']} - {format_fcfa(p['prix'])}" for p in produits]
    )
    taille_choisie_label = st.selectbox("Choisir la taille", list(tailles.keys()), index=1)
    quantite = st.number_input("Quantité", min_value=1, max_value=20, value=1, step=1)

with col2:
    st.markdown("### 3. Récapitulatif")
    prix_unitaire = tailles[taille_choisie_label]
    total = prix_unitaire * quantite
    livraison = 0 if total >= 13000 else 1000
    total_final = total + livraison

    st.markdown(f"""
    <div style="background:white; padding:20px; border-radius:15px;">
    <p><b>Bouteille:</b> {bouteille_choisie}</p>
    <p><b>Taille:</b> {taille_choisie_label}</p>
    <p><b>Quantité:</b> {quantite}</p>
    <p><b>Prix unitaire:</b> {format_fcfa(prix_unitaire)}</p>
    <p><b>Livraison:</b> {format_fcfa(livraison)} {'(Gratuite dès 13 000 FCFA)' if livraison == 0 else ''}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="total-box">Total: {format_fcfa(total_final)}</div>', unsafe_allow_html=True)
    st.write("")
    st.info("💳 Paiement à la livraison - Espèces ou MTN MoMo / Orange Money")

    message = f"""Bonjour Gaz Yaoundé ! Je veux commander:
- Nom: {nom}
- Téléphone: {telephone}
- Quartier: {quartier}
- Bouteille: {bouteille_choisie}
- Taille: {taille_choisie_label}
- Quantité: {quantite}
- Livraison: {format_fcfa(livraison)}
- Total: {format_fcfa(total_final)}"""

    lien = f"https://wa.me/{NUMERO_WHATSAPP}?text={urllib.parse.quote(message)}"

    if st.button("📲 COMMANDER VIA WHATSAPP", use_container_width=True, type="primary"):
        if not nom or not telephone or not quartier:
            st.error("⚠️ Remplis ton nom, ton téléphone et ton quartier d'abord !")
        else:
            try:
                existe = os.path.exists("commandes.csv")
                with open("commandes.csv", "a", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    if not existe:
                        writer.writerow(["date", "nom_client", "telephone", "quartier", "produit", "taille", "quantite", "total"])
                    writer.writerow([datetime.now().strftime("%d/%m/%Y %H:%M"), nom, telephone, quartier, bouteille_choisie, taille_choisie_label, quantite, total_final])
            except:
                pass
            st.success("✅ Commande prête ! Clique en bas pour envoyer sur WhatsApp")
            st.link_button("Ouvrir WhatsApp et envoyer", lien, use_container_width=True)

    if st.button("🧹 Effacer le formulaire", use_container_width=True):
        st.rerun()

st.divider()

# --- ADMIN SIMPLE ---
with st.expander("🔐 Voir mes commandes (pour toi seulement)"):
    if os.path.exists("commandes.csv"):
        try:
            import pandas as pd
            df = pd.read_csv("commandes.csv")
            st.dataframe(df, use_container_width=True)
            st.write(f"Total commandes : {len(df)}")
        except:
            st.write("Aucune commande pour l'instant")
    else:
        st.write("Aucune commande pour l'instant")

st.markdown("<p style='text-align:center; color:#888;'>© 2026 Gaz Yaoundé - Livraison 7j/7 de 7h à 21h • Mokolo - Bastos - Odza - Nlongkak</p>", unsafe_allow_html=True)