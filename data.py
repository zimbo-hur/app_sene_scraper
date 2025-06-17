import pandas as pd
import dateparser
import requests
import joblib
import os
import nltk
import re
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from wordcloud import STOPWORDS
from unidecode import unidecode

# Télécharger les stopwords français (si nécessaire)
nltk.download('stopwords')

# Fusion de stopwords : WordCloud, NLTK, sklearn + personnalisés
custom_stopwords = set(STOPWORDS)
custom_stopwords.update(stopwords.words('french'))
custom_stopwords.update(ENGLISH_STOP_WORDS)
custom_stopwords.update([
    'selon', 'ce', 'cet', 'cette', 'dont', 'ainsi', 'hgroupe', 'ete', 'aussi', 'field', 'plus',
    'dun', 'dune', 'cest', 'comme', 'juin', 'apres', 'deux', 'senegal', 'senegalais', 'juingroupe',
    'sest', 'lors', 'egalement', 'sans', 'notamment', 'quil', 'tout', 'tous', 'fait', 'entre',
    'titre', 'plusieurs', 'sous', 'faire', 'bien', 'meme', 'avant', 'toujours', 'cela', 'face', 'tres',
    'leur', 'leurs', 'toute', 'toutes', 'vers', 'quelle', 'jai', 'etait', 'etais', 'senegalaise',
    'alors', 'encore', 'avoir', 'nest', 'etre',
])

def preprocess(text):
    text = str(text).lower()
    text = unidecode(text)
    text = text.replace("'", " ")
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    tokens = text.split()
    tokens = [word for word in tokens if word not in custom_stopwords and len(word) > 2]
    return ' '.join(tokens)

def parse_mixed_datetime(date_str):
    return dateparser.parse(date_str, languages=['fr'])

def get_data():
    url = 'https://raw.githubusercontent.com/zimbo-hur/sene-scraper/refs/heads/master/articles_scraped.csv'

    # Lecture du fichier CSV
    df = pd.read_csv(
        url,
        sep=',',
        quotechar='"',
        encoding='utf-8',
        on_bad_lines='skip'
    )

    # Traitement des dates
    if 'date' in df.columns:
        df['date'] = df['date'].apply(parse_mixed_datetime)

    if 'date_parsed' in df.columns:
        df['date_parsed'] = df['date_parsed'].apply(parse_mixed_datetime)
        df.drop(columns=['date_parsed'], inplace=True)

    # Suppression des lignes sans contenu
    if 'contenu' in df.columns:
        df = df.dropna(subset=['contenu'])

        # Application du prétraitement
        df['cleaned_content'] = df['contenu'].apply(preprocess)

    return df

def load_lda_model(model_url, vectorizer_url, model_path="lda_model.joblib", vectorizer_path="vectorizer.joblib"):
    """
    Télécharge et charge un modèle LDA et son vectorizer.

    Arguments :
        model_url (str)       : URL GitHub raw du modèle LDA .joblib
        vectorizer_url (str)  : URL GitHub raw du vectorizer .joblib
        model_path (str)      : Chemin local pour enregistrer le modèle
        vectorizer_path (str) : Chemin local pour enregistrer le vectorizer

    Retourne :
        (lda_model, vectorizer)
    """
    def download(url, path):
        if not os.path.exists(path):
            r = requests.get(url)
            if r.status_code == 200:
                with open(path, "wb") as f:
                    f.write(r.content)
            else:
                raise Exception(f"Erreur lors du téléchargement : {url} (code {r.status_code})")

    download(model_url, model_path)
    download(vectorizer_url, vectorizer_path)

    lda_model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)

    return lda_model, vectorizer
