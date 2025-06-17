import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash import page_container, page_registry
from dash import dcc, html, Input, Output, State, callback, dash_table
import pandas as pd
import io
import base64

#-- Création de l'application Dash avec configuration multi-pages
app = dash.Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)
server = app.server

#-- Creation de la mise en page de l'application avec un menu
# de navigation et un stockage de données et des variables sélectionnées
# pour l'analyse factorielle discriminante
app.layout = html.Div([
    dbc.Navbar(
            dbc.Container([
                dbc.NavbarBrand("SENE SCRAPPER", href="/"),
                dbc.Nav(
                    [dbc.NavLink(p["name"], href=p["path"], active="exact")
                     for p in page_registry.values()],
                    navbar=True, className="ml-auto"
                ),
            ]),
            color="dark", dark=True,
            className="shadow",
            fixed="top"  # ✅ Fixe la barre en haut
        ),

        html.Div(
            page_container,
            style={"flex": "1", "marginTop": "70px", "marginBottom": "60px", "padding": "1rem"}
        ),

        html.Footer(
            dbc.Container(
                html.P("© 2025 - Application SENE SCRAPPER développée par Mamadou Saidou Diallo et Ahmed Firhoun Oumarou Souleye", className="text-center text-light mb-0"),
                className="py-3"
            ),
            style={
                "backgroundColor": "#343a40",
                "position": "fixed",
                "bottom": 0,
                "width": "100%",
                "zIndex": 1030
            }
        )
    ],
    style={"display": "flex", "flexDirection": "column", "minHeight": "100vh"}
)

if __name__ == "__main__":
    app.run_server(debug=True)
