from pymongo import MongoClient
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
pathenv = Path('../.env')
load_dotenv(dotenv_path=pathenv)

# SNMP and MongoDB configuration
MONGO_URI = os.getenv('MONGO_URI') or 'mongodb://localhost:27017'
DB_NAME = os.getenv('DB_NAME') or 'snmp_db'

# Initialize MongoDB client
mongo_client = MongoClient(MONGO_URI)
db = mongo_client[DB_NAME]

# Export the MongoDB collection
def get_collection(collection_name):
    print(MONGO_URI)
    return db[collection_name]
