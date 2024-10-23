from pymongo import MongoClient


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
        "topic": topic,
        "experts": experts
    })
