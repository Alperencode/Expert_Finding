from src import fetch, mongodb

# OpenAlex API
API_URL = "https://api.openalex.org/works"
PARAMS = {
    "filter": "display_name.search:clickbait|data mining",
    "sort": "cited_by_count:DESC",
    "per_page": 50
}

if __name__ == "__main__":
    # Connect to db and collection
    mongodb.connect_db_collection(
        connection_string="mongodb://localhost:27017/",
        db_string="openalexdb",
        collection="works",
    )

    # Fetch works
    works = fetch.fetch_works(API_URL, PARAMS)

    # Add works to db
    if works:
        mongodb.add_to_mongodb(works)
    else:
        print("No works found or an error occurred.")
