“””
EduTrack — Application de collecte et d’analyse des performances des étudiants
Cours   : INF 232 EC2 — Analyse de données
Langage : Python | Framework : Streamlit
Auteur  : Projet académique
“””

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import io
from datetime import datetime

# ─────────────────────────────────────────────────────────────

# CONFIGURATION MATPLOTLIB

# ─────────────────────────────────────────────────────────────

matplotlib.rcParams.update({
“figure.facecolor”:  “#0e1117”,
“axes.facecolor”:    “#1a1f2e”,
“axes.edgecolor”:    “#2d3748”,
“axes.labelcolor”:   “#a0aec0”,
“axes.titlecolor”:   “#e2e8f0”,
“xtick.color”:       “#a0aec0”,
“ytick.color”:       “#a0aec0”,
“text.color”:        “#e2e8f0”,
“grid.color”:        “#2d3748”,
“grid.alpha”:        0.5,
“legend.facecolor”:  “#1a1f2e”,
“legend.edgecolor”:  “#2d3748”,
“font.size”:         10,
})

# ─────────────────────────────────────────────────────────────

# CONFIGURATION STREAMLIT

# ─────────────────────────────────────────────────────────────

st.set_page_config(
page_title=“EduTrack — Performances des étudiants”,
page_icon=“🎓”,
layout=“wide”,
initial_sidebar_state=“expanded”,
)

# ─────────────────────────────────────────────────────────────

# CONSTANTES

# ─────────────────────────────────────────────────────────────

FILIERES = [
“Informatique”, “Mathématiques”, “Physique”, “Chimie”,
“Biologie”, “Économie”, “Droit”, “Médecine”,
“Génie Civil”, “Génie Électrique”, “Gestion”, “Lettres”
]

NIVEAUX = [“Licence 1”, “Licence 2”, “Licence 3”, “Master 1”, “Master 2”, “Doctorat”]

SEMESTRES = [“Semestre 1”, “Semestre 2”]

ANNEES = [“2022-2023”, “2023-2024”, “2024-2025”, “2025-2026”]

MATIERES = [
“Mathématiques”, “Informatique”, “Physique”, “Chimie”,
“Analyse”, “Algèbre”, “Statistiques”, “Probabilités”,
“Programmation”, “Base de données”, “Réseau”, “Anglais”,
“Français”, “Économie”, “Gestion de projet”
]

COLONNES = [
“Nom”, “Prénom”, “Matricule”, “Filière”, “Niveau”,
“Matière”, “Note (/20)”, “Semestre”, “Année académique”,
“Sexe”, “Âge”
]

# ─────────────────────────────────────────────────────────────

# SESSION STATE — initialisation avec données de démonstration

# ─────────────────────────────────────────────────────────────

if “df” not in st.session_state:
np.random.seed(42)
n_demo = 40
noms   = [“Mbala”,“Nzinga”,“Lelo”,“Kanda”,“Boma”,“Toko”,“Sana”,“Fula”,“Mpia”,“Diko”]
prenoms= [“Jean”,“Marie”,“Pierre”,“Alice”,“Paul”,“Sophie”,“Luc”,“Anna”,“Marc”,“Eva”]
demo   = []
for i in range(n_demo):
filiere  = np.random.choice(FILIERES[:6])
niveau   = np.random.choice(NIVEAUX[:4])
matiere  = np.random.choice(MATIERES[:8])
note     = round(np.random.normal(12.5, 3.2), 2)
note     = max(0.0, min(20.0, note))
age      = int(np.random.randint(18, 30))
demo.append([
np.random.choice(noms),
np.random.choice(prenoms),
f”ETU{1000+i}”,
filiere,
niveau,
matiere,
note,
np.random.choice(SEMESTRES),
np.random.choice(ANNEES[:2]),
np.random.choice([“M”, “F”]),
age,
])
st.session_state.df = pd.DataFrame(demo, columns=COLONNES)

# ─────────────────────────────────────────────────────────────

# FONCTIONS UTILITAIRES

# ─────────────────────────────────────────────────────────────

def get_df() -> pd.DataFrame:
return st.session_state.df.copy()

