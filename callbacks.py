# callbacks.py

from dash.dependencies import Input, Output, State
#from firebase_service import get_guest_users, update_user_role, get_pending_reservations
from layouts import dashboard_layout, user_management_layout, user_role_management_layout,reservation_management_layout
import plotly.express as px
from dash import callback_context
import pandas as pd
import dash
import plotly.express as px
import plotly.graph_objects as go


from test import get_pending_reservationss, get_guest_userss, update_user_rolee, update_reservationn


def register_callbacks(app,users,reservations,rooms):
    # Dashboard Callback
    @app.callback(
        [Output('user-growth-graph', 'figure'),
         Output('reservations-over-time-graph', 'figure'),
         Output('user-roles-graph', 'figure'),
         Output('reservation-statuses-graph', 'figure'),
         Output('top-users-table', 'data'),
         Output('user-table', 'data'),
         Output('total-users', 'children'),
         Output('verified-emails', 'children'),
         Output('total-reservations', 'children')],
        [Input('interval-component', 'n_intervals')]
    )
    def update_dashboard(n):

        # Convert data to DataFrame
        users_df = pd.DataFrame(users)
        reservations_df = pd.DataFrame(reservations)

        # Preprocessing users data
        users_df['created'] = pd.to_datetime(users_df['created'], errors='coerce', format="%d/%m/%Y %H:%M")
        users_df.dropna(subset=['created'], inplace=True)
        users_df['role'] = users_df['role'].fillna('Unknown')

        # Preprocessing reservations data
        reservations_df['createdAt'] = pd.to_datetime(reservations_df['createdAt'], unit='ms', errors='coerce')
        reservations_df.dropna(subset=['createdAt'], inplace=True)
        reservations_df['status'] = reservations_df['status'].fillna('Unknown')

        # User Growth Over Time - Wykres obszarowy (Area Chart)
        users_per_day = users_df.groupby(users_df['created'].dt.date).size().reset_index(name='user_count')
        users_per_day['cumulative_count'] = users_per_day['user_count'].cumsum()

        fig_user_growth = px.area(
            users_per_day, x='created', y='cumulative_count',
            labels={'created': 'Data', 'cumulative_count': 'Łączna liczba użytkowników'},
            title='Wzrost liczby użytkowników w czasie',
            template='plotly_white'
        )
        fig_user_growth.update_layout(
            height=500,
            xaxis_title='Data',
            yaxis_title='Łączna liczba użytkowników',
            xaxis=dict(
                tickformat='%d-%m-%Y',
                tickangle=45,
                nticks=20
            )
        )

        # Reservations Over Time - Ulepszony wykres
        reservations_df['date'] = reservations_df['createdAt'].dt.date

        # Agregacja danych według tygodnia lub miesiąca
        # Możesz wybrać jedną z poniższych opcji:

        # Opcja 1: Agregacja tygodniowa
        reservations_per_period = reservations_df.resample('W', on='createdAt').size().reset_index(
            name='reservation_count')

        # Opcja 2: Agregacja miesięczna
        # reservations_per_period = reservations_df.resample('M', on='createdAt').size().reset_index(name='reservation_count')

        # Użycie wykresu słupkowego z interaktywnym suwakiem zakresu dat
        fig_reservations_over_time = go.Figure()

        fig_reservations_over_time.add_trace(go.Bar(
            x=reservations_per_period['createdAt'],
            y=reservations_per_period['reservation_count'],
            marker_color='indianred'
        ))

        fig_reservations_over_time.update_layout(
            title='Liczba rezerwacji w czasie',
            xaxis_title='Data',
            yaxis_title='Liczba rezerwacji',
            template='plotly_white',
            height=500,
            xaxis=dict(
                tickformat='%d-%m-%Y',
                tickangle=45,
                rangeselector=dict(
                    buttons=list([
                        dict(count=1, label='1m', step='month', stepmode='backward'),
                        dict(count=6, label='6m', step='month', stepmode='backward'),
                        #dict(count=1, label='YTD', step='year', stepmode='todate'),
                        dict(count=1, label='1y', step='year', stepmode='backward'),
                        dict(step='all', label='Wszystko')
                    ])
                ),
                rangeslider=dict(visible=True),
                type='date'
            )
        )

        # User Roles Distribution - Wykres kołowy (Pie Chart)
        roles_count = users_df['role'].value_counts().reset_index()
        roles_count.columns = ['Rola', 'Liczba użytkowników']

        # Definicja mapy kolorów dla ról
        role_color_map = {
            'ADMIN': '#D32F2F',  # Crimson Red
            'STUDENT': '#0288D1',  # Bright Blue
            'EMPLOYEE': '#388E3C',  # Vivid Green
            'GUEST': '#757575'  # Neutral Grey
        }

        fig_user_roles = px.pie(
            roles_count,
            names='Rola',
            values='Liczba użytkowników',
            title='Podział użytkowników według ról',
            template='plotly_white',
            color='Rola',
            color_discrete_map=role_color_map
        )
        fig_user_roles.update_layout(height=500)

        # Reservation Statuses Distribution - Wykres słupkowy poziomy (Horizontal Bar Chart)
        status_count = reservations_df['status'].value_counts().reset_index()
        status_count.columns = ['Status', 'Liczba rezerwacji']

        # Definicja mapy kolorów dla statusów
        status_color_map = {
            'PENDING': '#FFB74D',  # Amber Orange
            'CONFIRMED': '#66BB6A',  # Fresh Green
            'CANCELED': '#E57373'  # Muted Red
        }

        fig_reservation_statuses = px.bar(
            status_count,
            x='Liczba rezerwacji',
            y='Status',
            orientation='h',
            title='Podział rezerwacji według statusu',
            template='plotly_white',
            color='Status',
            color_discrete_map=status_color_map
        )
        fig_reservation_statuses.update_layout(
            height=500,
            xaxis_title='Liczba rezerwacji',
            yaxis_title='Status',
        )

        # Top Active Users Table
        top_users = reservations_df['userId'].value_counts().reset_index()
        top_users.columns = ['userId', 'Liczba rezerwacji']
        top_users = top_users.merge(users_df[['uid', 'username', 'email']], left_on='userId', right_on='uid',
                                    how='left')
        top_users = top_users[['username', 'email', 'Liczba rezerwacji']].head(10).to_dict('records')

        # User Table Data
        user_table_data = users_df.to_dict('records')

        # User stats
        total_users = len(users_df)
        verified_emails = users_df['verified'].sum()
        total_reservations = f"{len(reservations_df)} rezerwacji"

        return (fig_user_growth, fig_reservations_over_time, fig_user_roles,
                fig_reservation_statuses, top_users, user_table_data,
                f"{total_users} użytkowników", f"{verified_emails} potwierdzonych emaili",
                total_reservations)

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

        guest = get_guest_userss() #get_guest_users()

        #print(guest)

        # Check which input triggered the callback
        if not ctx.triggered:
            return guest, dash.no_update, dash.no_update

        trigger = ctx.triggered[0]['prop_id'].split('.')[0]

        # Load data immediately when the page is first visited
        if trigger == 'url' and pathname == '/roles':  # Initial page load for '/roles' path
            guest = get_guest_userss()#get_guest_users()
            return guest, dash.no_update, dash.no_update

        # If the interval is triggered, refresh the table with fresh user data
        if trigger == 'interval-user-management':
            guest = get_guest_userss()#get_guest_users()
            return guest, dash.no_update, dash.no_update

        # If the save button is clicked, save the changes to Firestore
        if trigger == 'save-roles-btn' and n_clicks > 0:
            success = True
            for user in data:
                try:
                    # Update role in Firestore for each user
                    update_user_rolee(user['id'], user['change_role'])#update_user_role(user['id'], user['change_role'])
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
        Output("reservation-success-message", "children"),
        Output("reservation-table", "data"),
        Input("reservation-save-status-btn", "n_clicks"),
        Input('interval-reservation', 'n_intervals'),
        State("reservation-table", "data"),
        #prevent_initial_call=True,
    )
    def update_reservation_table(n_clicks, n_intervals, rows):
        ctx = dash.callback_context

        if not ctx.triggered:
            return dash.no_update, get_pending_reservationss()

        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if triggered_id == 'reservation-save-status-btn' and n_clicks > 0:
            # Kliknięto przycisk "Zapisz zmiany"
            if rows is None:
                raise dash.exceptions.PreventUpdate

            # Przejdź przez wszystkie wiersze tabeli i zaktualizuj status rezerwacji
            for row in rows:
                reservation_id = row.get('id')
                changed_status = row.get('status')
                # Zaktualizuj status rezerwacji w źródle danych
                update_reservationn(reservation_id, changed_status)
            # Po aktualizacji danych, pobierz zaktualizowane rezerwacje
            updated_data = get_pending_reservationss()
            return "Zapisano zmiany.", updated_data
        else:
            # Odświeżanie tabeli co interwał
            pending = get_pending_reservationss()
            # Convert the list of reservations to a DataFrame for easier handling
            df = pd.DataFrame(pending)
            # Sort by 'createdAt' if it exists
            if 'createdAt-long' in df.columns:
                df.sort_values(by='createdAt-long', ascending=False, inplace=True)
            else:
                print("Kolumna 'createdAt' nie istnieje w danych rezerwacji.")
            # Return the DataFrame as a list of dictionaries (for the DataTable)
            return dash.no_update, df.to_dict('records')




