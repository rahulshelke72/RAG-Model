from pymongo import MongoClient
from config.config import MONGODB_CONNECTION_STRING, DATABASE_NAME, COLLECTION_NAME

class MongoDBConnection:
    _instance = None

    @staticmethod
    def get_instance():
        if MongoDBConnection._instance is None:
            MongoDBConnection()
        return MongoDBConnection._instance

    def __init__(self):
        if MongoDBConnection._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.client = MongoClient(MONGODB_CONNECTION_STRING)
            self.db = self.client[DATABASE_NAME]
            self.collection = self.db[COLLECTION_NAME]
            MongoDBConnection._instance = self

    def close_connection(self):
        self.client.close()