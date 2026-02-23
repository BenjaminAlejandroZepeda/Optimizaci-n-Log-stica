from pymongo import MongoClient
from decisionengine.config.settings import MONGO_URI


def test_mongo_connection():
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    result = client.admin.command("ping")
    assert result["ok"] == 1.0