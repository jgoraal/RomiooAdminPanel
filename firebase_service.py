# firebase_service.py

import firebase_admin
from firebase_admin import credentials, firestore
from utils import convert_long_to_datetime, convert_long_to_simple_date_format
import redis
import pickle

redis_client = redis.Redis(host='localhost', port=6379, db=0)

#/Users/jakubgorski/Desktop/firebase.json
#C:/Users/yakoob/Downloads/firebase.json
# Initialize Firebase Admin SDK with credentials
cred = credentials.Certificate('/Users/jakubgorski/Desktop/firebase.json')
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()


# Global variables to cache data
# cached_users = None
# cached_reservations = None
# cached_rooms = None

# Fetch reservations from Firestore, with caching
def fetch_reservations_cached():
    cache_key = 'cached_reservations'
    cached_data = redis_client.get(cache_key)
    if cached_data:
        # Data is in cache, deserialize it
        cached_reservations = pickle.loads(cached_data)
        return cached_reservations
    else:
        # Data not in cache, fetch from Firestore
        reservations_ref = db.collection('reservations')
        docs = reservations_ref.stream()
        cached_reservations = [{**doc.to_dict(), 'id': doc.id} for doc in docs]
        # Serialize and store in cache with expiration time (e.g., 1 hour)
        redis_client.setex(cache_key, 3600, pickle.dumps(cached_reservations))
        return cached_reservations
# def fetch_reservations_cached():
#     global cached_reservations
#     if cached_reservations is None:  # Check if data is cached
#         reservations_ref = db.collection('reservations')
#         docs = reservations_ref.stream()
#         cached_reservations = [{**reservation.to_dict()} for reservation in docs]
#     return cached_reservations

# Fetch users from Firestore, with caching
def fetch_users_cached():
    cache_key = 'cached_users'
    cached_data = redis_client.get(cache_key)
    if cached_data:
        # Data is in cache, deserialize it
        cached_users = pickle.loads(cached_data)
        return cached_users
    else:
        # Data not in cache, fetch from Firestore
        users_ref = db.collection('users')
        docs = users_ref.stream()
        cached_users = [{**doc.to_dict(), 'uid': doc.id} for doc in docs]
        # Serialize and store in cache with expiration time (e.g., 1 hour)
        redis_client.setex(cache_key, 3600, pickle.dumps(cached_users))
        return cached_users
# def fetch_users_cached():
#     global cached_users
#     if cached_users is None:  # Check if data is cached
#         users_ref = db.collection('users')
#         docs = users_ref.stream()
#         cached_users = [{**user.to_dict()} for user in docs]
#     return cached_users

# Fetch rooms from Firestore, with caching
def fetch_rooms_cached():
    cache_key = 'cached_rooms'
    cached_data = redis_client.get(cache_key)
    if cached_data:
        # Data is in cache, deserialize it
        cached_rooms = pickle.loads(cached_data)
        return cached_rooms
    else:
        # Data not in cache, fetch from Firestore
        rooms_ref = db.collection('rooms')
        docs = rooms_ref.stream()
        cached_rooms = [{**doc.to_dict(), 'id': doc.id} for doc in docs]
        # Serialize and store in cache with expiration time (e.g., 1 hour)
        redis_client.setex(cache_key, 3600, pickle.dumps(cached_rooms))
        return cached_rooms
    # global cached_rooms
    # if cached_rooms is None:  # Check if data is cached
    #     rooms_ref = db.collection('rooms')
    #     docs = rooms_ref.stream()
    #     cached_rooms = [{**room.to_dict()} for room in docs]
    # return cached_rooms

# Clear cache when necessary
def clear_cache():
    redis_client.delete('cached_users')
    redis_client.delete('cached_reservations')
    redis_client.delete('cached_rooms')
    # global cached_users, cached_reservations, cached_rooms
    # cached_users = None
    # cached_reservations = None
    # cached_rooms = None

# Function to filter guest users from cached data
def get_guest_users():
    cached_users = fetch_users_cached()
    if not cached_users:
        return None  # Return None if data isn't cached

    # Filter for verified guest users
    guest_users = [
        {
            'username': user.get('username'),
            'email': user.get('email'),
            'role': user.get('role'),
            'change_role': user.get('role'),  # Sets the dropdown to the current role
            'id': user.get('uid')
        }
        for user in cached_users
        if user.get('verified') == True and user.get('role') == 'GUEST'
    ]

    return guest_users
    # global cached_users
    # if cached_users is None:
    #     return None  # Return None if data isn't cached
    #
    # # Filter for verified guest users
    # guest_users = [
    #     {
    #         'username': user.get('username'),
    #         'email': user.get('email'),
    #         'role': user.get('role'),
    #         'change_role': user.get('role'),  # Sets the dropdown to the current role
    #         'id': user.get('uid')
    #     }
    #     for user in cached_users
    #     if user.get('verified') == True and user.get('role') == 'GUEST'
    # ]
    #
    # return guest_users

