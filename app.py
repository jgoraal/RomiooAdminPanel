# app.py

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

from layouts import dashboard_layout, user_management_layout
from callbacks import register_callbacks

# Dash app initialization with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# Register callbacks
register_callbacks(app)

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
        ], width=2, className="bg-dark vh-100 p-0"),  # Sidebar width adjustment

        dbc.Col([
            html.Div(id="page-content", className="content p-4")
        ], width=10),
    ], className="vh-100"),
], fluid=True)

if __name__ == '__main__':
    app.run_server(debug=True)
