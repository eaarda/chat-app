from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://test:test@chatapp.vmnsy.mongodb.net/<dbname>?retryWrites=true&w=majority")

chat_db = client.get_database("ChatDB")
users_collection = chat_db.get_collection("users")