# Function to filter pending reservations from cached data
def get_pending_reservations():
    cached_reservations = fetch_reservations_cached()
    cached_users = fetch_users_cached()
    cached_rooms = fetch_rooms_cached()

    if not cached_reservations or not cached_users or not cached_rooms:
        return None  # Return None if data isn't cached

    # Fetch all verified users and map by userId (caching user data if needed)
    user_map = {user['uid']: user for user in cached_users}
    room_map = {room['id']: room for room in cached_rooms}

    # Filter and format PENDING reservations from cached data
    pending_reservations = [
        {
            'id': reservation.get('id'),
            'roomName': room_map.get(reservation.get('roomId'), {}).get('name', "?"),
            'username': user_map.get(reservation.get('userId'), {}).get('username', 'Unknown'),
            'userRole': user_map.get(reservation.get('userId'), {}).get('role', 'Unknown'),
            'createdAt': convert_long_to_datetime(reservation.get('createdAt')),
            'startTime': convert_long_to_simple_date_format(reservation.get('startTime')),
            'endTime': convert_long_to_simple_date_format(reservation.get('endTime')),
            'participants': reservation.get('participants', 'Unknown'),
            'status': reservation.get('status', 'Unknown')
        }
        for reservation in cached_reservations
        if reservation.get('status') == 'PENDING'
    ]


    return pending_reservations
    # global cached_reservations, cached_users, cached_rooms
    # if cached_reservations is None:
    #     return None  # Return None if data isn't cached
    #
    # print(cached_users)
    #
    # # Fetch all verified users and map by userId (caching user data if needed)
    # user_map = {user['uid']: user for user in cached_users}
    # room_map = {room['id']: room for room in cached_rooms}
    #
    # # Filter and format PENDING reservations from cached data
    # pending_reservations = [
    #     {
    #         'id': reservation.get('id'),
    #         'roomName': room_map.get(reservation.get('roomId'), {}).get('name',"?"),
    #         'username': user_map.get(reservation.get('userId'), {}).get('username', 'Unknown'),
    #         'userRole': user_map.get(reservation.get('userId'), {}).get('role', 'Unknown'),
    #         'createdAt': convert_long_to_datetime(reservation.get('createdAt')),
    #         'startTime': convert_long_to_simple_date_format(reservation.get('startTime')),
    #         'endTime': convert_long_to_simple_date_format(reservation.get('endTime')),
    #         'participants': reservation.get('participants', 'Unknown'),
    #         'status': reservation.get('status', 'Unknown')
    #     }
    #     for reservation in cached_reservations
    #     if reservation.get('status') == 'PENDING'
    # ]
    #
    # return pending_reservations

# Function to update the user's role in Firestore
def update_user_role(user_id, new_role):
    # Aktualizacja w Firestore
    user_ref = db.collection('users').document(user_id)
    user_ref.update({'role': new_role})

    # Aktualizacja w cache
    cache_key = 'cached_users'
    cached_data = redis_client.get(cache_key)
    if cached_data:
        # Deserializacja cache
        cached_users = pickle.loads(cached_data)

        # Znalezienie i aktualizacja użytkownika w cache
        for user in cached_users:
            if user.get('uid') == user_id:
                user['role'] = new_role
                break

        # Serializacja i zapis zaktualizowanego cache
        redis_client.setex(cache_key, 3600, pickle.dumps(cached_users))
    # # Update the role field of the user in Firestore
    # user_ref = db.collection('users').document(user_id)
    # user_ref.update({'role': new_role})

def update_reservation(reservation_id, changed_status):
    # Aktualizacja w Firestore
    reservation_ref = db.collection('reservations').document(reservation_id)
    reservation_ref.update({'status': changed_status})

    # Aktualizacja w cache
    cache_key = 'cached_reservations'
    cached_data = redis_client.get(cache_key)
    if cached_data:
        # Deserializacja cache
        cached_reservations = pickle.loads(cached_data)

        # Znalezienie i aktualizacja rezerwacji w cache
        for reservation in cached_reservations:
            if reservation.get('id') == reservation_id:
                reservation['status'] = changed_status
                break

        # Serializacja i zapis zaktualizowanego cache
        redis_client.setex(cache_key, 3600, pickle.dumps(cached_reservations))

    # reservation_ref = db.collection('reservations').document(reservation_id)
    # reservation_ref.update({'status': changed_status})

