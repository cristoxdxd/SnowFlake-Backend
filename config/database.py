from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))

db = client.booking_db

collection_name = db["bookings_collection"]
