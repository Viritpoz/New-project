import pandas as pd
from pymongo import MongoClient

file_path = 'Data/CSV/Cleaned.csv'
df = pd.read_csv(file_path)

# Convert DataFrame to a list of dictionaries
data_dict = df.to_dict(orient='records')

# Connect to MongoDB
client = MongoClient('mongodb://10.1.55.232:27017/')
db = client['mydb']
collection = db['DATA']

# Delete old data
collection.delete_many({})

# Insert new data
if data_dict:
    collection.insert_many(data_dict)

print("Data cleaned and inserted into MongoDB successfully")
