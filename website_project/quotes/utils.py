from pymongo import MongoClient


def get_mongodb():
    client = MongoClient('mongodb://localhost')
    db = client.Module_10_Home_Work_WEB
    return db
