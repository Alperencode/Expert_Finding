from src import fetch, mongodb, search

# OpenAlex API
API_URL = "https://api.openalex.org/works"
PARAMS = {
    "sort": "cited_by_count:DESC",
    "per_page": 50
}


if __name__ == "__main__":
    # TO-DO:
    # - Add only experts to the database (DONE)
    # - Add their unique identifier to database (DONE)
    #   - https://api.openalex.org/works/{id}
    #   - https://api.openalex.org/authors/{id}
    # - If topic already exists in database
    #   - Search database for experts
    #   - Gather main data keys for the following expert using its unique identifier
    # - If topic does not exists, use API (DONE)
    # - Add topic and its experts with their unique identifiers to database (DONE)

    # Connect to db and collection
    collection = mongodb.connect_db_collection(
        connection_string="mongodb://localhost:27018",
        db_string="openalexdb",
        collection_string="experts",
    )

    # Determine the search topic
    topic = "artificial intelligence"
    PARAMS['filter'] = f"display_name.search:{topic}"

    # Fetch works
    works = fetch.fetch_works(API_URL, PARAMS)
    experts = dict()
    if works:
        # Extract experts
        experts = search.extract_experts(works, topic)

        # Add topic and experts to MongoDB
        mongodb.add_topic_and_experts(collection, topic, experts)
    else:
        print("No works found or an error occurred.")

    print(f"\nExperts found: {len(experts)}")
