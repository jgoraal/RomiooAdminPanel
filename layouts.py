# layouts.py


import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table

from test import fetch_users

# Dashboard layout
dashboard_layout = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Łączna liczba użytkowników"),
                dbc.CardBody(html.H4(id="total-users", className="card-title text-center"))
            ], className="shadow-sm mb-4"),
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Liczba potwierdzonych emaili"),
                dbc.CardBody(html.H4(id="verified-emails", className="card-title text-center"))
            ], className="shadow-sm mb-4"),
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Łączna liczba rezerwacji"),
                dbc.CardBody(html.H4(id="total-reservations", className="card-title text-center"))
            ], className="shadow-sm mb-4"),
        ], width=4),
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='user-growth-graph')
        ], width=12),
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='reservations-over-time-graph')
        ], width=12),
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='user-roles-graph')
        ], width=6),
        dbc.Col([
            dcc.Graph(id='reservation-statuses-graph')
        ], width=6)
    ]),

    html.H2("Top 10 najbardziej aktywnych użytkowników", className="mt-4 text-center"),
    dash_table.DataTable(
        id='top-users-table',
        columns=[
            {'name': 'Nazwa użytkownika', 'id': 'username'},
            {'name': 'Email', 'id': 'email'},
            {'name': 'Liczba rezerwacji', 'id': 'Liczba rezerwacji'}
        ],
        # Dane zostaną ustawione przez callback
        style_table={'overflowX': 'auto'},
        style_header={'backgroundColor': '#f8f9fa', 'fontWeight': 'bold'},
        style_cell={'textAlign': 'center', 'padding': '10px'},
        style_as_list_view=True,
        page_size=10  # Dodano paginację
    ),

    html.H2("Lista wszystkich użytkowników", className="mt-4 text-center"),
    dash_table.DataTable(
        id='user-table',
        columns=[
            {'name': 'Nazwa', 'id': 'username'},
            {'name': 'Email', 'id': 'email'},
            {'name': 'Potwierdzony', 'id': 'verified'},
            {'name': 'Rola', 'id': 'role'},
            {'name': 'Ostatnio Widziany', 'id': 'lastSeen'},
            {'name': 'Stworzone', 'id': 'created'}
        ],
        # Dane zostaną ustawione przez callback
        style_table={'overflowX': 'auto'},
        style_header={'backgroundColor': '#f8f9fa', 'fontWeight': 'bold'},
        style_cell={'textAlign': 'center', 'padding': '10px'},
        style_as_list_view=True,
        page_size=20  # Dodano paginację
    ),

    dcc.Interval(
        id='interval-component',
        interval=2000 * 1000,  # Refresh every 2000 seconds
        n_intervals=0
    )
])



# User management layout
user_management_layout = html.Div(
    [
        html.H1("User Management"),
        dash_table.DataTable(
            id="user-table-management",
            columns=[
                {"name": "Nazwa", "id": "username"},
                {"name": "Email", "id": "email"},
                {"name": "Rola", "id": "role"},
                {"name": "Potwierdzony", "id": "verified"},
            ],
            style_table={"overflowX": "auto"},
            style_header={"backgroundColor": "lightgrey", "fontWeight": "bold"},
            style_cell={"textAlign": "center", "padding": "10px"},
            style_as_list_view=True,
        ),
        dcc.Interval(id="interval-user", interval=200 * 1000, n_intervals=0),
    ]
)



