import json
from bson import ObjectId

from pymongo import MongoClient

client = MongoClient("mongodb://localhost")  # "mongodb://localhost" - protocol

db = client.Module_10_Home_Work_WEB

with open("quotes.json", "r", encoding="utf-8") as fd:
    quotes = json.load(fd)

for quote in quotes:
    author = db.authors.find_one({"fullname": quote["author"]})
    if author:
        db.quotes.insert_one({
            "quote": quote["quote"],
            "tags": quote["tags"],
            "author": ObjectId(author["_id"]),
        })

