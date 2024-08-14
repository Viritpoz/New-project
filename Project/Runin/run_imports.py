import subprocess
import time
import os

def run_script(script_name):
    try:
        result = subprocess.run(['python', script_name], check=True, text=True, capture_output=True)
        print(f"ผลลัพธ์ของ {script_name}:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"เกิดข้อผิดพลาดขณะเรียกใช้ {script_name}:\n{e.stderr}")

def wait_for_completion(log_file, oids, timeout=600):
    """ รอให้ไฟล์ log เสร็จสิ้นการทำงาน """
    start_time = time.time()
    while time.time() - start_time < timeout:
        if os.path.exists(log_file):
            print("พบไฟล์ log แล้ว กำลังตรวจสอบเนื้อหา...")
            # ตรวจสอบว่าไฟล์ `log_file` ไม่มีการเขียนข้อมูลใหม่
            with open(log_file, 'r') as f:
                content = f.read()
                print("เนื้อหาไฟล์ log:\n", content)
                # ตรวจสอบว่าการทำงาน SNMP walk สำเร็จสำหรับทุก OID
                completed_oids = [oid for oid in oids if f"SNMP walk completed successfully for OID {oid}" in content]
                if len(completed_oids) == len(oids):
                    return True
        else:
            print(f"ไฟล์ {log_file} ยังไม่พบ")
        time.sleep(10)  # รอ 10 วินาทีแล้วลองใหม่
    return False

if __name__ == "__main__":
    # ใช้ double backslashes หรือ raw strings ในเส้นทาง Windows
    log_file = r'../Data/Script.txt'
    # รายการ OIDs ที่คาดหวังว่าจะเสร็จสิ้น
    oids = [
        # studentID
        '1.3.6.1.4.1.9.9.599.1.3.1.1.27',
        # Profile
        '1.3.6.1.4.1.9.9.599.1.3.1.1.28',
        # MAC Address
        '1.3.6.1.4.1.9.9.599.1.3.1.1.8'
    ]

    # รอจนกว่าไฟล์ `Script.txt` จะเสร็จสิ้นการทำงาน
    print("กำลังรอให้ SNMP walk เสร็จสิ้น...")
    if wait_for_completion(log_file, oids):
        print("SNMP walk เสร็จสิ้นแล้ว เริ่มอัปเดต MongoDB")
        
        scripts = [
            'Import/ImportAp.py',
            'Import/ImportData.py',
            'Import/ImportStid.py',
            'Import/ImportProfile.py',
            'Import/ImportHexstring.py'
        ]
        
        for script in scripts:
            run_script(script)
    else:
        print("หมดเวลาในการรอ SNMP walk เสร็จสิ้น หรือไม่พบข้อมูลที่คาดหวังในไฟล์ log")
