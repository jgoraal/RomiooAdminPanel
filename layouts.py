# layouts.py
from typing import OrderedDict

from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc

# Dashboard layout
dashboard_layout = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Total Users"),
                dbc.CardBody(html.H4(id="total-users", className="card-title text-center"))
            ], className="shadow-sm mb-4", style={"border": "1px solid #ccc"}),
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Verified Emails"),
                dbc.CardBody(html.H4(id="verified-emails", className="card-title text-center"))
            ], className="shadow-sm mb-4", style={"border": "1px solid #ccc"}),
        ], width=6)
    ]),
    html.H2("Reservations Per Room", className="mt-4 text-center"),
    dcc.Graph(id='reservation-graph', config={'displayModeBar': False}),

    html.H2("User List", className="mt-4 text-center"),
    dash_table.DataTable(
        id='user-table',
        columns=[
            {'name': 'Username', 'id': 'username'},
            {'name': 'Email', 'id': 'email'},
            {'name': 'Verified', 'id': 'verified'},
            {'name': 'Role', 'id': 'role'},
            {'name': 'Last Seen', 'id': 'lastSeen'},
            {'name': 'Created', 'id': 'created'}
        ],
        style_table={'overflowX': 'auto'},
        style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'},
        style_cell={'textAlign': 'center', 'padding': '10px'},
        style_as_list_view=True
    ),
    dcc.Interval(
        id='interval-component',
        interval=5 * 1000,  # Refresh every 5 seconds
        n_intervals=0
    )
])

# User management layout
user_management_layout = html.Div([
    html.H1("User Management"),
    dash_table.DataTable(
        id='user-table-management',
        columns=[
            {'name': 'Username', 'id': 'username'},
            {'name': 'Email', 'id': 'email'},
            {'name': 'Role', 'id': 'role'},
            {'name': 'Verified', 'id': 'verified'}
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

from dash import dcc, html, dash_table
import pandas as pd
from collections import OrderedDict
import dash_bootstrap_components as dbc

# Define the data as a list of dictionaries (JSON serializable)
data = [
    {'username': 'User1', 'email': 'user1@example.com', 'role': 'GUEST', 'change_role': 'GUEST'},
    {'username': 'User2', 'email': 'user2@example.com', 'role': 'ADMIN', 'change_role': 'ADMIN'},
    {'username': 'User3', 'email': 'user3@example.com', 'role': 'EMPLOYEE', 'change_role': 'EMPLOYEE'}
]

# Define the layout with the DataTable
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc

user_role_management_layout = html.Div([

    html.H1("User Role Management", className="text-center"),
    html.H3("GUEST Users with Verified Emails", className="text-center mt-4"),

    dash_table.DataTable(
        id='guest-user-table',
        data=data,  # Will be populated dynamically via callback
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
        css=[    {'selector': '.dash-table-container', 'rule': 'height: auto !important;'},
                 {'selector': '.Select-menu-outer', 'rule': 'display: block !important; z-index: 9999 !important;'},
                 {'selector': '.dash-cell', 'rule': 'position: relative; z-index: 9999 !important;'}]
,  # Ensure dropdown visibility and table stays on top
    ),
    html.Button("Save Changes", id="save-roles-btn", n_clicks=0, className="btn btn-primary mt-3"),
    dcc.Interval(id='interval-user-management', interval=500 * 1000, n_intervals=0)
])