# Define the layout with the DataTable
user_role_management_layout = html.Div(
    [
        html.H1("User Role Management", className="text-center"),
        html.H3("GUEST Users with Verified Emails", className="text-center mt-4"),
        dash_table.DataTable(
            id="guest-user-table",
            data=[],
            columns=[
                {"name": "Username", "id": "username"},
                {"name": "Email", "id": "email"},
                {"name": "Role", "id": "role"},
                {
                    "name": "Change Role",
                    "id": "change_role",
                    "presentation": "dropdown",
                },  # Dropdown column
            ],
            editable=True,  # Allow edits in the table
            dropdown={  # Define the dropdown options
                "change_role": {
                    "options": [
                        {"label": "ADMIN", "value": "ADMIN"},
                        {"label": "EMPLOYEE", "value": "EMPLOYEE"},
                        {"label": "STUDENT", "value": "STUDENT"},
                        {"label": "GUEST", "value": "GUEST"},
                    ]
                }
            },
            cell_selectable=False,  # Disable row selection
            style_table={"overflowX": "visible", "overflowY": "visible"},
            style_header={"backgroundColor": "lightgrey", "fontWeight": "bold"},
            style_cell={"textAlign": "center", "padding": "10px"},
            css=[
                {
                    "selector": ".dash-table-container",
                    "rule": "height: auto !important;",
                },
                {
                    "selector": ".Select-menu-outer",
                    "rule": "display: block !important; z-index: 9999 !important;",
                },
                {
                    "selector": ".dash-cell",
                    "rule": "position: relative; z-index: 9999 !important;",
                },
                {
                    "selector": ".dropdown",
                    "rule": "position: static;",
                },
            ],
            page_size=10,
        ),
        html.Div(
            [
                html.Button(
                    "Save Changes",
                    id="save-roles-btn",
                    n_clicks=0,
                    className="btn btn-primary mt-3",
                ),
                html.Div(id="success-message", className="text-success mt-3"),
            ],
            style={"textAlign": "right"},
        ),
        # Success message
        dcc.Interval(id="interval-user-management", interval=200 * 1000, n_intervals=0),
    ]
)



# Reservation management layout
reservation_management_layout = html.Div(
    [
        html.H1("Zarządzanie Rezerwacjami", className="text-center mb-4"),
        # Reservation table
        dash_table.DataTable(
            id="reservation-table",
            columns=[
                {"name": "Nazwa Użytkownika", "id": "username"},
                {"name": "Rola", "id": "userRole"},
                {"name": "Utworzono", "id": "createdAt", "type": "datetime"},
                {"name": "Start", "id": "startTime", "type": "datetime"},
                {"name": "Koniec", "id": "endTime", "type": "datetime"},
                {"name": "Liczba Uczestników", "id": "participants", "type": "numeric"},
                {"name": "Pokój", "id": "roomName"},
                {"name": "Status", "id": "status"},
                {
                    "name": "change status",
                    "id": "change_status",
                    "presentation": "dropdown",
                },  # Dropdown column
            ],
            sort_action="native",  # Allows column sorting
            sort_by=[
                {"column_id": "createdAt", "direction": "desc"}
            ],  # Default sorting by createdAt
            editable=True,  # Allow edits in the table
            dropdown={  # Define the dropdown options
                "change_status": {
                    "options": [
                        {"label": "PENDING", "value": "PENDING"},
                        {"label": "CONFIRMED", "value": "CONFIRMED"},
                        {"label": "CANCELED", "value": "CANCELED"},
                    ],
                }
            },
            cell_selectable=False,  # Disable row selection
            style_table={"overflowX": "visible", "overflowY": "visible"},
            style_header={"backgroundColor": "lightgrey", "fontWeight": "bold"},
            style_cell={"textAlign": "center", "padding": "10px"},
            css=[
                {
                    "selector": ".dash-table-container",
                    "rule": "height: auto !important;",
                },
                {
                    "selector": ".Select-menu-outer",
                    "rule": "display: block !important; z-index: 10000 !important;",
                },
                {
                    "selector": ".dash-cell",
                    "rule": "position: relative; z-index: 99 !important;",
                },
                {
                    "selector": ".dropdown",
                    "rule": "position: static;",
                },
            ],
            page_size=10,
        ),
        html.Div(
            [
                html.Button(
                    "Save Changes",
                    id="save-status-btn",
                    n_clicks=0,
                    className="btn btn-primary mt-3",
                ),
                html.Div(id="success-message", className="text-success mt-3"),
            ],
            style={"textAlign": "right"},
        ),
        dcc.Interval(id="interval-reservation", interval=200 * 1000, n_intervals=0),
    ]
)
