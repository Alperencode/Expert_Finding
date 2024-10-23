from pymongo import MongoClient
import hashlib


def connect_db_collection(connection_string, db_string, collection_string):
    client = MongoClient(connection_string)
    db = client[db_string]
    collection = db[collection_string]

    return collection


def add_topic_and_experts(collection, topic, experts):
    topic_exists = collection.find_one({"topic": topic})
    if topic_exists:
        collection.update_one(
            {"topic": topic},
            {"$set": {"experts": experts}}
        )
        return

    collection.insert_one({
        "_id": int(hashlib.sha1(topic.encode("utf-8")).hexdigest(), 16) % (10 ** 8),
        "topic": topic,
        "experts": experts
    })


def get_topic_experts_using_db(collection, topic):
    topic = collection.find_one({"topic": topic})
    if topic:
        return topic["experts"]
    return None
