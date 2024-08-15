from config.db import get_collection
from models.snmp_model import Accespoint

def get_accesspoint(mac: str):
    collection = get_collection('accesspoint')
    document = collection.find_one({'Ethernet_MAC': mac})

    if document:
        return Accespoint(AP_Name=document['AP_Name'], Ethernet_MAC=document['Ethernet_MAC'])
    else:
        return None