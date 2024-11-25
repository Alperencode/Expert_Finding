from pymongo import MongoClient
import hashlib


def connect_db_collection(connection_string, db_string, collection_string):
    client = MongoClient(connection_string)
    db = client[db_string]
    collection = db[collection_string]

    return collection


def add_topic_and_experts(collection, topic, experts, filters):
    topic_exists = collection.find_one({"topic": topic, "filters": filters})
    if topic_exists:
        collection.update_one(
            {"topic": topic},
            {"$set": {"experts": experts, "filters": filters}}
        )
        return

    identifier = topic
    if filters:
        identifier += str(filters)

    collection.insert_one({
        "_id": int(hashlib.sha1(identifier.encode("utf-8")).hexdigest(), 16) % (10 ** 8),
        "topic": topic,
        "experts": experts,
        "filters": filters
    })


def get_topic_experts_using_db(collection, topic, filters):
    topic = collection.find_one({"topic": topic, "filters": filters})
    if topic:
        return topic["experts"]
    return None


def get_all_topics(collection):
    return list(collection.find({}, {"_id": 0, "topic": 1, "experts": 1}))
