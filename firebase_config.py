import firebase_admin
from firebase_admin import credentials, firestore
import os

FIREBASE_CREDS_PATH = os.path.join(os.getcwd(), "firebase-adminsdk.json")

cred = credentials.Certificate(FIREBASE_CREDS_PATH)
firebase_admin.initialize_app(cred)

db = firestore.client()
