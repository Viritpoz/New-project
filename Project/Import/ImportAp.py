import pandas as pd
from pymongo import MongoClient

# Read the CSV file
file_path = 'Data/CSV/Cleaned.csv'
df = pd.read_csv(file_path)

# Drop rows with null values in 'AP Name', 'Ethernet MAC'
df_cleaned = df.dropna(subset=['AP Name', 'Ethernet MAC'])

# Select specific columns for MongoDB insertion
df_final = df_cleaned[['AP Name', 'Ethernet MAC']]

# Convert DataFrame to dictionary for MongoDB insertion
data_dict = df_final.to_dict(orient='records')

# Connect to MongoDB
client = MongoClient('mongodb://10.1.55.232:27017/')
db = client['mydb']
collection = db['Ap']

# Clear the existing data in the collection
collection.delete_many({})

# Insert new data into the collection
if data_dict:
    collection.insert_many(data_dict)
    print("Data cleaned and inserted into MongoDB successfully")
else:
    print("No data to insert")

