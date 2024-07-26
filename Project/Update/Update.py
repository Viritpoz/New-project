import csv
import re
import pandas as pd
import os
from datetime import datetime

# ข้อมูลไฟล์
txt_file_path = 'Data/snmp_output.txt'  # Path to the text file
csv_file_path = 'Data/CSV/New.csv'  # Path to the existing CSV file
output_csv_path = 'Data/CSV/New.csv'  # Path to the output CSV file
cleaned_csv_path = 'Data/CSV/Cleaned.csv'  # Path to the cleaned CSV file

# สร้างชื่อไฟล์ History.csv ตามวันที่และเวลา
current_time = datetime.now().strftime("%d-%m-%Y_%H-%M")
history_csv_path = f'History/History_{current_time}.csv'

# รูปแบบการจับคู่ที่ต้องการ
student_id_pattern = re.compile(r'iso\.3\.6\.1\.4\.1\.9\.9\.599\.1\.3\.1\.1\.27\.\d+\.\d+\.\d+\.\d+\.\d+\.\d+ = (?:STRING: )?"([^"]*)"')
profile_pattern = re.compile(r'iso\.3\.6\.1\.4\.1\.9\.9\.599\.1\.3\.1\.1\.28\.\d+\.\d+\.\d+\.\d+\.\d+\.\d+ = STRING: "([^"]+)"')
hexstring_pattern = re.compile(r'iso\.3\.6\.1\.4\.1\.9\.9\.599\.1\.3\.1\.1\.8\.\d+\.\d+\.\d+\.\d+\.\d+\.\d+ = Hex-STRING: ([0-9A-Fa-f ]+)')

# ฟังก์ชันจัดรูปแบบ HEX-STRING
def format_hexstring(hexstring):
    hexstring = hexstring.replace(' ', '').lower()  # Remove spaces and convert to lowercase
    groups = [hexstring[i:i+4] for i in range(0, len(hexstring), 4)]  # Split into groups of 4 characters
    return '.'.join(groups)  # Join groups with dots

# อ่านไฟล์ TXT และดึงข้อมูลที่เกี่ยวข้อง
with open(txt_file_path, 'r') as txt_file:
    txt_content = txt_file.read()
    student_ids = student_id_pattern.findall(txt_content)
    profiles = profile_pattern.findall(txt_content)
    hexstrings = [format_hexstring(hs) for hs in hexstring_pattern.findall(txt_content)]

# อ่านไฟล์ CSV ที่มีอยู่และอัปเดตข้อมูล
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    csv_data = list(csv_reader)

header = csv_data[0]
columns_to_add = {"Student ID": student_ids, "Profile": profiles, "HexString": hexstrings}

for column in columns_to_add.keys():
    if column not in header:
        header.append(column)

for i, row in enumerate(csv_data[1:], start=1):
    for column in columns_to_add.keys():
        column_index = header.index(column)
        if len(row) < len(header):
            row.extend([''] * (len(header) - len(row)))

max_len = max(len(student_ids), len(profiles), len(hexstrings))

for _ in range(max_len - len(csv_data) + 1):
    csv_data.append([''] * len(header))

for i in range(max_len):
    row_index = i + 1
    if row_index < len(csv_data):
        for column, values in columns_to_add.items():
            column_index = header.index(column)
            if i < len(values):
                csv_data[row_index][column_index] = values[i]

with open(output_csv_path, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerows(csv_data)

print("Student IDs, Profiles, and Hexstring have been added to the CSV file.")

# อ่านไฟล์ CSV ที่อัปเดตแล้วและล้างข้อมูล
df = pd.read_csv(output_csv_path)
df_cleaned = df.copy()

df_cleaned.loc[df_cleaned['Student ID'].isna() | df_cleaned['Student ID'].eq(''), ['Profile', 'HexString']] = ''
df_cleaned = df_cleaned.dropna(subset=['Student ID', 'Ethernet MAC', 'AP Name'], how='all')

# บันทึก DataFrame ที่ล้างแล้วลงในไฟล์ CSV ใหม่
df_cleaned.to_csv(cleaned_csv_path, index=False)

# ตรวจสอบว่ามีไฟล์ History.csv อยู่แล้วหรือไม่
if os.path.exists(history_csv_path):
    # อ่านข้อมูลจาก History.csv
    df_history = pd.read_csv(history_csv_path)
    # รวมข้อมูลใหม่เข้ากับข้อมูลเก่า
    df_combined = pd.concat([df_history, df_cleaned], ignore_index=True)
else:
    # ถ้ายังไม่มี History.csv ให้ใช้ข้อมูลที่ล้างแล้วเป็นข้อมูลแรก
    df_combined = df_cleaned

# บันทึกข้อมูลรวมลงใน History.csv
df_combined.to_csv(history_csv_path, index=False)

print("Data has been saved to History.csv.")
print(df_cleaned)