# def fetch_users_data():
#     users_ref = db.collection('users')
#     docs = users_ref.stream()
#     users = [{**doc.to_dict()} for doc in docs]
#     return users
#
#
# def fetch_all_reservation():
#     reservations_ref = db.collection('reservations')
#     docs = reservations_ref.stream()
#     reservations = [{**doc.to_dict()} for doc in docs]
#     return reservations
#
#
# def fetch_reservation_data():
#     reservations_ref = db.collection('reservations')
#     docs = reservations_ref.stream()
#
#     reservations = []
#     for doc in docs:
#         reservation_data = doc.to_dict()
#
#         # Convert long timestamps to formatted dates
#         created_at_formatted = convert_long_to_datetime(reservation_data.get('createdAt'))
#         start_time_formatted = convert_long_to_simple_date_format(reservation_data.get('startTime'))
#         end_time_formatted = convert_long_to_simple_date_format(reservation_data.get('endTime'))
#
#         # Append the formatted data
#         reservations.append({
#             'room': reservation_data.get('roomId', 'Unknown'),
#             'status': reservation_data.get('status', 'Unknown'),
#             'participants': reservation_data.get('participants', 'Unknown'),
#             'createdAt': created_at_formatted,
#             'startTime': start_time_formatted,
#             'endTime': end_time_formatted
#         })
#
#     return reservations
#
#
# def fetch_guest_users():
#     users_ref = db.collection('users')
#
#     # Create filters
#     verified_filter = FieldFilter('verified', '==', True)
#     role_filter = FieldFilter('role', '==', 'GUEST')
#
#     # Apply the filters
#     docs = users_ref.where(filter=verified_filter).where(filter=role_filter).stream()
#
#     users = [{
#         'username': doc.get('username'),
#         'email': doc.get('email'),
#         'role': doc.get('role'),
#         'change_role': doc.get('role'),  # This sets the dropdown to the current role
#         'id': doc.id
#     } for doc in docs]
#
#     return users
#
#
#
#
# def fetch_verified_users():
#     users_ref = db.collection('users')
#
#     verified_filter = FieldFilter('verified', '==', True)
#     role_filter = FieldFilter('role', '!=', 'GUEST')
#
#     docs = users_ref.where(filter=verified_filter).where(filter=role_filter).stream()
#
#     users = [{
#         'username': doc.get('username'),
#         'email': doc.get('email'),
#         'role': doc.get('role'),
#         'id': doc.id
#     } for doc in docs]
#
#     return users
#
#
# def fetch_pending_reservations():
#     # Fetch all verified users and map by userId
#     users = fetch_verified_users()
#     user_map = {user['id']: user for user in users}
#
#     # Query reservations with pending status
#     reservations_ref = db.collection('reservations')
#     pending_filter = FieldFilter('status', '==', 'PENDING')
#     docs = reservations_ref.where(filter=pending_filter).stream()
#
#     reservations = []
#     for doc in docs:
#         reservation_data = doc.to_dict()
#         user_id = reservation_data.get('userId')
#
#         # Fetch user details from user_map
#         user = user_map.get(user_id, {})
#         username = user.get('username', 'Unknown')
#         user_role = user.get('role', 'Unknown')
#
#         # Convert timestamps to readable format
#         created_at_long = reservation_data.get('createdAt')
#         start_time_long = reservation_data.get('startTime')
#         end_time_long = reservation_data.get('endTime')
#
#         created_at_formatted = convert_long_to_datetime(created_at_long) if created_at_long else "Unknown"
#         start_time_formatted = convert_long_to_datetime(start_time_long) if start_time_long else "Unknown"
#         end_time_formatted = convert_long_to_datetime(end_time_long) if end_time_long else "Unknown"
#
#         # Append the reservation with enriched user data
#         reservations.append({
#             'username': username,
#             'userRole': user_role,
#             'createdAt': created_at_formatted,
#             'startTime': start_time_formatted,
#             'endTime': end_time_formatted,
#             'participants': reservation_data.get('participants', 'Unknown'),
#             'roomId': reservation_data.get('roomId', 'Unknown'),
#             'status': reservation_data.get('status', 'Unknown'),
#             'id': doc.id
#         })
#
#     return reservations


