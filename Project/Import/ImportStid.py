import pandas as pd
import re
from pymongo import MongoClient

# อ่านไฟล์ CSV
file_path = 'Data/CSV/Cleaned.csv'
df = pd.read_csv(file_path)

# ดรอปแถวที่มีค่า null ในคอลัมน์ 'Student ID'
df_cleaned = df.dropna(subset=['Student ID'])

# เลือกเฉพาะคอลัมน์ 'Student ID' สำหรับนำไปใช้งาน
df_final = df_cleaned[['Student ID']]

# แปลง DataFrame เป็น dict เพื่อเตรียมสำหรับการอัพเดตใน MongoDB
data_dict = df_final.to_dict(orient='records')

# เชื่อมต่อกับ MongoDB
client = MongoClient('mongodb://10.1.55.232:27017/')
db = client['mydb']
collection = db['Stid']

# ลบข้อมูลเก่าทั้งหมดในคอลเล็กชัน
collection.delete_many({})

# แทรกข้อมูลใหม่
collection.insert_many(data_dict)

print("Data cleaned and inserted into MongoDB successfully")

# from pymongo import MongoClient
# import datetime

# # MongoDB connection details
# mongo_host = '10.1.55.232'
# mongo_port = 27017  # default MongoDB port
# mongo_db = 'mydb'  # replace with your MongoDB database name
# mongo_collection = 'Ap'  # replace with your MongoDB collection name
# mongo_username = 'student'
# mongo_password = 'zaq12wsx1234'

# # Path to SNMP output file
# output_file = 'snmp_output.txt'

# # Connect to MongoDB
# try:
#     client = MongoClient(mongo_host, username=mongo_username, password=mongo_password, authSource='admin', authMechanism='SCRAM-SHA-256', port=mongo_port)
#     db = client[mongo_db]
#     collection = db[mongo_collection]
#     print("Connected to MongoDB successfully")
# except Exception as e:
#     print(f"Error connecting to MongoDB: {e}")
#     exit(1)

# # Read SNMP output file and insert into MongoDB
# try:
#     with open(output_file, 'r') as f:
#         lines = f.readlines()
#         for line in lines:
#             # Example parsing logic, adjust as per your SNMP output format
#             parts = line.split()
#             if len(parts) >= 4:
#                 timestamp = datetime.datetime.strptime(parts[0] + ' ' + parts[1], '%Y-%m-%d %H:%M:%S')
#                 oid = parts[3]
#                 value = ' '.join(parts[4:])
                
#                 # Example document structure, adjust as per your data
#                 document = {
#                     'timestamp': timestamp,
#                     'OID': oid,
#                     'value': value
#                 }
                
#                 # Insert document into MongoDB collection
#                 collection.insert_one(document)
#     print("Data inserted into MongoDB successfully")
# except Exception as e:
#     print(f"Error inserting data into MongoDB: {e}")

# # Disconnect from MongoDB
# client.close()


