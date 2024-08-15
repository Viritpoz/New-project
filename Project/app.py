#!/usr/bin/env python3

from datetime import datetime, timedelta
from pymongo import MongoClient
from fastapi import FastAPI, BackgroundTasks
from dotenv import load_dotenv
from pymongo.errors import ConnectionFailure
from models.snmp_model import SNMPData
import asyncio
from puresnmp import Client, PyWrapper, V2C

# Load environment variables from .env file
load_dotenv()

# SNMP and MongoDB configuration ================================================
COMMUNITY = 'mfunet'
HOST = '172.30.99.11'
OIDS = {
    'student': '1.3.6.1.4.1.9.9.599.1.3.1.1.27',
    'type': '1.3.6.1.4.1.9.9.599.1.3.1.1.28',
    'macAccespoint': '1.3.6.1.4.1.9.9.599.1.3.1.1.8'
}
MONGO_URI = 'mongodb://root:1234@localhost:27018'
DB_NAME = 'snmp_data'
COLLECTION_NAME = 'snmp_results'
#===============================================================================

#================================================================================================
# adjust time to collect data from the device
time=10
# adjust the maximum data to be collected from the device per time
max_data = 100
#================================================================================================

# Initialize FastAPI app
app = FastAPI()

# Initialize MongoDB client
mongo_client = MongoClient(MONGO_URI)
db = mongo_client[DB_NAME]
collection = db[COLLECTION_NAME]

async def snmp_walk(host, community, oid):
    client = PyWrapper(Client(host, V2C(community)))
    results = {}
    async for oid, value in client.walk(oid):
        results[str(oid)] = str(value)
        if len(results) >= max_data:
            break
    return results

def format_mac_address(raw_mac):
    # Remove 'b' prefix and quotes, and split into bytes
    mac_bytes = raw_mac.strip("b'").replace('-', '').encode('ascii').decode('unicode_escape').encode('latin1')
    
    # Convert bytes to hexadecimal and join with colons
    return ':'.join(['{:02X}'.format(b) for b in mac_bytes])

async def continuous_snmp_collection():
    while True:
        try:
            print("Collecting SNMP data...")
            snmp_data = await asyncio.gather(
                snmp_walk(HOST, COMMUNITY, OIDS['student']),
                snmp_walk(HOST, COMMUNITY, OIDS['type']),
                snmp_walk(HOST, COMMUNITY, OIDS['macAccespoint'])
            )
            print("SNMP data collected successfully!")

            snmp_data_dict = {
                'student': {},
                'type': {},
                'macAccespoint': {}
            }

            # Process the data
            for i, category in enumerate(['student', 'type', 'macAccespoint']):
                for oid, value in snmp_data[i].items():
                    # Split the OID and use the last part as the key
                    key = oid.split('.')[-1]
                    if category == 'macAccespoint':
                        # Format MAC address
                        clean_value = format_mac_address(value)
                    else:
                        # Remove the 'b' prefix and quotes from the value
                        clean_value = value.strip("b'")
                    snmp_data_dict[category][key] = clean_value

            # Insert data into MongoDB
            for key in snmp_data_dict['student']:
                snmp_data_obj = SNMPData(
                    time=datetime.now().isoformat(),
                    student=snmp_data_dict['student'].get(key, "Unknown"),
                    type=snmp_data_dict['type'].get(key, "Unknown"),
                    macAccespoint=snmp_data_dict['macAccespoint'].get(key, "Unknown")
                )
                collection.insert_one(snmp_data_obj.dict())

            print("Data inserted into MongoDB")

            # Wait for a short period before the next collection
            await asyncio.sleep(time)  
        except Exception as e:
            print(f"Error in SNMP collection: {e}")
            await asyncio.sleep(time)  # Wait before retrying
            
@app.on_event("startup")
async def startup_event():
    print("Starting SNMP collection...")
    asyncio.create_task(continuous_snmp_collection())

@app.get('/latest_snmp_data')
async def get_latest_snmp_data():
    latest_data = list(collection.find().sort([('time', -1)]).limit(100))
    return {"status": "success", "data": latest_data}

@app.get('/snmp_data_range')
async def get_snmp_data_range(start_time: str, end_time: str):
    start = datetime.fromisoformat(start_time)
    end = datetime.fromisoformat(end_time)
    data = list(collection.find({
        'time': {'$gte': start.isoformat(), '$lte': end.isoformat()}
    }).sort([('time', -1)]))
    return {"status": "success", "data": data}

@app.get('/')
def api_home():
    return {"status": "success", "message": "Hello, World!"}