def mention(note: float) -> str:
if note >= 16:   return “Très Bien”
elif note >= 14: return “Bien”
elif note >= 12: return “Assez Bien”
elif note >= 10: return “Passable”
else:            return “Insuffisant”

def couleur_note(note: float) -> str:
if note >= 14:   return “#10d47e”
elif note >= 10: return “#f5c842”
else:            return “#f05252”

def stats_descriptives(serie: pd.Series) -> pd.DataFrame:
“”“Calcule les statistiques descriptives complètes d’une série numérique.”””
s = serie.dropna()
if len(s) == 0:
return pd.DataFrame()
cv = (s.std() / s.mean() * 100) if s.mean() != 0 else 0
etendue = s.max() - s.min()
iq = s.quantile(0.75) - s.quantile(0.25)
return pd.DataFrame({
“Indicateur”: [
“N (effectif)”,
“Moyenne”,
“Médiane”,
“Mode (approx.)”,
“Minimum”,
“Maximum”,
“Étendue”,
“Écart-type”,
“Variance”,
“Coeff. de variation (%)”,
“1er Quartile — Q1”,
“3e Quartile — Q3”,
“Intervalle interquartile (IQR)”,
“Asymétrie (Skewness)”,
“Aplatissement (Kurtosis)”,
],
“Valeur”: [
int(len(s)),
f”{s.mean():.2f} / 20”,
f”{s.median():.2f} / 20”,
f”{round(s.mode().iloc[0], 1):.2f} / 20” if not s.mode().empty else “—”,
f”{s.min():.2f} / 20”,
f”{s.max():.2f} / 20”,
f”{etendue:.2f}”,
f”{s.std():.4f}”,
f”{s.var():.4f}”,
f”{cv:.2f} %”,
f”{s.quantile(0.25):.2f} / 20”,
f”{s.quantile(0.75):.2f} / 20”,
f”{iq:.2f}”,
f”{s.skew():.4f}”,
f”{s.kurt():.4f}”,
]
})

# ─────────────────────────────────────────────────────────────

# SIDEBAR

# ─────────────────────────────────────────────────────────────

with st.sidebar:
st.title(“🎓 EduTrack”)
st.caption(“Analyse des performances des étudiants”)
st.caption(“INF 232 EC2 — Analyse de données”)
st.markdown(”—”)

```
page = st.radio("Navigation", [
    "📥 Saisie des données",
    "📋 Base de données",
    "📊 Analyse descriptive",
    "📈 Régression linéaire",
    "💾 Export des données",
])

st.markdown("---")
df_side = get_df()
if not df_side.empty:
    notes = df_side["Note (/20)"]
    st.metric("Étudiants enregistrés",  len(df_side))
    st.metric("Moyenne générale",        f"{notes.mean():.2f} / 20")
    st.metric("Taux de réussite (≥10)",  f"{(notes >= 10).mean()*100:.1f} %")
    st.metric("Meilleure note",          f"{notes.max():.2f} / 20")
```

# ═════════════════════════════════════════════════════════════

# PAGE 1 — SAISIE DES DONNÉES

# ═════════════════════════════════════════════════════════════

if page == “📥 Saisie des données”:

