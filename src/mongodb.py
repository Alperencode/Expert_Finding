from pymongo import MongoClient


def connect_db_collection(connection_string, db_string, collection_string):
    client = MongoClient(connection_string)
    db = client[db_string]
    collection = db[collection_string]

    return collection


def add_to_mongodb(collection, works):
    for work in works:
        work_id = work['id']
        if not collection.find_one({"id": work_id}):
            collection.insert_one(work)
            print(f"Inserted: {work['title']}")
        else:
            print(f"Already exists: {work['title']}")
