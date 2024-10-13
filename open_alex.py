from src import fetch, mongodb, search

# OpenAlex API
API_URL = "https://api.openalex.org/works"
PARAMS = {
    "sort": "cited_by_count:DESC",
    "per_page": 50
}


if __name__ == "__main__":
    # TO-DO:
    # - Add only experts to the database
    # - Add their unique identifier to database
    # - If topic already exists in database
    #   - Search database for experts
    #   - Gather main data keys for the following expert using its unique identifier
    # - If topic does not exists, use API
    # - Add topic and the its experts with unique identifiers to database

    # Connect to db and collection
    collection = mongodb.connect_db_collection(
        connection_string="mongodb://localhost:27017/",
        db_string="openalexdb",
        collection_string="works",
    )

    # Determine the search topic
    topic = "artificial intelligence"

    # Fetch works
    works = fetch.fetch_works(API_URL, PARAMS)
    if works:
        # Add works to db [excluding duplicates]
        mongodb.add_to_mongodb(collection, works)

        # Find experts on the selected topic
        experts = search.find_experts(collection, topic)
        if experts:
            for expert in experts:
                print(expert)
        else:
            print("No experts found.")
    else:
        print("No works found or an error occurred.")

    print(f"\nParsed object: {len(works)}")
    print(f"Parsed fields: {len(works[0].keys()) * len(works)}")
    print(f"Experts found: {len(experts)}")