```
st.title("📥 Saisie d'un résultat étudiant")
st.markdown("Remplissez le formulaire ci-dessous pour enregistrer la note d'un étudiant.")
st.markdown("---")

with st.form(key="form_saisie", clear_on_submit=True):

    col1, col2, col3 = st.columns(3)

    with col1:
        nom         = st.text_input("Nom *",        placeholder="Ex : Mbala")
        prenom      = st.text_input("Prénom *",     placeholder="Ex : Jean")
        matricule   = st.text_input("Matricule *",  placeholder="Ex : ETU2025")

    with col2:
        filiere     = st.selectbox("Filière *",          FILIERES)
        niveau      = st.selectbox("Niveau *",           NIVEAUX)
        matiere     = st.selectbox("Matière *",          MATIERES)

    with col3:
        note        = st.number_input("Note (/20) *",   min_value=0.0, max_value=20.0, step=0.25, format="%.2f")
        semestre    = st.selectbox("Semestre *",         SEMESTRES)
        annee       = st.selectbox("Année académique *", ANNEES)

    col4, col5 = st.columns(2)
    with col4:
        sexe        = st.selectbox("Sexe", ["M", "F"])
    with col5:
        age         = st.number_input("Âge", min_value=16, max_value=60, value=20, step=1)

    st.markdown(" ")
    soumettre = st.form_submit_button(
        "💾 Enregistrer le résultat",
        use_container_width=True,
        type="primary"
    )

    if soumettre:
        erreurs = []
        if not nom.strip():
            erreurs.append("Le champ **Nom** est obligatoire.")
        if not prenom.strip():
            erreurs.append("Le champ **Prénom** est obligatoire.")
        if not matricule.strip():
            erreurs.append("Le champ **Matricule** est obligatoire.")

        if erreurs:
            for e in erreurs:
                st.error(e)
        else:
            nouvelle_ligne = pd.DataFrame([[
                nom.strip(), prenom.strip(), matricule.strip(),
                filiere, niveau, matiere,
                round(float(note), 2),
                semestre, annee, sexe, int(age)
            ]], columns=COLONNES)

            st.session_state.df = pd.concat(
                [st.session_state.df, nouvelle_ligne],
                ignore_index=True
            )
            st.success(
                f"✅ Résultat enregistré — **{prenom.strip()} {nom.strip()}** | "
                f"{matiere} | Note : **{note:.2f}/20** | Mention : **{mention(note)}**"
            )
            st.balloons()
```

# ═════════════════════════════════════════════════════════════

# PAGE 2 — BASE DE DONNÉES

# ═════════════════════════════════════════════════════════════

elif page == “📋 Base de données”:

```
st.title("📋 Base de données")
st.markdown("Consultez et filtrez l'ensemble des résultats enregistrés.")
st.markdown("---")

df = get_df()

if df.empty:
    st.info("📭 Aucun résultat disponible. Commencez par saisir des données.")
else:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        flt_filiere = st.selectbox("Filière",   ["Toutes"] + FILIERES)
    with col2:
        flt_niveau  = st.selectbox("Niveau",    ["Tous"]   + NIVEAUX)
    with col3:
        flt_matiere = st.selectbox("Matière",   ["Toutes"] + MATIERES)
    with col4:
        flt_annee   = st.selectbox("Année",     ["Toutes"] + ANNEES)

    if flt_filiere != "Toutes":
        df = df[df["Filière"] == flt_filiere]
    if flt_niveau != "Tous":
        df = df[df["Niveau"] == flt_niveau]
    if flt_matiere != "Toutes":
        df = df[df["Matière"] == flt_matiere]
    if flt_annee != "Toutes":
        df = df[df["Année académique"] == flt_annee]

    st.markdown(f"**{len(df)} enregistrement(s) affiché(s)**")

    df_affiche = df.copy().reset_index(drop=True)
    df_affiche["Mention"] = df_affiche["Note (/20)"].apply(mention)
    st.dataframe(df_affiche, use_container_width=True, height=450)

    st.markdown("---")
    if st.button("🗑️ Supprimer toutes les données", type="secondary"):
        st.session_state.df = pd.DataFrame(columns=COLONNES)
        st.success("Base de données vidée.")
        st.rerun()
```

# ═════════════════════════════════════════════════════════════

# PAGE 3 — ANALYSE DESCRIPTIVE

# ═════════════════════════════════════════════════════════════

elif page == “📊 Analyse descriptive”:

