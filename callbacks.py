# callbacks.py

from dash.dependencies import Input, Output, State
from firebase_service import get_guest_users, update_user_role, get_pending_reservations
from layouts import dashboard_layout, user_management_layout, user_role_management_layout,reservation_management_layout
import plotly.express as px
from dash import callback_context
import pandas as pd
import dash


def register_callbacks(app,users,reservations,rooms):
    # Dashboard Callback
    @app.callback(
        [Output('reservation-graph', 'figure'),
         Output('reservation-per-day-graph', 'figure'),
         Output('users-vs-reservations-graph', 'figure'),
         Output('user-table', 'data'),
         Output('total-users', 'children'),
         Output('verified-emails', 'children')],
        [Input('interval-component', 'n_intervals')]
    )
    def update_dashboard(n):

        # Convert data to DataFrame
        reservation_data = pd.DataFrame(reservations)  # Convert reservation_data to DataFrame
        users_df = pd.DataFrame(users)  # Convert users to DataFrame

        # Convert 'created' column to datetime in users_df
        users_df['created'] = pd.to_datetime(users_df['created'], errors='coerce', format="%d/%m/%Y %H:%M")
        users_df.dropna(subset=['created'], inplace=True)

        # Users per day and cumulative count
        users_per_day = users_df.groupby(users_df['created'].dt.date).size().reset_index(name='user_count')
        users_per_day['cumulative_count'] = users_per_day['user_count'].cumsum()

        # User Growth Over Time Chart
        fig_user_growth = px.line(
            users_per_day, x='created', y='cumulative_count',
            labels={'created': 'Date', 'cumulative_count': 'Total Users'},
            title='User Growth Over Time'
        )
        fig_user_growth.update_xaxes(tickformat="%d-%m-%Y", title_text="Date")
        fig_user_growth.update_yaxes(title_text="Total Users")

        # Convert 'createdAt' column to datetime in reservation_data
        reservation_data['createdAt'] = pd.to_datetime(reservation_data['createdAt'], errors='coerce')
        reservation_data.dropna(subset=['createdAt'], inplace=True)

        # Reservations per Day
        reservations_per_day = reservation_data.groupby(reservation_data['createdAt'].dt.date).size().reset_index(
            name='reservation_count')

        fig_reservations = px.bar(
            reservations_per_day, x='createdAt', y='reservation_count',
            title='Reservations Over Time',
            labels={'createdAt': 'Date', 'reservation_count': 'Reservations'}
        )

        # Daily Users vs. Reservations
        users_daily = users_df.groupby(users_df['created'].dt.date).size().reset_index(name='daily_new_users')
        reservations_daily = reservation_data.groupby(reservation_data['createdAt'].dt.date).size().reset_index(
            name='daily_reservations')
        daily_combined = pd.merge(users_daily, reservations_daily, how='outer', left_on='created',
                                  right_on='createdAt').fillna(0)

        fig_user_vs_reservations = px.line(
            daily_combined, x='created', y=['daily_new_users', 'daily_reservations'],
            title='Daily New Users vs. Daily Reservations'
        )

        # User stats
        total_users = len(users)
        verified_emails = sum(user.get('verified', False) for user in users)

        return fig_user_growth, fig_reservations, fig_user_vs_reservations, users, f"{total_users} users", f"{verified_emails} verified emails"

    # User table
    @app.callback(
        Output('user-table-management', 'data'),
        [Input('interval-user', 'n_intervals')]
    )
    def update_user_management(n):
        #users = fetch_users_data()
        return users

    # User role
    @app.callback(
        [Output('guest-user-table', 'data'),
         Output('success-message', 'children'),
         Output('save-roles-btn', 'n_clicks')],
        [Input('save-roles-btn', 'n_clicks'),
         Input('url', 'pathname'),  # Add this to load data on initial page load
         Input('interval-user-management', 'n_intervals')],
        [State('guest-user-table', 'data')]
    )
    def handle_user_roles(n_clicks, pathname, n_intervals, data):
        ctx = callback_context

        guest = get_guest_users()

        # Check which input triggered the callback
        if not ctx.triggered:
            return guest, dash.no_update, dash.no_update

        trigger = ctx.triggered[0]['prop_id'].split('.')[0]

        # Load data immediately when the page is first visited
        if trigger == 'url' and pathname == '/roles':  # Initial page load for '/roles' path
            guest = get_guest_users()
            return guest, dash.no_update, dash.no_update

        # If the interval is triggered, refresh the table with fresh user data
        if trigger == 'interval-user-management':
            guest = get_guest_users()
            return guest, dash.no_update, dash.no_update

        # If the save button is clicked, save the changes to Firestore
        if trigger == 'save-roles-btn' and n_clicks > 0:
            success = True
            for user in data:
                try:
                    # Update role in Firestore for each user
                    update_user_role(user['id'], user['change_role'])
                except Exception as e:
                    success = False
                    print(f"Error updating user {user['id']}: {e}")

            if success:
                return data, "Roles updated successfully!", 0  # Reset button click count after success
            else:
                return data, "Failed to update roles.", 0  # Reset button click count after failure

        return dash.no_update, "", dash.no_update

    # Layout
    @app.callback(Output('page-content', 'children'),
                  [Input('url', 'pathname')])
    def display_page(pathname):
        if pathname == '/users':
            return user_management_layout
        if pathname == '/roles':
            return user_role_management_layout
        if pathname == '/reservations':
            return reservation_management_layout
        else:
            return dashboard_layout


    # Reservation
    @app.callback(
        Output('reservation-table', 'data'),
        [Input('interval-reservation', 'n_intervals')]  # Optional: auto-update at intervals
    )
    def update_reservation_table(n):
        # Fetch pending reservations
        pending = get_pending_reservations()

        print(pending)

        # Convert the list of reservations to a DataFrame for easier handling
        df = pd.DataFrame(pending)

        # Sort by 'createdAt' in descending order
        df.sort_values(by='createdAt', ascending=False, inplace=True)

        # Return the DataFrame as a list of dictionaries (for the DataTable)
        return df.to_dict('records')
