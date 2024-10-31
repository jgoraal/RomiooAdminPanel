# layouts.py


import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table

# Dashboard layout
dashboard_layout = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Liczba Zarejstrowanych Użytkowników"),
                dbc.CardBody(html.H4(id="total-users", className="card-title text-center"))
            ], className="shadow-sm mb-4", style={"border": "1px solid #ccc"}),
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Liczba Potwierdzonych emaili"),
                dbc.CardBody(html.H4(id="verified-emails", className="card-title text-center"))
            ], className="shadow-sm mb-4", style={"border": "1px solid #ccc"}),
        ], width=6)
    ]),

    # Add the combined subplot graph
    html.H2("Podsumowanie Statystyk", className="mt-4 text-center"),
    dcc.Graph(id='reservation-graph', config={'displayModeBar': False}),
    dcc.Graph(id='reservation-per-day-graph', config={'displayModeBar': False}),
    dcc.Graph(id='users-vs-reservations-graph', config={'displayModeBar': False}),

    # Users Table
    html.H2("Lista Użytkowników", className="mt-4 text-center"),
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
        style_table={'overflowX': 'auto'},
        style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'},
        style_cell={'textAlign': 'center', 'padding': '10px'},
        style_as_list_view=True
    ),
    dcc.Interval(
        id='interval-component',
        interval=50 * 1000,  # Refresh every 5 seconds
        n_intervals=0
    )
])


# User management layout
user_management_layout = html.Div([
    html.H1("User Management"),
    dash_table.DataTable(
        id='user-table-management',
        columns=[
            {'name': 'Nazwa', 'id': 'username'},
            {'name': 'Email', 'id': 'email'},
            {'name': 'Rola', 'id': 'role'},
            {'name': 'Potwierdzony', 'id': 'verified'}
        ],
        style_table={'overflowX': 'auto'},
        style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'},
        style_cell={'textAlign': 'center', 'padding': '10px'},
        style_as_list_view=True
    ),
    dcc.Interval(
        id='interval-user',
        interval=5 * 1000,
        n_intervals=0
    )
])


# Define the layout with the DataTable
user_role_management_layout = html.Div([

    html.H1("User Role Management", className="text-center"),
    html.H3("GUEST Users with Verified Emails", className="text-center mt-4"),

    dash_table.DataTable(
        id='guest-user-table',
        data=[],
        columns=[
            {'name': 'Username', 'id': 'username'},
            {'name': 'Email', 'id': 'email'},
            {'name': 'Role', 'id': 'role'},
            {'name': 'Change Role', 'id': 'change_role', 'presentation': 'dropdown'},  # Dropdown column
        ],
        editable=True,  # Allow edits in the table
        dropdown={  # Define the dropdown options
            'change_role': {
                'options': [
                    {'label': 'ADMIN', 'value': 'ADMIN'},
                    {'label': 'EMPLOYEE', 'value': 'EMPLOYEE'},
                    {'label': 'STUDENT', 'value': 'STUDENT'},
                    {'label': 'GUEST', 'value': 'GUEST'}
                ]
            }
        },
        style_table={'overflowX': 'visible', 'overflowY': 'visible'},
        style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'},
        style_cell={'textAlign': 'center', 'padding': '10px'},
        css=[{'selector': '.dash-table-container', 'rule': 'height: auto !important;'},
             {'selector': '.Select-menu-outer', 'rule': 'display: block !important; z-index: 9999 !important;'},
             {'selector': '.dash-cell', 'rule': 'position: relative; z-index: 9999 !important;'}
             ],
        page_size=10
    ),
    html.Button("Save Changes", id="save-roles-btn", n_clicks=0, className="btn btn-primary mt-3"),

    # Success message
    html.Div(id="success-message", className="text-success mt-3"),

    dcc.Interval(id='interval-user-management', interval=5 * 1000, n_intervals=0)
])

# Reservation management layout
reservation_management_layout = html.Div([
    html.H1("Zarządzanie Rezerwacjami", className="text-center mb-4"),

    # Reservation table
    dash_table.DataTable(
        id='reservation-table',
        columns=[
            {'name': 'Nazwa Użytkownika', 'id': 'username'},
            {'name': 'Rola', 'id': 'userRole'},
            {'name': 'Utworzono', 'id': 'createdAt', 'type': 'datetime'},
            {'name': 'Start', 'id': 'startTime', 'type': 'datetime'},
            {'name': 'Koniec', 'id': 'endTime', 'type': 'datetime'},
            {'name': 'Liczba Uczestników', 'id': 'participants', 'type': 'numeric'},
            {'name': 'Pokój', 'id': 'roomId'},
            {'name': 'Status', 'id': 'status'},
        ],
        sort_action='native',  # Allows column sorting
        sort_by=[{'column_id': 'createdAt', 'direction': 'desc'}],  # Default sorting by createdAt
        page_size=10,  # Pagination
        style_table={'overflowX': 'auto'},
        style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'},
        style_cell={'textAlign': 'center', 'padding': '10px'},
        style_as_list_view=True
    ),
    dcc.Interval(
        id='interval-reservation',
        interval=5 * 1000,
        n_intervals=0
    )
])
