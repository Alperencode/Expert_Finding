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

    for work in works:
        if not work or len(work['authorships']) <= 0:
            continue

        # Expert filters
        title = (topic.lower() in work["title"].lower())
        abstract = False
        if works[0]["abstract_inverted_index"]:
            abstract = (topic.lower() in [key.lower() for key in works[0]["abstract_inverted_index"].keys()])
        cited = work["cited_by_count"] >= 1000

        # Author informations
        authorID = work['authorships'][0]["author"]["id"].split("/")[-1]
        authorName = work['authorships'][0]["author"]["display_name"]
        workID = work["id"].split("/")[-1]

        if (title or abstract) and (cited):
            experts.append({
                "name": authorName,
                "id": authorID,
                "work_id": workID
            })
    return experts