```
st.title("📊 Analyse descriptive")
st.markdown("Statistiques complètes et visualisations graphiques des performances.")
st.markdown("---")

df = get_df()

if len(df) < 2:
    st.warning("⚠️ Données insuffisantes. Enregistrez au moins 2 résultats.")
    st.stop()

notes = df["Note (/20)"]

# ── KPI ──
taux_reussite = (notes >= 10).mean() * 100
taux_echec    = 100 - taux_reussite

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("👥 Effectif total",      len(df))
c2.metric("📊 Moyenne générale",    f"{notes.mean():.2f} / 20")
c3.metric("🏆 Taux de réussite",    f"{taux_reussite:.1f} %")
c4.metric("⚠️ Taux d'échec",        f"{taux_echec:.1f} %")
c5.metric("🎯 Meilleure note",      f"{notes.max():.2f} / 20")

st.markdown("---")

# ── Tableau des statistiques descriptives ──
st.subheader("📐 Statistiques descriptives des notes")
st.dataframe(
    stats_descriptives(notes),
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# ── Graphique 1 : Histogramme des notes ──
st.subheader("📊 Distribution des notes")

fig1, ax1 = plt.subplots(figsize=(10, 4))
bins = np.arange(0, 21, 1)
ax1.hist(notes, bins=bins, color="#3b82f6", alpha=0.8, edgecolor="#1e2d4a", linewidth=0.8)
ax1.axvline(notes.mean(),   color="#f5c842", linewidth=2,   linestyle="--", label=f"Moyenne : {notes.mean():.2f}")
ax1.axvline(notes.median(), color="#10d47e", linewidth=2,   linestyle=":",  label=f"Médiane : {notes.median():.2f}")
ax1.axvline(10,             color="#f05252", linewidth=1.5, linestyle="-",  label="Seuil de réussite (10)")
ax1.set_xlabel("Note (/20)")
ax1.set_ylabel("Nombre d'étudiants")
ax1.set_title("Distribution des notes — Histogramme", pad=10)
ax1.set_xlim(0, 20)
ax1.legend()
ax1.grid(axis="y", linestyle="--", alpha=0.4)
plt.tight_layout()
st.pyplot(fig1)
plt.close(fig1)

st.markdown("---")

# ── Graphique 2 & 3 côte à côte ──
col_g1, col_g2 = st.columns(2)

with col_g1:
    st.subheader("🥧 Répartition par mention")
    df_m = df.copy()
    df_m["Mention"] = df_m["Note (/20)"].apply(mention)
    counts = df_m["Mention"].value_counts()
    ordre  = ["Très Bien", "Bien", "Assez Bien", "Passable", "Insuffisant"]
    counts = counts.reindex([m for m in ordre if m in counts.index])
    colors_pie = ["#10d47e", "#3b82f6", "#f5c842", "#fb923c", "#f05252"]

    fig2, ax2 = plt.subplots(figsize=(5, 5))
    wedges, texts, autotexts = ax2.pie(
        counts.values,
        labels=counts.index,
        autopct="%1.1f%%",
        colors=colors_pie[:len(counts)],
        startangle=90,
        pctdistance=0.82,
    )
    for t in texts:
        t.set_fontsize(9)
    for at in autotexts:
        at.set_fontsize(9)
    ax2.set_title("Répartition par mention", pad=10)
    plt.tight_layout()
    st.pyplot(fig2)
    plt.close(fig2)

with col_g2:
    st.subheader("📦 Boîte à moustaches par filière")
    filieres_pres = df["Filière"].unique().tolist()
    data_box = [df[df["Filière"] == f]["Note (/20)"].dropna().values for f in filieres_pres]
    data_box = [d for d in data_box if len(d) > 0]
    labels_box = [f for f, d in zip(filieres_pres, [df[df["Filière"] == f]["Note (/20)"].dropna().values for f in filieres_pres]) if len(d) > 0]

    fig3, ax3 = plt.subplots(figsize=(5, 5))
    bp = ax3.boxplot(
        data_box,
        labels=labels_box,
        patch_artist=True,
        medianprops={"color": "#f5c842", "linewidth": 2},
    )
    colors_box = plt.cm.tab10.colors
    for patch, color in zip(bp["boxes"], colors_box):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    ax3.set_xlabel("Filière")
    ax3.set_ylabel("Note (/20)")
    ax3.set_title("Distribution des notes par filière", pad=10)
    ax3.set_ylim(0, 20)
    ax3.axhline(10, color="#f05252", linestyle="--", linewidth=1, alpha=0.7)
    plt.xticks(rotation=30, ha="right", fontsize=8)
    ax3.grid(axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()
    st.pyplot(fig3)
    plt.close(fig3)

st.markdown("---")

# ── Graphique 4 : Moyenne par matière ──
st.subheader("📚 Moyenne des notes par matière")
moy_matiere = df.groupby("Matière")["Note (/20)"].mean().sort_values(ascending=True)

fig4, ax4 = plt.subplots(figsize=(10, max(4, len(moy_matiere) * 0.5)))
colors_bar = ["#10d47e" if v >= 10 else "#f05252" for v in moy_matiere.values]
bars = ax4.barh(moy_matiere.index, moy_matiere.values, color=colors_bar, alpha=0.85)
ax4.axvline(10, color="#f5c842", linestyle="--", linewidth=1.5, label="Seuil réussite (10)")
ax4.axvline(moy_matiere.mean(), color="#a0aec0", linestyle=":", linewidth=1.5,
            label=f"Moyenne générale ({moy_matiere.mean():.2f})")
for bar, val in zip(bars, moy_matiere.values):
    ax4.text(val + 0.1, bar.get_y() + bar.get_height() / 2,
             f"{val:.2f}", va="center", fontsize=9)
ax4.set_xlabel("Moyenne (/20)")
ax4.set_xlim(0, 22)
ax4.set_title("Moyenne des notes par matière", pad=10)
ax4.legend()
ax4.grid(axis="x", linestyle="--", alpha=0.4)
plt.tight_layout()
st.pyplot(fig4)
plt.close(fig4)

st.markdown("---")

# ── Graphique 5 : Comparaison par sexe ──
st.subheader("👥 Comparaison des performances par sexe")
moy_sexe = df.groupby("Sexe")["Note (/20)"].mean()

fig5, axes5 = plt.subplots(1, 2, figsize=(10, 4))

# Bar chart
sexe_labels = moy_sexe.index.tolist()
sexe_colors = ["#3b82f6", "#f472b6"]
axes5[0].bar(sexe_labels, moy_sexe.values, color=sexe_colors[:len(sexe_labels)], alpha=0.85, width=0.4)
for i, (label, val) in enumerate(zip(sexe_labels, moy_sexe.values)):
    axes5[0].text(i, val + 0.2, f"{val:.2f}", ha="center", fontsize=11, fontweight="bold")
axes5[0].axhline(10, color="#f05252", linestyle="--", linewidth=1.5, alpha=0.7)
axes5[0].set_ylim(0, 20)
axes5[0].set_ylabel("Moyenne (/20)")
axes5[0].set_title("Moyenne par sexe")
axes5[0].grid(axis="y", linestyle="--", alpha=0.4)

# Effectifs
eff_sexe = df["Sexe"].value_counts()
axes5[1].pie(
    eff_sexe.values,
    labels=eff_sexe.index,
    autopct="%1.1f%%",
    colors=["#3b82f6", "#f472b6"][:len(eff_sexe)],
    startangle=90,
)
axes5[1].set_title("Répartition effectif par sexe")

plt.tight_layout()
st.pyplot(fig5)
plt.close(fig5)
```

