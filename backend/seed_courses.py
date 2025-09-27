#seed_courses.py

import json
from pymongo import MongoClient
from urllib.parse import quote_plus
import os

MONGO_USER = "harsh_db_user"
MONGO_PASS = "Harshitha8"  # raw password, even if it has @, #, :, etc.
MONGO_DB = "upskill_advisor"
encoded_pass = quote_plus(MONGO_PASS)

    # build a safe Mongo URI
MONGO_URI = f"mongodb+srv://{MONGO_USER}:{encoded_pass}@cluster0.lsxfc4a.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


# Load env vars (or paste directly here for now)

DB_NAME = os.getenv("MONGO_DB", "upskill_advisor")
COLLECTION_NAME = os.getenv("MONGO_COLLECTION", "courses")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Load courses.json
with open("data/courses.json", "r") as f:
    courses = json.load(f)

# Insert each course as a separate document, with the course name as a field
if isinstance(courses, dict):
    docs = []
    for name, data in courses.items():
        doc = {"name": name}
        doc.update(data)
        docs.append(doc)
    if docs:
        collection.insert_many(docs)
    print(f"Inserted {len(docs)} courses into MongoDB!")
else:
    print("courses.json is not a dict. No courses inserted.")