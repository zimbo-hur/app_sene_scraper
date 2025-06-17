# <center>École nationale de la statistique et de l'analyse économique (ENSAE) - Pierre NDIAYE</center>
## <center>Application Dash - Interface de Visualisation</center>
### <center>📊 Plateforme d'analyse des tendances médiatiques sénégalaises</center>

<center>Réalisé par :</center>  
<center><strong>Ahmed Firhoun OUMAROU SOULEYE</strong></center>  
<center><strong>Mamadou Saïdou DIALLO</strong></center>  
<center><em>Étudiants en AS3 - Option Data Science</em></center>

<br>

<center>Cours tenu par :</center>  
<center><strong>M. Baye Demba DIACK</strong></center>  
<center><em>Chef du Bureau des Données et des Solutions informatique (BDSI)</em></center>

<br>

<center>Année académique 2024-2025</center>

---

> Interface web interactive pour visualiser et explorer les tendances des actualités sénégalaises analysées par Topic Modeling

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/downloads/)
[![Dash](https://img.shields.io/badge/Dash-2.14+-red.svg)](https://dash.plotly.com/)
[![Render](https://img.shields.io/badge/Deploy-Render-46E3B7.svg)](https://render.com/)
[![Live Demo](https://img.shields.io/badge/Demo-Live-brightgreen.svg)](https://sene-scraper.onrender.com)

## 🎯 Description

Cette application Dash constitue l'interface utilisateur interactive du projet d'analyse des tendances médiatiques sénégalaises. Elle permet de visualiser les résultats du Topic Modeling LDA appliqué aux articles collectés depuis SeneWeb et Senego.

### ✨ Fonctionnalités principales
- 🏠 **Page d'accueil** avec présentation du projet
- 📈 **Graphiques interactifs** des tendances temporelles
- 🔍 **Filtrages avancés** par date, source et rubrique
- 🧠 **Visualisation des topics** identifiés par LDA
- ☁️ **Nuage de mots** et mots les plus fréquents par topic
- 🔎 **Recherche d'articles** par titre, contenu, catégorie et date de publication
- 📱 **Interface responsive** et moderne

🌐 **Application déployée** : [https://sene-scraper.onrender.com](https://sene-scraper.onrender.com)

## 🏗️ Architecture de l'Application

```
├── 📱 app.py                      # Application principale Dash
├── 🔧 data.py                     # Gestion des données et modèles
├── 📋 requirements.txt            # Dépendances Python
├── assets/                        # Ressources statiques
│   ├── 🏛️ ansd_logo.png          # Logo ANSD
│   ├── 🎓 ensae_logo.png         # Logo ENSAE
│   └── 🎨 style.css              # Styles personnalisés
├── pages/                         # Pages de l'application
│   ├── 🏠 accueil.py             # Page d'accueil
│   ├── 📊 Analyse_exploratoire.py # Analyse des données
│   ├── 🔍 Recherche_d_article.py # Moteur de recherche
│   └── 🧠 Topic_modeling.py      # Visualisation LDA
└── __pycache__/                   # Cache Python (auto-généré)
```

## 🚀 Installation et Déploiement

### 🔧 Installation locale

#### Prérequis
- Python 3.12+
- Git

#### Étapes d'installation
```bash
# Cloner le dépôt
git clone https://github.com/zimbo-hur/app_sene_scraper.git
cd app_sene_scraper

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python app.py
```

L'application sera accessible en local.

### ☁️ Déploiement sur Render

Cette application est configurée pour être déployée automatiquement sur **Render**.


## 🛠️ Technologies Utilisées

### Frontend & Visualisation
- **Dash/Plotly** - Framework web et graphiques interactifs
- **Dash Bootstrap Components** - Composants UI modernes
- **HTML/CSS** - Structure et style personnalisés

### Backend & Data Science
- **Python 3.12** - Langage principal
- **Scikit-learn** - Algorithme LDA pour Topic Modeling
- **NLTK** - Traitement du langage naturel
- **WordCloud** - Génération de nuages de mots
- **Pandas** - Manipulation des données
- **Joblib** - Chargement des modèles sauvegardés
- **Optuna** - Optimisation des hyperparamètres

### Infrastructure & Déploiement
- **GitHub** - Contrôle de version
- **GitHub Actions** - Automatisation
- **Render** - Plateforme de déploiement cloud

## 🚀 Démo en Ligne

🌐 **Application déployée** : [https://sene-scraper.onrender.com](https://sene-scraper.onrender.com)

### 🎨 Interface Utilisateur

**Fonctionnalités :**
- **Graphiques dynamiques** : Tendances temporelles (fréquence de publications), répartition des articles par rubriques...
- **Filtrages** : Par date, source et rubrique
- **Recherche intelligente** : Articles par titre, contenu, catégorie et date
- **Visualisation des topics** : Nuages de mots interactifs

## 🏫 Contexte Académique

Ce projet s'inscrit dans le cadre du cours de Web Scraping dispensé par M. Baye Demba DIACK, Chef du Bureau des Données et des Solutions informatique (BDSI) à l'Agence nationale de la Statistique et de la Démographie (ANSD).
