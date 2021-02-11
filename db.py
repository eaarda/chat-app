from pymongo import MongoClient
from werkzeug.security import generate_password_hash

client = MongoClient(
    "mongodb+srv://test:test@chatapp.vmnsy.mongodb.net/<dbname>?retryWrites=true&w=majority")


chat_db = client.get_database("ChatDB")
users_collection = chat_db.get_collection("users")


def save_user(username, email, password):
    password_hash = generate_password_hash(password)
    users_collection.insert_one(
        {'_id': username, 'email': email, 'password': password_hash})


save_user("elif", "ea@ea", "ea123")
