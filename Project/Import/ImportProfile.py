import pandas as pd
import re
from pymongo import MongoClient


# อ่านไฟล์ CSV
file_path = 'Data/CSV/Cleaned.csv'
df = pd.read_csv(file_path)


# ดรอปแถวที่มีค่า null ในคอลัมน์ 'Profile'
df_cleaned = df.dropna(subset=['Profile'])

# เลือกเฉพาะคอลัมน์ 'Profile' สำหรับนำไปใช้งาน
df_final = df_cleaned[['Profile']]

# เลือกเฉพาะคอลัมน์ที่ต้องการจะเพิ่มลงใน MongoDB (Profile และ OID)
df_final = df_cleaned[['Profile']]

# แปลง DataFrame เป็น dict เพื่อเตรียมสำหรับการอัพเดตใน MongoDB
data_dict = df_final.to_dict(orient='records')

# เชื่อมต่อกับ MongoDB
client = MongoClient('mongodb://10.1.55.232:27017/')
db = client['mydb']
collection = db['Profile']

# ลบข้อมูลเก่าทั้งหมดในคอลเล็กชัน
collection.delete_many({})

# แทรกข้อมูลใหม่
collection.insert_many(data_dict)

print("Data cleaned and inserted into MongoDB successfully")
