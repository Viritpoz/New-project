import asyncio
from service.snmpservie import continuous_snmp_collection, getsnmpdataservice


async def startup_event():
    print("Starting SNMP collection...")
    asyncio.create_task(continuous_snmp_collection())

def getsnmpdatacontroller():
    allData = getsnmpdataservice()
    # print(allData)
    return {"status": "success", "data": allData}