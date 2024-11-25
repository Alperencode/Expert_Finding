from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time
from src import mongodb, search, fetch, utils

# Connect to the MongoDB collection
COLLECTION = mongodb.connect_db_collection(
    connection_string="mongodb://localhost:27018",
    db_string="openalexdb",
    collection_string="experts",
)

# Initialize FastAPI app
app = FastAPI()


# Request model for searching experts
class SearchRequest(BaseModel):
    topic: str
    filters: dict = None


@app.post("/search")
async def search_experts(request: SearchRequest):
    """
    Search experts for a given topic. Return the full object as stored in the database.
    """
    result = dict()
    start_time = time.time()

    # Get topic from request
    topic = request.topic
    filters = None
    fined_filters = ""
    if request.filters:
        filters = request.filters
        fined_filters = utils.parse_filters(request.filters)

    # Check if topic exists in the database
    experts = mongodb.get_topic_experts_using_db(COLLECTION, topic, filters)
    result = {
        "source": "database",
        "topic": topic,
        "experts": experts
    }

    # If topic doesn't exist, fetch from API and store
    if not experts:
        print("Topic doesn't exist in database, using API...")
        experts = search.extract_experts_using_api(topic, fined_filters)
        if experts:
            # Save the topic and experts into the database
            result["experts"] = experts
            result["source"] = "api"
            mongodb.add_topic_and_experts(COLLECTION, topic, experts, filters)
        else:
            raise HTTPException(status_code=404, detail="Couldn't find any experts for this topic.")

    elapsed_time = time.time() - start_time
    result["elapsed_time"] = f"{float(elapsed_time):.2f} seconds"

    return result


@app.get("/expert/{name}")
async def get_expert_details(name: str):
    result = dict()
    topics = mongodb.get_all_topics(COLLECTION)
    for topic in topics:
        expert = next((e for e in topic["experts"] if e["expert_name"].lower() == name.lower()), None)
        if expert:
            result["source"] = "database"
            result["expert"] = utils.generate_expert_info(expert)
            return result

    print(f"Expert not found in DB, using authors API with ID: {name}")

    author = fetch.fetch_author(name)
    if author:
        result["source"] = "api"
        result["author"] = utils.generate_author_info(author)
        return result

    raise HTTPException(status_code=404, detail="Expert not found.")


if __name__ == "__main__":
    import uvicorn

    # Run the FastAPI app
    uvicorn.run(app, host="127.0.0.1", port=8000)
