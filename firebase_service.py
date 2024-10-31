# firebase_service.py

import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from pandas.core.window import doc
import datetime
import pytz

# Initialize Firebase Admin SDK with credentials
cred = credentials.Certificate('C:/Users/yakoob/Downloads/firebase.json')
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()


def fetch_user_data():
    users_ref = db.collection('users')
    docs = users_ref.stream()
    users = [{**doc.to_dict()} for doc in docs]
    return users

def fetch_all_reservation():
    reservations_ref = db.collection('reservations')
    docs = reservations_ref.stream()
    reservations = [{**doc.to_dict()} for doc in docs]
    return reservations


def fetch_reservation_data():
    reservations_ref = db.collection('reservations')
    docs = reservations_ref.stream()

    reservations = []
    for doc in docs:
        reservation_data = doc.to_dict()

        # Convert long timestamps to formatted dates
        created_at_formatted = convert_long_to_datetime(reservation_data.get('createdAt'))
        start_time_formatted = convert_long_to_datetime(reservation_data.get('startTime'))
        end_time_formatted = convert_long_to_datetime(reservation_data.get('endTime'))

        # Append the formatted data
        reservations.append({
            'room': reservation_data.get('roomId', 'Unknown'),
            'status': reservation_data.get('status', 'Unknown'),
            'participants': reservation_data.get('participants', 'Unknown'),
            'createdAt': created_at_formatted,
            'startTime': start_time_formatted,
            'endTime': end_time_formatted
        })

    return reservations



def fetch_guest_users():
    users_ref = db.collection('users')

    # Create filters
    verified_filter = FieldFilter('verified', '==', True)
    role_filter = FieldFilter('role', '==', 'GUEST')

    # Apply the filters
    docs = users_ref.where(filter=verified_filter).where(filter=role_filter).stream()

    users = [{
        'username': doc.get('username'),
        'email': doc.get('email'),
        'role': doc.get('role'),
        'change_role': doc.get('role'),  # This sets the dropdown to the current role
        'id': doc.id
    } for doc in docs]

    return users


# Function to update the user's role in Firestore
def update_user_role(user_id, new_role):
    # Update the role field of the user in Firestore
    user_ref = db.collection('users').document(user_id)
    user_ref.update({'role': new_role})


def fetch_verified_users():
    users_ref = db.collection('users')

    verified_filter = FieldFilter('verified', '==', True)
    role_filter = FieldFilter('role', '!=', 'GUEST')

    docs = users_ref.where(filter=verified_filter).where(filter=role_filter).stream()

    users = [{
        'username': doc.get('username'),
        'email': doc.get('email'),
        'role': doc.get('role'),
        'id': doc.id
    } for doc in docs]

    return users


def convert_long_to_datetime(timestamp_long):
    # Convert long (milliseconds) to a UTC datetime object
    timestamp_utc = datetime.datetime.fromtimestamp(timestamp_long / 1000.0)

    # Split the formatted string to include only milliseconds, ensuring only 3 digits are shown for milliseconds
    formatted_time = timestamp_utc.strftime('%d.%m.%Y %Hh:%Mm:%Ss')

    # Extract milliseconds and add it to the string in the correct format
    milliseconds = int((timestamp_long % 1000))  # Get the remaining milliseconds part
    return f"{formatted_time}.{milliseconds:03d}ms"


def fetch_pending_reservations():
    # Fetch all verified users and map by userId
    users = fetch_verified_users()
    user_map = {user['id']: user for user in users}

    # Query reservations with pending status
    reservations_ref = db.collection('reservations')
    pending_filter = FieldFilter('status', '==', 'PENDING')
    docs = reservations_ref.where(filter=pending_filter).stream()

    reservations = []
    for doc in docs:
        reservation_data = doc.to_dict()
        user_id = reservation_data.get('userId')

        # Fetch user details from user_map
        user = user_map.get(user_id, {})
        username = user.get('username', 'Unknown')
        user_role = user.get('role', 'Unknown')

        # Convert timestamps to readable format
        created_at_long = reservation_data.get('createdAt')
        start_time_long = reservation_data.get('startTime')
        end_time_long = reservation_data.get('endTime')

        created_at_formatted = convert_long_to_datetime(created_at_long) if created_at_long else "Unknown"
        start_time_formatted = convert_long_to_datetime(start_time_long) if start_time_long else "Unknown"
        end_time_formatted = convert_long_to_datetime(end_time_long) if end_time_long else "Unknown"

        # Append the reservation with enriched user data
        reservations.append({
            'username': username,
            'userRole': user_role,
            'createdAt': created_at_formatted,
            'startTime': start_time_formatted,
            'endTime': end_time_formatted,
            'participants': reservation_data.get('participants', 'Unknown'),
            'roomId': reservation_data.get('roomId', 'Unknown'),
            'status': reservation_data.get('status', 'Unknown'),
            'id': doc.id
        })

    return reservations
