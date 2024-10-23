# firebase_service.py

import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_query import FieldFilter

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



def fetch_reservation_data():
    return {
        'room': ['Room A', 'Room B', 'Room C','Room D','Room G','Room H','Room J','Room N','Room M'],
        'reservations': [15, 25, 10,10,1,2,3,5,6]
    }

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