# ═════════════════════════════════════════════════════════════

# PAGE 4 — RÉGRESSION LINÉAIRE SIMPLE

# ═════════════════════════════════════════════════════════════

elif page == “📈 Régression linéaire”:

```
st.title("📈 Régression linéaire simple")
st.markdown("Modélisation de la relation entre l'âge (ou le rang) d'un étudiant et sa note.")
st.markdown("---")

df = get_df()

if len(df) < 3:
    st.warning("⚠️ Il faut au moins 3 enregistrements pour effectuer une régression.")
    st.stop()

col1, col2 = st.columns(2)
with col1:
    choix_x = st.selectbox("Variable X (prédicteur)", [
        "Âge de l'étudiant",
        "Rang (numéro d'enregistrement)",
    ])
with col2:
    choix_y = st.selectbox("Variable Y (cible)", [
        "Note (/20)",
    ])

df_reg = df.copy().reset_index(drop=True)
df_reg["Rang"] = range(1, len(df_reg) + 1)

if "Âge" in choix_x:
    X = df_reg["Âge"].values.astype(float)
    xlabel = "Âge (années)"
else:
    X = df_reg["Rang"].values.astype(float)
    xlabel = "Rang (N° enregistrement)"

Y = df_reg["Note (/20)"].values.astype(float)

# ── Calcul analytique de la régression (moindres carrés ordinaires) ──
n     = len(X)
x_bar = X.mean()
y_bar = Y.mean()
Sxx   = np.sum((X - x_bar) ** 2)
Sxy   = np.sum((X - x_bar) * (Y - y_bar))

if Sxx == 0:
    st.error("Impossible de calculer la régression : variance de X nulle.")
    st.stop()

b1    = Sxy / Sxx
b0    = y_bar - b1 * x_bar
Y_hat = b0 + b1 * X

SS_tot = np.sum((Y - y_bar) ** 2)
SS_res = np.sum((Y - Y_hat) ** 2)
R2     = 1 - (SS_res / SS_tot) if SS_tot != 0 else 0
r      = np.sqrt(abs(R2)) * np.sign(b1)
rmse   = np.sqrt(SS_res / n)

# ── Graphique ──
fig_r, ax_r = plt.subplots(figsize=(10, 5))
ax_r.scatter(X, Y, color="#3b82f6", alpha=0.7, s=60, zorder=3, label="Observations")
x_line = np.linspace(X.min(), X.max(), 200)
y_line = b0 + b1 * x_line
ax_r.plot(x_line, y_line, color="#f5c842", linewidth=2.5,
          label=f"Ŷ = {b0:.2f} + {b1:.4f} · X")
ax_r.axhline(10, color="#f05252", linestyle="--", linewidth=1.2, alpha=0.7, label="Seuil réussite")
ax_r.set_xlabel(xlabel)
ax_r.set_ylabel("Note (/20)")
ax_r.set_ylim(0, 21)
ax_r.set_title("Nuage de points et droite de régression", pad=10)
ax_r.legend()
ax_r.grid(linestyle="--", alpha=0.4)
plt.tight_layout()
st.pyplot(fig_r)
plt.close(fig_r)

st.markdown("---")

# ── Tableau des résultats ──
st.subheader("📐 Résultats numériques de la régression")

if R2 > 0.8:
    qualite = "Excellent (R² > 0.8)"
elif R2 > 0.5:
    qualite = "Modéré (0.5 < R² ≤ 0.8)"
else:
    qualite = "Faible (R² ≤ 0.5)"

if abs(r) > 0.7:
    force_r = "forte"
elif abs(r) > 0.4:
    force_r = "modérée"
else:
    force_r = "faible"

direction = "positive ↗" if b1 > 0 else "négative ↘"

resultats = pd.DataFrame({
    "Paramètre": [
        "N (observations)",
        "Ordonnée à l'origine  β₀",
        "Pente  β₁",
        "Coefficient de corrélation  r",
        "Coefficient de détermination  R²",
        "RMSE (erreur quadratique moyenne)",
        "Qualité du modèle",
    ],
    "Valeur": [
        n,
        f"{b0:.4f}",
        f"{b1:.4f}",
        f"{r:.4f}",
        f"{R2:.4f}",
        f"{rmse:.4f}",
        qualite,
    ]
})
st.dataframe(resultats, use_container_width=True, hide_index=True)

st.markdown("---")
st.subheader("📝 Interprétation automatique")
st.markdown(f"""
```

