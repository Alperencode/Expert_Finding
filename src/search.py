

def extract_experts(works, topic):
    experts = list()
    for work in works:
        if len(work['authorships']) <= 0:
            continue

        # Expert filters
        title = (topic.lower() in work["title"].lower())
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
