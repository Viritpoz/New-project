from pymongo import MongoClient
from dotenv import load_dotenv, dotenv_values
from pathlib import Path
# Load environment variables from .env file
## /app/.env for deployment ##
## ../.env for development ##
pathenv = Path('../.env')
load_dotenv(dotenv_path=pathenv)
config = dotenv_values()  

# SNMP and MongoDB configuration
MONGO_URI = config.get('MONGO_URI') or 'mongodb://localhost:27017'
DB_NAME = config.get('DB_NAME') or 'snmp_db'

# Initialize MongoDB client
mongo_client = MongoClient(MONGO_URI)
db = mongo_client[DB_NAME]

# Export the MongoDB collection
def get_collection(collection_name):
    # print(MONGO_URI)
    return db[collection_name]
