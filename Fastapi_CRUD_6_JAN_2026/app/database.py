from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

mongo_url = os.getenv("MONGO_URL")
if not mongo_url:
    raise ValueError("URL is not set in environment.")

client = MongoClient(mongo_url)
db = client["crud_database"]
collection = db["items"]

