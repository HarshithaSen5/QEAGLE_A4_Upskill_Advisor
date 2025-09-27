# backend/services/retriever.py
import json
import os
from pathlib import Path
from pymongo import MongoClient
import pinecone
from langchain_community.vectorstores import MongoDBAtlasVectorSearch, Pinecone
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings

# Local fallback embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


# -------------------
# JSON Loaders (your existing code)
# -------------------
def load_job_description(role: str):
    """Load required skills for a given role from jds.json"""
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, "..", "data", "jds.json")

    with open(file_path, "r") as f:
        jds = json.load(f)

    # Check if role exists
    for job_role, skills in jds.items():
        if job_role.lower() == role.lower():
            return skills  # dict of categories (core, tools, etc.)

    return {}


def load_courses():
    """Load available courses from courses.json"""
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, "..", "data", "courses.json")

    with open(file_path, "r") as f:
        courses = json.load(f)

    return courses


# -------------------
# Vector DB Retrievers
# -------------------
def get_mongo_retriever(uri: str, db_name: str, collection_name: str):
    """Connect to MongoDB Atlas Vector Search"""
    client = MongoClient(uri)
    collection = client[db_name][collection_name]
    return MongoDBAtlasVectorSearch(collection, embedding_model)


def get_pinecone_retriever(api_key: str, index_name: str, environment="us-east1-gcp"):
    """Connect to Pinecone Vector DB"""
    pinecone.init(api_key=api_key, environment=environment)
    index = pinecone.Index(index_name)
    return Pinecone(index, embedding_model.embed_query, "text")


# -------------------
# Keyword-based fallback (BM25/Elastic-like)
# -------------------
def keyword_search(role: str, query: str):
    """
    Simple keyword-based fallback search inside jds.json
    """
    jd = load_job_description(role)
    results = []
    for category, skills in jd.items():
        for skill in skills:
            if query.lower() in skill.lower():
                results.append(skill)
    return results