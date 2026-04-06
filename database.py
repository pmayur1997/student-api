from pymongo import MongoClient, ASCENDING
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]

student_collection = db["students"]
user_collection = db["users"]  
email_tokens_collection = db["email_verification_tokens"]

# TTL index: MongoDB auto-deletes expired token documents after 24h
# (runs as a background job every ~60 seconds)
email_tokens_collection.create_index(
    [("expires_at", ASCENDING)],
    expireAfterSeconds=0
)
 