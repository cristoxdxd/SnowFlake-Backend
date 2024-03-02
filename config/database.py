from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))

db = client.booking_db

collection_name = db["booking_collection"]
availability_name = db["availability_collection"]
activities_name = db["activities_collection"]
codes_reservation = db["codes_reservation"]
