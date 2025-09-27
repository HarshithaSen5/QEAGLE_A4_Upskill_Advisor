#seed_jds.py
from pymongo import MongoClient
from urllib.parse import quote_plus

MONGO_USER = "harsh_db_user"
MONGO_PASS = "Harshitha8"  # raw password, even if it has @, #, :, etc.
MONGO_DB = "upskill_advisor"

def seed_job_descriptions():
    # encode the password safely
    encoded_pass = quote_plus(MONGO_PASS)

    # build a safe Mongo URI
    MONGO_URI = f"mongodb+srv://{MONGO_USER}:{encoded_pass}@cluster0.lsxfc4a.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

    # connect to MongoDB
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    collection = db["job_descriptions"]

    import os, json
    jd_path = os.path.join(os.path.dirname(__file__), "data", "jds.json")
    if os.path.exists(jd_path):
        with open(jd_path, "r") as f:
            job_descriptions = json.load(f)
        if isinstance(job_descriptions, dict):
            job_descriptions = list(job_descriptions.values())
        if job_descriptions:
            collection.insert_many(job_descriptions)
            print(f"✅ {len(job_descriptions)} job descriptions seeded from jds.json!")
        else:
            print("No job descriptions found in jds.json.")
    else:
        # fallback to sample data
        job_descriptions = [
            {"role": "Data Analyst", "skills": ["sql", "excel", "python", "tableau"]},
            {"role": "Backend Developer", "skills": ["python", "django", "rest api", "mongodb"]},
            {"role": "Frontend Developer", "skills": ["javascript", "react", "css", "html"]},
        ]
        collection.insert_many(job_descriptions)
        print("✅ Sample job descriptions seeded!")

if __name__ == "__main__":
    seed_job_descriptions()