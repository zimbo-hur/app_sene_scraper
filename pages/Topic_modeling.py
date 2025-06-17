from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import dash
import base64
from io import BytesIO

from data import get_data, load_lda_model

dash.register_page(__name__, path='/topic-modeling', name='Topic modeling')

# Chargement des données
df = get_data()

# Chargement des modèles
lda_model, vectorizer = load_lda_model(
    model_url="https://raw.githubusercontent.com/zimbo-hur/sene-scraper/master/models/best_lda_model.joblib",
    vectorizer_url="https://raw.githubusercontent.com/zimbo-hur/sene-scraper/master/models/vectorizer.joblib"
)

# Prédiction des topics (clusters)
if 'topic' not in df.columns:
    dtm = vectorizer.transform(df['cleaned_content'])
    df['topic'] = lda_model.transform(dtm).argmax(axis=1)

# Layout
def layout():
    return html.Div([
        html.H1("Analyse thématique (Topic Modeling)", className="text-center mb-4"),

        dbc.Row([
            dbc.Col(dcc.Dropdown(
                id='filter-source-tm',
                options=[{"label": s, "value": s} for s in sorted(df['source'].dropna().unique())],
                placeholder="Filtrer par source",
                multi=True
            ), md=4),
            dbc.Col(dcc.Dropdown(
                id='filter-theme-tm',
                options=[{"label": r, "value": r} for r in sorted(df['theme'].dropna().unique())],
                placeholder="Filtrer par rubrique",
                multi=True
            ), md=4),
            dbc.Col(dcc.DatePickerRange(
                id='filter-date-tm',
                start_date=df['date'].min(),
                end_date=df['date'].max(),
                display_format='YYYY-MM-DD'
            ), md=4)
        ], className="mb-4"),

        dbc.Row([
            dbc.Col(dbc.Card(dcc.Graph(id='freq-words-global'), body=True), md=6),
            dbc.Col(dbc.Card(html.Img(id='wordcloud-global', style={"width": "100%"}), body=True), md=6),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col(dbc.Card(dcc.Graph(id='topic-summary'), body=True), md=6),
            dbc.Col(dbc.Card([
                dcc.Dropdown(id='topic-selector-bar', placeholder="Choisir un topic", value=0),
                dcc.Graph(id='words-by-topic')
            ], body=True), md=6),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col(dbc.Card([
                dcc.Dropdown(id='topic-selector-cloud', placeholder="Choisir un topic", value=0),
                html.Img(id='wordcloud-by-topic', style={"width": "100%"})
            ], body=True), md=6),
            dbc.Col(dbc.Card(dcc.Graph(id='topic-vs-theme'), body=True), md=6),
        ])
    ])

# Callback principal
@callback(
    Output('freq-words-global', 'figure'),
    Output('wordcloud-global', 'src'),
    Output('topic-summary', 'figure'),
    Output('topic-selector-bar', 'options'),
    Output('topic-selector-cloud', 'options'),
    Output('words-by-topic', 'figure'),
    Output('wordcloud-by-topic', 'src'),
    Output('topic-vs-theme', 'figure'),
    Input('filter-source-tm', 'value'),
    Input('filter-theme-tm', 'value'),
    Input('filter-date-tm', 'start_date'),
    Input('filter-date-tm', 'end_date'),
    Input('topic-selector-bar', 'value'),
    Input('topic-selector-cloud', 'value')
)
def update_all(source, theme, start, end, topic_bar, topic_cloud):
    dff = df.copy()

    if source:
        dff = dff[dff['source'].isin(source)]
    if theme:
        dff = dff[dff['theme'].isin(theme)]
    dff = dff[(dff['date'] >= start) & (dff['date'] <= end)]

    # 1. Diagramme des mots fréquents
    word_freq = dff['cleaned_content'].str.split().explode().value_counts().head(20).reset_index()
    word_freq.columns = ['Mot', 'Fréquence']
    fig_freq = px.bar(word_freq, x='Mot', y='Fréquence', title="Mots les plus fréquents")

    # 2. Nuage de mots global
    text = " ".join(dff['cleaned_content'].dropna())
    wc = WordCloud(width=800, height=400, background_color="white").generate(text)
    buffer = BytesIO()
    wc.to_image().save(buffer, format="PNG")
    cloud_global = base64.b64encode(buffer.getvalue()).decode()

    # 3. Résumé des topics
    summary = dff.groupby('topic').agg(
        Nombre_articles=('cleaned_content', 'count'),
        Longueur_moyenne=('cleaned_content', lambda x: x.str.split().str.len().mean())
    ).reset_index()
    summary['Proportion (%)'] = (summary['Nombre_articles'] / summary['Nombre_articles'].sum()) * 100
    fig_summary = px.bar(summary, x='topic', y='Nombre_articles',
                         hover_data=['Proportion (%)', 'Longueur_moyenne'],
                         title="Résumé des Topics",
                         labels={'topic': 'Topic'})

    # 4. Diagramme des mots par topic
    top_words = dff[['topic', 'cleaned_content']].copy()
    top_words['tokens'] = top_words['cleaned_content'].str.split()
    exploded = top_words.explode('tokens')
    top_by_topic = exploded.groupby(['topic', 'tokens']).size().reset_index(name='count')
    topic_options = [{'label': f'Topic {int(i)}', 'value': int(i)} for i in sorted(top_by_topic['topic'].unique())]
    filtered_words = top_by_topic[top_by_topic['topic'] == topic_bar].sort_values('count', ascending=False).head(15)
    fig_words_topic = px.bar(filtered_words, x='tokens', y='count',
                             title=f"Mots fréquents - Topic {topic_bar}",
                             labels={'tokens': 'Mot', 'count': 'Fréquence'})

    # 5. Wordcloud par topic
    topic_text = " ".join(exploded[exploded['topic'] == topic_cloud]['tokens'].dropna())
    wc_topic = WordCloud(width=800, height=400, background_color="white").generate(topic_text)
    buffer2 = BytesIO()
    wc_topic.to_image().save(buffer2, format="PNG")
    cloud_topic = base64.b64encode(buffer2.getvalue()).decode()

    # 6. Croisement Topic / Thème : forcer topic en type str
    dff['topic'] = dff['topic'].astype(str)
    fig_tvstheme = px.histogram(dff, x='topic', color='theme', barmode='group',
                                title="Croisement Topic / Rubrique",
                                labels={'topic': 'Topic', 'theme': 'Rubrique'})

    return (
        fig_freq,
        f"data:image/png;base64,{cloud_global}",
        fig_summary,
        topic_options,
        topic_options,
        fig_words_topic,
        f"data:image/png;base64,{cloud_topic}",
        fig_tvstheme
    )
