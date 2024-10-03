import json
import logging
from config.db import get_collection
from models.snmp_model import Accespoint
import os
from puresnmp import Client, PyWrapper, V2C
from pathlib import Path
from dotenv import load_dotenv
import asyncio
from models.snmp_model import SNMPData
import codecs
from config.db import get_collection
from datetime import datetime, timedelta
import pytz
from bson import json_util
from datetime import datetime, time
from pymongo import DESCENDING

# Load environment variables from .env file
pathenv = Path('./.env')
load_dotenv(dotenv_path=pathenv)

# SNMP configuration ================================================
COMMUNITY = os.getenv('COMMUNITY') or 'public'
HOST = os.getenv('HOST') or 'http://localhost'
OIDS = {
    'student': '1.3.6.1.4.1.9.9.599.1.3.1.1.27',
    'type': '1.3.6.1.4.1.9.9.599.1.3.1.1.28',
    'macAccespoint': '1.3.6.1.4.1.9.9.599.1.3.1.1.8'
}

# adjust time to collect data from the device
time=10
# adjust the maximum data to be collected from the device per time
max_data = 1500
#=====================================================================



bangkok_tz = pytz.timezone('Asia/Bangkok')

# Initialize the collection
collection = get_collection('snmp_data')

def get_accesspoint(mac: str):
    collection = get_collection('accesspoint')
    # print(f"MAC: {mac}")
    document = collection.find_one({'Ethernet_MAC': mac})
    # print(document)
    if document:
        return Accespoint(AP_Name=document['AP_Name'], Ethernet_MAC=document['Ethernet_MAC'])
    else:
        return None

async def snmp_walk(host, community, oid):
    client = PyWrapper(Client(host, V2C(community)))
    results = {}
    async for oid, value in client.walk(oid):
        results[str(oid)] = str(value)
        if len(results) >= max_data:
            break
    return results

def format_mac_address(raw_mac):
    clean_mac = raw_mac.strip("b'")
    
    # Decode the ASCII representation of hex values
    decoded_mac = codecs.escape_decode(clean_mac)[0].hex()
    
    # Format the MAC address in the desired pattern
    return f"{decoded_mac[:4]}.{decoded_mac[4:8]}.{decoded_mac[8:12]}"

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
                        # print(f"MAC Address: {value}")
                        # Format MAC address
                        clean_value = format_mac_address(value)
                    else:
                        # Remove the 'b' prefix and quotes from the value
                        clean_value = value.strip("b'")
                    snmp_data_dict[category][key] = clean_value

            # Insert data into MongoDB ================================================
            all_keys = set(snmp_data_dict['student'].keys()) | set(snmp_data_dict['type'].keys()) | set(snmp_data_dict['macAccespoint'].keys())
            print(f"Number of unique keys processed: {len(all_keys)}")
            # Get the current time in Bangkok time zone
            bangkok_time = datetime.now(bangkok_tz).isoformat()
            for key in all_keys:
                student_id = snmp_data_dict['student'].get(key, "Unknown")
                # Skip this record if student_id is an empty string
                if student_id == "":
                    continue
                mac_address = snmp_data_dict['macAccespoint'].get(key, "Unknown")
                # print(f"MAC Address: {mac_address}")
                ap_name = get_accesspoint(mac_address)
                snmp_data_obj = SNMPData(
                    time=bangkok_time,
                    student=student_id,
                    type=snmp_data_dict['type'].get(key, "Unknown"),
                    macAccespoint=mac_address,
                    apName=ap_name.AP_Name if ap_name else "Unknown"
                )
                collection.insert_one(snmp_data_obj.dict())

            print(f"Inserted {len(all_keys)} records into MongoDB")
                                                                                                                                          
            print("Data inserted into MongoDB")

            # Wait for a short period before the next collection
            await asyncio.sleep(time)  
        except Exception as e:
            print(f"Error in SNMP collection: {e}")
            await asyncio.sleep(time)  # Wait before retrying

