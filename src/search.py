

def find_experts(collection, topic):
    if not topic:
        return []

    # Query explanation:
    # Searches topic in: "title", "abstract"
    # Gets articles that has at least 5 citations
    query = {
        "$or": [
            {"title": {"$regex": topic, "$options": "i"}},
            {"abstract": {"$regex": topic, "$options": "i"}},
            {"cited_by_count": {"$gte": 10000}}
        ]
    }

    # Query operators explanation:
    # `$or`: allows specify multiple conditions.
    # `"$options": "i"`: Makes the regex case-insensitive
    # `"$gte": 10000`: greater than or equal to 10.000

    works = list(collection.find(query))

    experts = [
        {
            "name": authorship['raw_author_name'],
            "title": work['title'],
            "id": work['id'],
        }
        for work in works
        if 'authorships' in work
        for authorship in work['authorships']
        if authorship["author_position"] == "first"
    ]

    return list(experts)
