# callbacks.py

from dash.dependencies import Input, Output, State
from firebase_service import fetch_user_data, fetch_reservation_data, fetch_guest_users, update_user_role
from layouts import dashboard_layout, user_management_layout, user_role_management_layout
import plotly.express as px
from dash import dcc, html


def register_callbacks(app):
    @app.callback(
        [Output('reservation-graph', 'figure'),
         Output('user-table', 'data'),
         Output('total-users', 'children'),
         Output('verified-emails', 'children')],
        [Input('interval-component', 'n_intervals')]
    )
    def update_dashboard(n):
        reservation_data = fetch_reservation_data()
        fig = px.bar(reservation_data, x='room', y='reservations',
                     labels={'reservations': 'Reservations', 'room': 'Room'},
                     title="Reservations Per Room",
                     color_discrete_sequence=["#007bff"])
        fig.update_layout(paper_bgcolor='rgba(255,255,255,100)', plot_bgcolor='rgba(255,255,255,0)')

        users = fetch_user_data()
        total_users = len(users)
        verified_emails = sum(1 for user in users if user.get('verified', False))

        return fig, users, f"{total_users} users", f"{verified_emails} verified emails"




    @app.callback(Output('user-table-management', 'data'), [Input('interval-user', 'n_intervals')])
    def update_user_management(n):
        users = fetch_user_data()
        return users




    @app.callback(
        Output('guest-user-table', 'data'),
        Input('interval-user-management', 'n_intervals'))
    def update_user_role_management(n):
        users = fetch_guest_users()
        print(users)
        return users




    @app.callback(Output('page-content', 'children'),
                  [Input('url', 'pathname')])
    def display_page(pathname):
        if pathname == '/users':
            return user_management_layout
        if pathname == '/roles':
            return user_role_management_layout
        else:
            return dashboard_layout