def getsnmpdataservice():
    cursor = collection.find()
    # Convert MongoDB cursor to a list of dictionaries
    data = [doc for doc in cursor]
    # Use json_util to handle MongoDB-specific types
    return json.loads(json_util.dumps(data))

def get_today_data():
    now = datetime.now(bangkok_tz)
    start_of_day = datetime(now.year, now.month, now.day, tzinfo=bangkok_tz)

    pipeline = [
        {"$match": {"time": {"$gte": start_of_day.isoformat()}}},
        {"$sort": {"time": DESCENDING}},
        {
            "$group": {
                "_id": "$student",
                "latest_entry": {"$first": "$$ROOT"}
            }
        },
        {"$replaceRoot": {"newRoot": "$latest_entry"}},
        {"$sort": {"time": DESCENDING}}
    ]

    today_data = list(collection.aggregate(pipeline))
    return today_data



def getDatafromBuilding(buildingname):
    now = datetime.now(bangkok_tz)
    start_of_day = datetime(now.year, now.month, now.day, tzinfo=bangkok_tz)

    pipeline = [
        {"$match": {"time": {"$gte": start_of_day.isoformat()}, "apName": {"$regex": f"^{buildingname}-"}}},
        {"$sort": {"time": DESCENDING}},
        {
            "$group": {
                "_id": "$student",
                "latest_entry": {"$first": "$$ROOT"}
            }
        },
        {"$replaceRoot": {"newRoot": "$latest_entry"}},
        {"$sort": {"time": DESCENDING}}
    ]
    building_data = list(collection.aggregate(pipeline))
    
    return building_data

def count_student_frombuilding(buildingname,timerange=10):
    now = datetime.now(bangkok_tz)
    time = now - timedelta(minutes=timerange)

    pipeline = [
        {"$match": {"time": {"$gte": time.isoformat()}, "apName": {"$regex": f"^{buildingname}-"}}},
        {"$group": {"_id": None, "unique_students": {"$addToSet": "$student"}}},
        {"$project": {"_id": 0, "total": {"$size": "$unique_students"}}}
    ]
    
    result = list(collection.aggregate(pipeline))
    total = result[0]["total"] if result else 0
    
    return total

def count_student_frombuilding_floor(buildingname, timerange=10):
    now = datetime.now(bangkok_tz)
    
    time = now - timedelta(minutes=timerange)

    # Step 1: Find all distinct floors for the building
    distinct_floors_pipeline = [
        {"$match": { "apName": {"$regex": f"^{buildingname}-"}}},
        {"$group": {"_id": {"$substr": ["$apName", 0, {"$indexOfBytes": ["$apName", "-AP"]}]}}}
    ]
    distinct_floors_result = list(collection.aggregate(distinct_floors_pipeline))
    all_floors = [floor["_id"] for floor in distinct_floors_result]

    # Debugging: Print the distinct floors result
    # print("Distinct floors result:", distinct_floors_result)
    # print("All floors:", all_floors)

    # Step 2: Count unique students for each floor
    pipeline_each_floor = [
        {"$match": {"time": {"$gte": time.isoformat()}, "apName": {"$regex": f"^{buildingname}-"}}},
        {"$group": {"_id": {"$substr": ["$apName", 0, {"$indexOfBytes": ["$apName", "-AP"]}]}, "unique_students": {"$addToSet": "$student"}}},
        {"$project": {"_id": 1, "total": {"$size": "$unique_students"}}}
    ]
    
    total_each_floor = list(collection.aggregate(pipeline_each_floor))
    
    # Debugging: Print the total each floor result
    # print("Total each floor result:", total_each_floor)

    # Step 3: Create a dictionary to store the results with default count 0
    floor_counts = {floor: 0 for floor in all_floors}
    
    # Step 4: Update the dictionary with actual counts from the query
    for floor_data in total_each_floor:
        floor_counts[floor_data["_id"]] = floor_data["total"]
    
    # Step 5: Convert the dictionary to the desired list format
    result = [{"_id": floor, "total": count} for floor, count in floor_counts.items()]
    
    return result