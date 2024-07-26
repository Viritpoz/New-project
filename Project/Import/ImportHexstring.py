import pandas as pd
import re
from pymongo import MongoClient

# อ่านไฟล์ CSV
file_path = 'Data/CSV/Cleaned.csv'
df = pd.read_csv(file_path)

# ดรอปแถวที่มีค่า null ในคอลัมน์ 'Student ID'
df_cleaned = df.dropna(subset=['HexString'])

# เลือกเฉพาะคอลัมน์ 'Student ID' สำหรับนำไปใช้งาน
df_final = df_cleaned[['HexString']]

# แปลง DataFrame เป็น dict เพื่อเตรียมสำหรับการอัพเดตใน MongoDB
data_dict = df_final.to_dict(orient='records')

# เชื่อมต่อกับ MongoDB
client = MongoClient('mongodb://10.1.55.232:27017/')
db = client['mydb']
collection = db['HexString']

# ลบข้อมูลเก่าทั้งหมดในคอลเล็กชัน
collection.delete_many({})

# แทรกข้อมูลใหม่
collection.insert_many(data_dict)

print("Data cleaned and inserted into MongoDB successfully")
