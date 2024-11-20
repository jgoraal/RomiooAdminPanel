import random
import datetime
import uuid
from faker import Faker

from utils import convert_long_to_datetime, convert_long_to_simple_date_format

fake = Faker()

# Zmienne globalne
cached_users = None
cached_rooms = None
cached_reservations = None

def fetch_users():
    global cached_users
    if cached_users is None:
        cached_users = []
        roles = ['ADMIN', 'EMPLOYEE', 'STUDENT', 'GUEST']
        for _ in range(1000):  # Generuj 100 użytkowników
            uid = str(uuid.uuid4())
            user = {
                'uid': uid,
                'username': fake.user_name(),
                'email': fake.email(),
                'role': random.choice(roles),
                'verified': random.choice([True, False]),
                'created': fake.date_time_between(start_date='-2y', end_date='now').strftime('%d/%m/%Y %H:%M'),
                'lastSeen': fake.date_time_between(start_date='-1y', end_date='now').strftime('%d/%m/%Y %H:%M')
            }
            cached_users.append(user)
    return cached_users

def fetch_rooms():
    global cached_rooms
    if cached_rooms is None:
        cached_rooms = []
        for i in range(1, 41):  # Generuj 40 pokoi
            room = {
                'id': f'room_{i}',
                'name': f'Sala {i}',
                # Dodaj dodatkowe atrybuty pokoju, jeśli potrzebujesz
            }
            cached_rooms.append(room)
    return cached_rooms

def fetch_reservations():
    global cached_reservations
    if cached_reservations is None:
        cached_reservations = []
        statuses = ['PENDING', 'CONFIRMED', 'CANCELED']
        cached_users = fetch_users()
        cached_rooms = fetch_rooms()
        user_ids = [user['uid'] for user in cached_users]
        room_ids = [room['id'] for room in cached_rooms]
        for _ in range(2000):  # Generuj 2000 rezerwacji
            reservation_id = str(uuid.uuid4())
            user_id = random.choice(user_ids)
            room_id = random.choice(room_ids)
            created_at = fake.date_time_between(start_date='-2y', end_date='now')
            start_time = created_at + datetime.timedelta(days=random.randint(0, 30))
            end_time = start_time + datetime.timedelta(hours=random.randint(1, 8))
            reservation = {
                'id': reservation_id,
                'userId': user_id,
                'roomId': room_id,
                'status': random.choice(statuses),
                'createdAt': int(created_at.timestamp() * 1000),  # w milisekundach
                'startTime': int(start_time.timestamp() * 1000),
                'endTime': int(end_time.timestamp() * 1000),
                'participants': random.randint(1, 20),
            }
            cached_reservations.append(reservation)
    return cached_reservations

def get_guest_userss():
    cached_users = fetch_users()
    if not cached_users:
        return []  # Zwróć pustą listę, jeśli brak danych

    guest_users = [
        {
            'username': user.get('username'),
            'email': user.get('email'),
            'role': user.get('role'),
            'change_role': user.get('role'),
            'id': user.get('uid')
        }
        for user in cached_users
        if user.get('verified') == True and user.get('role') == 'GUEST'
    ]
    return guest_users

def get_pending_reservationss():
    cached_reservations = fetch_reservations()
    cached_users = fetch_users()
    cached_rooms = fetch_rooms()

    if not cached_reservations or not cached_users or not cached_rooms:
        return []  # Zwróć pustą listę, jeśli brak danych

    user_map = {user['uid']: user for user in cached_users}
    room_map = {room['id']: room for room in cached_rooms}

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


def update_user_rolee(user_id, new_role):
    global cached_users
    if cached_users is None:
        # Jeśli użytkownicy nie są jeszcze załadowani, ładujemy ich
        cached_users = fetch_users()
    # Znajdujemy użytkownika o podanym `user_id` i aktualizujemy jego rolę
    for user in cached_users:
        if user.get('uid') == user_id:
            user['role'] = new_role
            break


def update_reservationn(reservation_id, changed_status):
    global cached_reservations
    if cached_reservations is None:
        # Jeśli rezerwacje nie są jeszcze załadowane, ładujemy je
        cached_reservations = fetch_reservations()
    # Znajdujemy rezerwację o podanym `reservation_id` i aktualizujemy jej status
    for reservation in cached_reservations:
        if reservation.get('id') == reservation_id:
            reservation['status'] = changed_status
            break

