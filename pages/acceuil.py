from plotly.figure_factory import create_distplot
import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import dash_table

dash.register_page(__name__, path='/', name='Accueil')


def layout():
    return html.Div([
        html.H1("Accueil", className="text-center mb-4"),
        html.Div([
            html.Div([
                html.Img(src="/assets/ansd_logo.png", style={"width": "150px", "height": "auto", "margin": "0 auto"}),
                html.P("Agence nationale de la Statistique et de la Démographie (ANSD)",
                       className="text-center mt-2", style={"color": "#1a3c6d", "font-weight": "500"})
            ], className="col-md-6 text-center"),
            html.Div([
                html.Img(src="/assets/ensae_logo.png", style={"width": "150px", "height": "auto", "margin": "0 auto"}),
                html.P("École nationale de la Statistique et de l’Analyse économique - Pierre NDIAYE (ENSAE)",
                       className="text-center mt-2", style={"color": "#1a3c6d", "font-weight": "500"})
            ], className="col-md-6 text-center")
        ], className="row mb-4 justify-content-center"),
        html.Div([
            html.H3("Projet de Web Scraping", className="text-center mb-2",
                    style={"color": "#1a3c6d", "font-weight": "600"}),
            html.H4("Projet 4 : Analyse des tendances médiatiques, topic modeling", className="text-center mb-4",
                    style={"color": "#333", "font-style": "italic"}),
            html.P("Rédigé par :", className="text-center mb-2", style={"font-weight": "500"}),
            html.P("Ahmed Firhoun OUMAROU SOULEYE", className="text-center mb-1"),
            html.P("Mamadou Saïdou DIALLO", className="text-center mb-3"),
            html.P("Étudiants en AS3 Option Data Science", className="text-center mb-4"),
            html.P("Cours tenu par :", className="text-center mb-2", style={"font-weight": "500"}),
            html.P("M. Baye Demba DIACK", className="text-center mb-1",
                   style={"color": "#1a3c6d", "font-weight": "600"}),
            html.P("Chef du Bureau des Données et des Solutions informatique (BDSI)", className="text-center mb-3"),
            html.P("Année académique 2024-2025", className="text-center", style={"font-style": "italic"})
        ], className="text-center")
    ], style={"padding": "2rem", "background-color": "#ffffff", "border-radius": "10px",
              "box-shadow": "0 4px 12px rgba(0, 0, 0, 0.05)"})