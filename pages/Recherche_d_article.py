from dash import dcc, html, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import dash
from data import get_data

dash.register_page(__name__, path="/recherche-article", name="Recherche d'article")

# Chargement des données
df = get_data()
df["date"] = pd.to_datetime(df["date"], errors='coerce')

# Layout
def layout():
    return html.Div([
        html.H1("Recherche d'article", className="text-center mb-4"),

        dbc.Row([
            dbc.Col(dcc.Input(
                id='search-bar',
                type='text',
                placeholder='Rechercher un mot-clé (titre, contenu ou thème)...',
                debounce=True,
                style={'width': '100%'}
            ), md=6),
            dbc.Col(dcc.Dropdown(
                id='filter-source-search',
                options=[{'label': s, 'value': s} for s in sorted(df['source'].dropna().unique())],
                placeholder='Filtrer par source',
                multi=True
            ), md=3),
            dbc.Col(dcc.Dropdown(
                id='filter-theme-search',
                options=[{'label': t, 'value': t} for t in sorted(df['theme'].dropna().unique())],
                placeholder='Filtrer par rubrique',
                multi=True
            ), md=3),
        ], className="mb-3"),

        dbc.Row([
            dbc.Col(dcc.DatePickerRange(
                id='filter-date-search',
                start_date=df['date'].min(),
                end_date=df['date'].max(),
                display_format='YYYY-MM-DD'
            ), md=4),
        ], className="mb-4"),

        dash_table.DataTable(
            id='search-results-table',
            columns=[
                {'name': 'Titre', 'id': 'titre', 'type': 'text'},
                {'name': 'Rubrique', 'id': 'theme', 'type': 'text'},
                {'name': 'Source', 'id': 'source', 'type': 'text'},
                {'name': 'Date', 'id': 'date', 'type': 'datetime'},
                {'name': 'URL', 'id': 'url', 'type': 'text', 'presentation': 'markdown'}
            ],
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left'},
            style_header={'fontWeight': 'bold'},
            page_size=15,
        )
    ])


@callback(
    Output('search-results-table', 'data'),
    Input('search-bar', 'value'),
    Input('filter-source-search', 'value'),
    Input('filter-theme-search', 'value'),
    Input('filter-date-search', 'start_date'),
    Input('filter-date-search', 'end_date')
)
def update_search_results(query, sources, themes, start_date, end_date):
    dff = df.copy()

    # Filtres
    if sources:
        dff = dff[dff['source'].isin(sources)]
    if themes:
        dff = dff[dff['theme'].isin(themes)]
    dff = dff[(dff['date'] >= start_date) & (dff['date'] <= end_date)]

    # Recherche par mot-clé
    if query and query.strip():
        query = query.lower()
        dff = dff[
            dff['titre'].str.lower().str.contains(query, na=False) |
            dff['contenu'].str.lower().str.contains(query, na=False) |
            dff['theme'].str.lower().str.contains(query, na=False)
        ]

    # Rendu du tableau
    results = dff[['titre', 'theme', 'source', 'date', 'url']].copy()
    results['url'] = results['url'].apply(lambda u: f"[Ouvrir]({u})" if pd.notnull(u) else "")
    return results.to_dict('records')
