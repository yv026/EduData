🎓 EduData — Application de collecte et d'analyse des performances des étudiants

> Cours : INF 232 EC2 — Analyse de données  
> Langage : Python |Framework : Streamlit  
> Domain : Éducation — Suivi académique des étudiants

---

📌 Description du projet

EduData est une application web interactive développée en Python avec le framework Streamlit. Elle permet de :

- Collecte les résultats académiques des étudiants via un formulaire structuré
- Stocker les données dans une base de données en session
- Analyser les performances à travers des statistiques descriptives complètes
-Visualise les données sous forme de graphiques professionnels
- Modéliser la relation entre variables via la régression linéaire simple
- Exporter les données et les scripts d'analyse (CSV, JSON, R, Python)

---

🎯 Objectifs pédagogiques

Ce projet couvre les thématiques du cours INF 232 EC2 :

| Thématique | Couverture dans l'application |
|---|---|
| Collecte de données | Formulaire de saisie des notes et informations étudiantes |
| Analyse descriptive | Moyenne, médiane, mode, écart-type, variance, quartiles, CV, skewness, kurtosis |
| Visualisation | Histogramme, diagramme circulaire, boxplot, barres, nuage de points |
| Régression linéaire simple | Calcul analytique de β₀, β₁, R², r, RMSE |
| Export | CSV, JSON, scripts R et Python prêts à l'emploi |

---
 🗂️ Structure du projet

```
edutrack/
│
├── app.py               Application principale Streamlit
├── requirements.txt     Dépendances Python
└── README.md             Documentation du projet
```

---

⚙️ Installation et exécution en local
 Prérequis
- Python 3.9 ou supérieur
- pip

 Étapes

```bash
 1. Cloner le dépôt
git clone https://github.com/votre-username/edutrack.git
cd edutrack

 2. Installer les dépendances
pip install -r requirements.txt

 3. Lancer l'application
streamlit run app.py
```

L'application s'ouvre automatiquement sur `http://localhost:8501`

---

 🚀 Déploiement en ligne (Streamlit Cloud)

1. Pousser le projet sur GitHub
2. Aller sur [share.streamlit.io](https://share.streamlit.io)
3. Connecter le compte GitHub
4. Sélectionner le dépôt et le fichier `app.py`
5. Cliquer sur Deploy

---

📦 Dépendances

```
streamlit==1.35.0
pandas==2.2.2
numpy==1.26.4
matplotlib==3.9.0
scikit-learn==1.5.0
```

---

📋 Fonctionnalités détaillées

📥 Page 1 — Saisie des données
Formulaire complet permettant de saisir :
- Identité de l'étudiant (Nom, Prénom, Matricule)
- Informations académiques (Filière, Niveau, Matière, Semestre, Année)
- Résultat (Note sur 20)
- Informations personnelles (Sexe, Âge)

Validation des champs obligatoires avec messages d'erreur explicites.

📋 Page 2 — Base de données
- Affichage de tous les enregistrements dans un tableau interactif
- Filtres par Filière, Niveau, Matière et Année académique
- Calcul automatique de la mention (Très Bien, Bien, Assez Bien, Passable, Insuffisant)
- Suppression de la base de données

 📊 Page 3 — Analyse descriptive
Indicateurs statistiques calculés :
- Effectif (N)
- Moyenne arithmétique
- Médiane
- Mode
- Minimum et Maximum
- Étendue
- Écart-type et Variance
- Coefficient de variation (%)
- Quartiles Q1 et Q3
- Intervalle interquartile (IQR)
- Asymétrie (Skewness)
- Aplatissement (Kurtosis)

Graphiques produits :
1. Histogramme de distribution des notes
2. Diagramme circulaire des mentions
3. Boîte à moustaches (boxplot) par filière
4. Diagramme en barres des moyennes par matière
5. Comparaison des performances par sexe

📈 Page 4 — Régression linéaire simple
Modélisation analytique par la méthode des moindres carrés ordinaires (MCO) :

```
Ŷ = β₀ + β₁ · X
```

Paramètres calculés :
- β₀ : ordonnée à l'origine
- β₁ : pente de la droite
- r : coefficient de corrélation de Pearson
- R² : coefficient de détermination
- RMSE : erreur quadratique moyenne

Interprétation automatique de la qualité et du sens du modèle.

 💾 Page 5 — Export des données
- CSV: compatible Excel, pandas, R
- JSON : format structuré pour APIs
- Script R: analyse complète avec ggplot2
- Script Python : analyse avec pandas, matplotlib et scikit-learn

---

📊 Données de démonstration

L'application est préchargée avec **40 enregistrements de démonstration** générés aléatoirement (seed fixe pour la reproductibilité) couvrant plusieurs filières, niveaux et matières.

---
👨‍💻 Technologies utilisées

| Technologie | Usage |
|---|---|
| Python 3.9+ | Langage principal |
| Streamlit | Interface web interactive |
| Pandas | Manipulation des données |
| NumPy | Calculs numériques et statistiques |
| Matplotlib | Visualisations graphiques |
| Scikit-learn | Régression linéaire (export uniquement) |

---

 📧 cContact

Projet soumis à : rollinfrancis28@gmail.com
