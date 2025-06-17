from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import dash
from data import get_data

dash.register_page(__name__, path='/analyse-exploratoire', name='Analyse exploratoire')

# Charger les données
df = get_data()
df["date"] = pd.to_datetime(df["date"], errors='coerce')

# Layout de la page
def layout():
    return html.Div([
        html.H1("Analyse exploratoire des données", className="text-center mb-4"),

        dbc.Row([
            dbc.Col(dcc.Dropdown(
                id='filter-source',
                options=[{"label": s, "value": s} for s in sorted(df['source'].dropna().unique())],
                placeholder="Filtrer par source",
                multi=True
            ), md=4),
            dbc.Col(dcc.Dropdown(
                id='filter-theme',
                options=[{"label": r, "value": r} for r in sorted(df['theme'].dropna().unique())],
                placeholder="Filtrer par thème",
                multi=True
            ), md=4),
            dbc.Col(dcc.DatePickerRange(
                id='filter-date',
                start_date=df['date'].min(),
                end_date=df['date'].max(),
                display_format='YYYY-MM-DD'
            ), md=4)
        ], className="mb-4"),

        dbc.Row([
            dbc.Col(dbc.Card(dcc.Graph(id='bar-theme'), body=True), md=6),
            dbc.Col(dbc.Card(dcc.Graph(id='bar-source'), body=True), md=6),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col(dbc.Card(dcc.Graph(id='evol-source'), body=True), md=6),
            dbc.Col(dbc.Card([
                dcc.Dropdown(
                    id='theme-evol-selector',
                    options=[{"label": r, "value": r} for r in sorted(df['theme'].dropna().unique())],
                    value=[df['theme'].dropna().unique()[0]],
                    multi=True,
                    clearable=False
                ),
                dcc.Graph(id='evol-theme')
            ], body=True), md=6),
        ])
    ])

# Callback pour les graphiques principaux
@callback(
    Output("bar-theme", "figure"),
    Output("bar-source", "figure"),
    Output("evol-source", "figure"),
    Input("filter-source", "value"),
    Input("filter-theme", "value"),
    Input("filter-date", "start_date"),
    Input("filter-date", "end_date")
)
def update_graphs(sources, themes, start_date, end_date):
    dff = df.copy()
    if sources:
        dff = dff[dff['source'].isin(sources)]
    if themes:
        dff = dff[dff['theme'].isin(themes)]
    dff = dff[(dff['date'] >= start_date) & (dff['date'] <= end_date)]

    # Bar chart par thème
    fig1_data = dff['theme'].value_counts().reset_index()
    fig1_data.columns = ['Thème', 'Nombre d’articles']
    fig1 = px.bar(fig1_data, x='Thème', y='Nombre d’articles',
                  title="Nombre d'articles par thème")

    # Bar chart par source
    fig2_data = dff['source'].value_counts().reset_index()
    fig2_data.columns = ['Source', 'Nombre d’articles']
    fig2 = px.bar(fig2_data, x='Source', y='Nombre d’articles',
                  title="Nombre d'articles par source")

    # Courbe par source
    dff['Date'] = dff['date'].dt.date
    pivot = dff.groupby(['Date', 'source']).size().unstack(fill_value=0)
    df_long = pivot.reset_index().melt(id_vars='Date', var_name='Source', value_name='Nombre d’articles')

    fig3 = px.line(df_long, x='Date', y='Nombre d’articles', color='Source',
                   markers=True,
                   title="Nombre d'articles par jour et par source",
                   labels={'Date': 'Date', 'Nombre d’articles': 'Nombre d’articles', 'Source': 'Source'})
    fig3.update_traces(mode='lines+markers')

    return fig1, fig2, fig3

# Callback pour le graphique d’évolution des thèmes
@callback(
    Output("evol-theme", "figure"),
    Input("theme-evol-selector", "value"),
    Input("filter-date", "start_date"),
    Input("filter-date", "end_date"),
    Input("filter-source", "value"),
)
def update_theme_evol(selected_themes, start_date, end_date, sources):
    dff = df.copy()
    if sources:
        dff = dff[dff['source'].isin(sources)]
    dff = dff[(dff['date'] >= start_date) & (dff['date'] <= end_date)]
    dff['Date'] = dff['date'].dt.date

    # Si un seul thème est sélectionné
    if isinstance(selected_themes, str):
        selected_themes = [selected_themes]

    dff = dff[dff['theme'].isin(selected_themes)]
    evol = dff.groupby(['Date', 'theme']).size().reset_index(name='Nombre d’articles')

    fig = px.line(evol, x='Date', y='Nombre d’articles', color='theme',
                  markers=True,
                  title="Évolution des articles selon les thèmes sélectionnés",
                  labels={'Date': 'Date', 'Nombre d’articles': 'Nombre d’articles', 'theme': 'Thème'})
    fig.update_traces(mode='lines+markers')
    return fig
