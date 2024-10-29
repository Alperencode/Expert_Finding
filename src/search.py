from .fetch import fetch_works


def extract_experts_using_api(topic):
    experts = list()

    # Fetch works from OpenAlex API
    PARAMS = {
        "sort": "cited_by_count:DESC",
        "per_page": 50,
        "filter": f"display_name.search:{topic}"
    }
    works = fetch_works("https://api.openalex.org/works", PARAMS)
    if not works:
        return experts

    # First pass: calculate the average cited_by_count
    total_citations = 0
    valid_works_count = 0

    for work in works:
        if work and 'cited_by_count' in work:
            total_citations += work['cited_by_count']
            valid_works_count += 1

    # Avoid division by zero if no valid works were fetched
    avg_cited_by_count = total_citations / valid_works_count if valid_works_count > 0 else 0

    # Second pass: filter experts based on the average cited_by_count
    for work in works:
        if not work or len(work['authorships']) <= 0:
            continue

        # Expert filters
        title_match = (topic.lower() in work["title"].lower())
        abstract_match = False
        if work.get("abstract_inverted_index"):
            abstract_match = any(topic.lower() in word.lower() for word in work["abstract_inverted_index"])
        cited_above_average = work["cited_by_count"] >= avg_cited_by_count

        # Author information
        authorID = work['authorships'][0]["author"]["id"].split("/")[-1]
        authorName = work['authorships'][0]["author"]["display_name"]
        workID = work["id"].split("/")[-1]

        # Apply filters to identify experts
        if (title_match or abstract_match) and cited_above_average:
            experts.append({
                "name": authorName,
                "id": authorID,
                "work_id": workID
            })

    return experts