- **Équation du modèle :** Ŷ = **{b0:.4f}** + **{b1:.4f}** × X
- **Sens de la relation :** La relation entre X et Y est **{direction}**.
- **R² = {R2:.4f}** → Le modèle explique **{R2*100:.1f} %** de la variabilité des notes.
- **r = {r:.4f}** → Corrélation **{force_r}** entre les deux variables.
- **RMSE = {rmse:.4f}** → L’erreur de prédiction moyenne du modèle est de **{rmse:.2f} points**.
  “””)

# ═════════════════════════════════════════════════════════════

# PAGE 5 — EXPORT DES DONNÉES

# ═════════════════════════════════════════════════════════════

elif page == “💾 Export des données”:

```
st.title("💾 Export des données")
st.markdown("Téléchargez vos données et les scripts d'analyse prêts à l'emploi.")
st.markdown("---")

df = get_df()

if df.empty:
    st.info("📭 Aucune donnée à exporter.")
    st.stop()

# ── CSV ──
st.subheader("📄 Format CSV")
buf_csv = io.StringIO()
df.to_csv(buf_csv, index=False, encoding="utf-8-sig")
st.download_button(
    label="⬇️ Télécharger CSV",
    data=buf_csv.getvalue().encode("utf-8-sig"),
    file_name="edutrack_performances.csv",
    mime="text/csv",
    use_container_width=True,
)

st.markdown("---")

# ── JSON ──
st.subheader("📦 Format JSON")
st.download_button(
    label="⬇️ Télécharger JSON",
    data=df.to_json(orient="records", force_ascii=False, indent=2).encode("utf-8"),
    file_name="edutrack_performances.json",
    mime="application/json",
    use_container_width=True,
)

st.markdown("---")

# ── Script R ──
st.subheader("📊 Script R — Analyse complète")
script_r = """\
```

