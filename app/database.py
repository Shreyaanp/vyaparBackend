from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client.get_database(os.getenv("DB_NAME"))

def init_db():
    # Add any initialization code here if needed
    pass
