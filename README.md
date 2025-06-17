# <center>École nationale de la statistique et de l'analyse économique (ENSAE) - Pierre NDIAYE</center>
## <center>Application Dash - Interface de Visualisation</center>
### <center>📊 Plateforme d'analyse des tendances médiatiques sénégalaises</center>

<center>Réalisé par :</center>  
<center><strong>Ahmed Firhoun OUMAROU SOULEYE</strong></center>  
<center><strong>Mamadou Saïdou DIALLO</strong></center>  
<center><em>Étudiants en AS3 - Option Data Science</em></center>

<center>Cours tenu par :</center>  
<center><strong>M. Baye Demba DIACK</strong></center>  
<center><em>Chef du Bureau des Données et des Solutions informatique (BDSI)</em></center>  
<center>Année académique 2024-2025</center>


## 🎯 Description

Cette application Dash constitue l'interface utilisateur interactive du projet d'analyse des tendances médiatiques sénégalaises. Elle permet de visualiser les résultats du Topic Modeling LDA appliqué aux articles collectés depuis SeneWeb et Senego.

### ✨ Fonctionnalités principales
- 🏠 **Page d'accueil** avec présentation du projet
- 📈 **Analyse exploratoire** des données collectées
- 🔍 **Recherche d'articles** avec filtres avancés
- 🧠 **Visualisation des topics** identifiés par LDA
- 📊 **Graphiques interactifs** avec Plotly
- 📱 **Interface responsive** et moderne

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

### ☁️ Déploiement sur Render

Cette application est configurée pour être déployée automatiquement sur **Render**.


## 🚀 Démo en Ligne

🌐 **Application déployée** : [https://sene-scraper.onrender.com](https://sene-scraper.onrender.com)