# ═══════════════════════════════════════════════════

# EduTrack — Analyse des performances des étudiants

# INF 232 EC2 | Script R

# ═══════════════════════════════════════════════════

library(ggplot2)
library(dplyr)

# 1. Chargement des données

df <- read.csv(“edutrack_performances.csv”, encoding = “UTF-8”, stringsAsFactors = FALSE)
df$Note….20. <- as.numeric(df$Note….20.)
df$Age <- as.numeric(df$Age)

# 2. Statistiques descriptives

cat(”\n=== STATISTIQUES DESCRIPTIVES ===\n”)
print(summary(df$Note….20.))
cat(”\nEcart-type :”, sd(df$Note….20.), “\n”)
cat(“Variance   :”, var(df$Note….20.), “\n”)
cat(“Coefficient de variation (%) :”, sd(df$Note….20.) / mean(df$Note….20.) * 100, “\n”)

# 3. Taux de réussite

cat(”\nTaux de réussite (note >= 10) :”,
round(mean(df$Note….20. >= 10) * 100, 2), “%\n”)

# 4. Histogramme des notes

ggplot(df, aes(x = Note….20.)) +
geom_histogram(binwidth = 1, fill = “#3b82f6”, color = “#1e2d4a”, alpha = 0.85) +
geom_vline(aes(xintercept = mean(Note….20.)), color = “#f5c842”, linetype = “dashed”, size = 1) +
geom_vline(xintercept = 10, color = “#f05252”, linetype = “solid”, size = 1) +
labs(title = “Distribution des notes”, x = “Note (/20)”, y = “Effectif”) +
theme_minimal()

# 5. Moyenne par filière

df %>% group_by(Filiere) %>%
summarise(Moyenne = mean(Note….20.)) %>%
ggplot(aes(x = reorder(Filiere, Moyenne), y = Moyenne, fill = Moyenne >= 10)) +
geom_bar(stat = “identity”, alpha = 0.85) +
coord_flip() +
scale_fill_manual(values = c(“TRUE” = “#10d47e”, “FALSE” = “#f05252”)) +
labs(title = “Moyenne par filière”, x = “”, y = “Moyenne (/20)”) +
theme_minimal()

# 6. Régression linéaire simple

model <- lm(Note….20. ~ Age, data = df)
cat(”\n=== RÉGRESSION LINÉAIRE : Note ~ Age ===\n”)
print(summary(model))

ggplot(df, aes(x = Age, y = Note….20.)) +
geom_point(color = “#3b82f6”, alpha = 0.7) +
geom_smooth(method = “lm”, color = “#f5c842”, se = TRUE) +
geom_hline(yintercept = 10, color = “#f05252”, linetype = “dashed”) +
labs(title = “Régression linéaire : Note ~ Age”, x = “Age”, y = “Note (/20)”) +
theme_minimal()
“””
st.download_button(
label=“⬇️ Télécharger le script R”,
data=script_r.encode(“utf-8”),
file_name=“edutrack_analyse.R”,
mime=“text/plain”,
use_container_width=True,
)

```
st.markdown("---")

# ── Script Python ──
st.subheader("🐍 Script Python — Analyse complète")
script_py = """\
```

# ═══════════════════════════════════════════════════

# EduTrack — Analyse des performances des étudiants

# INF 232 EC2 | Script Python

# ═══════════════════════════════════════════════════

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error

# 1. Chargement des données

df = pd.read_csv(“edutrack_performances.csv”)
df[“Note (/20)”] = pd.to_numeric(df[“Note (/20)”])
df[“Âge”]        = pd.to_numeric(df[“Âge”])

# 2. Statistiques descriptives

print(”=== STATISTIQUES DESCRIPTIVES ===”)
print(df[“Note (/20)”].describe())
print(f”Écart-type         : {df[‘Note (/20)’].std():.4f}”)
print(f”Variance           : {df[‘Note (/20)’].var():.4f}”)
print(f”Coeff. variation   : {df[‘Note (/20)’].std() / df[‘Note (/20)’].mean() * 100:.2f} %”)
print(f”Taux de réussite   : {(df[‘Note (/20)’] >= 10).mean() * 100:.2f} %”)

# 3. Visualisation

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].hist(df[“Note (/20)”], bins=range(0, 22), color=”#3b82f6”, alpha=0.85, edgecolor=“white”)
axes[0].axvline(df[“Note (/20)”].mean(), color=”#f5c842”, linestyle=”–”, label=f”Moyenne : {df[‘Note (/20)’].mean():.2f}”)
axes[0].axvline(10, color=”#f05252”, linestyle=”-”, label=“Seuil réussite”)
axes[0].set_title(“Distribution des notes”)
axes[0].set_xlabel(“Note (/20)”)
axes[0].set_ylabel(“Effectif”)
axes[0].legend()

moy_filiere = df.groupby(“Filière”)[“Note (/20)”].mean().sort_values()
colors = [”#10d47e” if v >= 10 else “#f05252” for v in moy_filiere.values]
axes[1].barh(moy_filiere.index, moy_filiere.values, color=colors, alpha=0.85)
axes[1].axvline(10, color=”#f5c842”, linestyle=”–”, label=“Seuil réussite”)
axes[1].set_title(“Moyenne par filière”)
axes[1].set_xlabel(“Moyenne (/20)”)
axes[1].legend()
plt.tight_layout()
plt.show()

# 4. Régression linéaire simple

X = df[“Âge”].values.reshape(-1, 1)
y = df[“Note (/20)”].values
model = LinearRegression().fit(X, y)
y_pred = model.predict(X)

print(f”\n=== RÉGRESSION LINÉAIRE : Note ~ Âge ===”)
print(f”β₀ (intercept) : {model.intercept_:.4f}”)
print(f”β₁ (pente)     : {model.coef_[0]:.4f}”)
print(f”R²             : {r2_score(y, y_pred):.4f}”)
print(f”RMSE           : {np.sqrt(mean_squared_error(y, y_pred)):.4f}”)

plt.figure(figsize=(8, 5))
plt.scatter(df[“Âge”], df[“Note (/20)”], color=”#3b82f6”, alpha=0.7, label=“Observations”)
plt.plot(df[“Âge”].sort_values(), model.predict(df[“Âge”].sort_values().values.reshape(-1,1)),
color=”#f5c842”, linewidth=2, label=f”Droite : Ŷ = {model.intercept_:.2f} + {model.coef_[0]:.4f}·X”)
plt.axhline(10, color=”#f05252”, linestyle=”–”, alpha=0.7, label=“Seuil réussite”)
plt.xlabel(“Âge”)
plt.ylabel(“Note (/20)”)
plt.title(“Régression linéaire : Note ~ Âge”)
plt.legend()
plt.tight_layout()
plt.show()
“””
st.download_button(
label=“⬇️ Télécharger le script Python”,
data=script_py.encode(“utf-8”),
file_name=“edutrack_analyse.py”,
mime=“text/plain”,
use_container_width=True,
)

```
st.markdown("---")
st.subheader("👁️ Aperçu des données")
st.dataframe(df, use_container_width=True, height=300)
```
