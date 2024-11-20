# app.py

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from callbacks import register_callbacks
from firebase_service import fetch_users_cached, fetch_reservations_cached, fetch_rooms_cached
from test import *

# Fetch data once and cache it globally
cached_users = fetch_users()#fetch_users_cached()
cached_reservations = fetch_reservations()#fetch_reservations_cached()
cached_rooms = fetch_rooms()#fetch_rooms_cached()


# Dash app initialization with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# Register callbacks
register_callbacks(app,cached_users,cached_reservations,cached_rooms)

# Layout of the app
app.layout = dbc.Container([
    dcc.Location(id='url', refresh=False),  # Tracks the URL for navigation
    dbc.Row([
        dbc.Col([  # Sidebar
            html.H2("Menu", className="text-white p-3"),
            dbc.Nav([
                dbc.NavLink("Strona Główna", href="/", active="exact", className="nav-link"),
                dbc.NavLink("Zarządzanie Użytkownikami", href="/users", active="exact", className="nav-link"),
                dbc.NavLink("Zarządzanie Rolami", href="/roles", active="exact", className="nav-link"),
                dbc.NavLink("Zarządzanie Rezerwacjami",href="/reservations", active="exact", className="nav-link"),
            ], vertical=True, pills=True, className="bg-dark"),
        ], width=2, className="bg-dark vh-200 p-0"),  # Sidebar width adjustment

        dbc.Col([
            html.Div(id="page-content", className="content p-4")
        ], width=10),
    ], className="vh-100"),
], fluid=True)

if __name__ == '__main__':
    app.run_server(debug=True)
