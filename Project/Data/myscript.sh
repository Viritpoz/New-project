#!/bin/bash

COMMUNITY='mfunet'
HOST='172.30.99.11'
OIDS=('1.3.6.1.4.1.9.9.599.1.3.1.1.27' '1.3.6.1.4.1.9.9.599.1.3.1.1.28' '1.3.6.1.4.1.9.9.599.1.3.1.1.8')
OUTPUT_FILE="/home/student/shared_data/snmp_output.txt"
LOG_FILE="/home/student/shared_data/Script.txt"


# Clear the old output file content
> "$OUTPUT_FILE"

# Log a timestamp and message to indicate script execution
echo "$(date '+%Y-%m-%d %H:%M:%S') - Starting SNMP walk for OIDs ${OIDS[@]}" >> "$LOG_FILE"

# Loop through OIDs and perform SNMP walk for each
for OID in "${OIDS[@]}"; do
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Walking OID $OID" >> "$LOG_FILE"
    snmpwalk -v1 -c "$COMMUNITY" "$HOST" "$OID" >> "$OUTPUT_FILE" 2>> "$LOG_FILE"

    # Check the exit status of snmpwalk command
    if [ $? -ne 0 ]; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') - SNMP walk failed with OID $OID" >> "$LOG_FILE"
    else
        echo "$(date '+%Y-%m-%d %H:%M:%S') - SNMP walk completed successfully for OID $OID" >> "$LOG_FILE"
    fi
done

# เรียกใช้สคริปต์ Python เพื่ออัปเดตข้อมูลใน MongoDB
/usr/bin/python3 /home/student/run_imports.py