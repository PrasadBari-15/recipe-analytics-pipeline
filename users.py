
import os, sys, datetime
import firebase_admin
from firebase_admin import credentials, firestore

KEY_FILE = r"D:\programs\firebase\Task 2\RecipeAccountKey.json" 
if not os.path.exists(KEY_FILE):
    print("Service account key not found:", KEY_FILE); sys.exit(1)

cred = credentials.Certificate(KEY_FILE)
firebase_admin.initialize_app(cred)
db = firestore.client()

now = datetime.datetime.utcnow()

users = [
    {"user_id":"user_001","name":"Rohan Patil","email":"rohan01@example.com","location":"Pune","preferences":["vegetarian","quick"],"signup_date":now},
    {"user_id":"user_002","name":"Sneha Deshmukh","email":"sneha02@example.com","location":"Mumbai","preferences":["spicy","one-pot"],"signup_date":now},
    {"user_id":"user_003","name":"Ajay Kulkarni","email":"ajay03@example.com","location":"Pune","preferences":["breakfast","quick"],"signup_date":now},
    {"user_id":"user_004","name":"Priya More","email":"priya04@example.com","location":"Nagpur","preferences":["dessert","vegetarian"],"signup_date":now},
    {"user_id":"user_005","name":"Sagar Jadhav","email":"sagar05@example.com","location":"Nashik","preferences":["one-pot","comfort"],"signup_date":now},
    {"user_id":"user_006","name":"Neha Pisal","email":"neha06@example.com","location":"Kolhapur","preferences":["vegetarian","breakfast"],"signup_date":now},
    {"user_id":"user_007","name":"Amit Shinde","email":"amit07@example.com","location":"Mumbai","preferences":["protein","spicy"],"signup_date":now},
    {"user_id":"user_008","name":"Kavya Bhosale","email":"kavya08@example.com","location":"Satara","preferences":["quick","snack"],"signup_date":now},
    {"user_id":"user_009","name":"Suraj Pawar","email":"suraj09@example.com","location":"Solapur","preferences":["comfort","dal"],"signup_date":now},
    {"user_id":"user_010","name":"Maya Ingle","email":"maya10@example.com","location":"Sambhaji Nagar","preferences":["sweet","dessert"],"signup_date":now},
]

for u in users:
    doc_ref = db.collection("users").document(u["user_id"])
    doc_ref.set(u)   # set() overwrites existing doc with same id
    print(f"Uploaded: {u['user_id']} - {u['name']}")

print("Upload complete.")
