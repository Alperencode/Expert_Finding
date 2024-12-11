from .fetch import fetch_works, fetch_author
from .utils import get_recent_years, parse_topics
from collections import defaultdict


def extract_experts_using_api(topic, filters=None):
    experts = list()

    # Fetch works from OpenAlex API
    query_topic = parse_topics(topic)
    PARAMS = {
        "filter": f"default.search:{query_topic}" + filters,
        "select": "doi,title,display_name,relevance_score,publication_year," +
        "publication_date,primary_location,open_access,authorships," +
        "cited_by_count,biblio,primary_topic,abstract_inverted_index,id",
        "sort": "cited_by_count:DESC",
        "per_page": 50
    }
    works = fetch_works(PARAMS)
    if not works:
        return None

    # First work traverse: calculate the average cited by count and relevance score
    total_citations = 0
    total_relevance = 0
    valid_works_count = 0
    for work in works:
        valid_works_count += 1
        if ('cited_by_count' in work):
            total_citations += work['cited_by_count']
        if ('relevance_score' in work):
            total_relevance += work['relevance_score']

    # Avoid division by zero if no valid works were fetched
    avg_cited_by_count = total_citations / valid_works_count
    avg_relevance = total_relevance / valid_works_count

    # Second work traverse: filter authors based on basic filters
    filtered_authors = []
    for work in works:
        if not work or len(work['authorships']) <= 0:
            continue

        # Expert filters
        topics = [t.strip() for t in topic.split(",")]
        title_match = any(t.lower() in work["title"].lower() for t in topics) if work["title"] else False
        abstract_match = any(
            t.lower() in word.lower()
            for t in topics
            for word in work["abstract_inverted_index"]
        ) if work["abstract_inverted_index"] else False
        cited_above_average = work["cited_by_count"] >= avg_cited_by_count
        relevance_above_average = work["relevance_score"] >= avg_relevance

        # Author information
        author_id = work['authorships'][0]["author"]["id"].split("/")[-1]
        author_name = work['authorships'][0]["author"]["display_name"]
        author_country_code = None
        if work['authorships'][0]["countries"]:
            author_country_code = work['authorships'][0]["countries"][0]

        # Filter out experts using basic parameters
        if not (title_match or abstract_match) or ((not cited_above_average) or (not relevance_above_average)):
            continue
        filtered_authors.append({
            "author_name": author_name,
            "author_id": author_id,
            "author_country_code": author_country_code
        })

    print(f"{len(filtered_authors)} authors pass the first check.")
    print("Executing advanced expert calculation to sort experts.")
    experts = sort_experts(authors=filtered_authors, topic=topic)
    print("Sorted experts.")
    return experts


def sort_experts(authors, topic, notable_institutions=None, num_recent_years=2):
    # Default notable institutions, can be extended or customized as needed
    if notable_institutions is None:
        notable_institutions = {"Mila - Quebec Artificial Intelligence Institute", "Google", "Stanford"}

    recent_years = get_recent_years(num_recent_years)
    author_scores = defaultdict(float)
    author_profiles = {}

    for author in authors:
        author_name = author["author_name"]
        author_id = author["author_id"]

        # If author already exists in experts, add extra score and pass
        if author_name in author_profiles:
            author_scores[author_name] += 1.5
            continue

        # Fetch author data, skip if API request fails
        author_data = fetch_author(author_id)
        if not author_data:
            continue

        # Author data
        country_code = author["author_country_code"]
        author_h_index = works_count = None
        cited_by_count = institution = orcid = None

        if author_data['summary_stats']['h_index']:
            author_h_index = author_data['summary_stats']['h_index']
        if author_data['works_count']:
            works_count = author_data['works_count']
        if author_data['cited_by_count']:
            cited_by_count = author_data['cited_by_count']
        if author_data['last_known_institutions']:
            institution = author_data['last_known_institutions'][0]['display_name']
        if author_data['orcid']:
            orcid = author_data['orcid'].split("/")[-1]

        # Initialize the score for the author
        score = 1

        # Calculate Topic Concentration Score
        topic_count = sum(1 for t in author_data["topics"] if topic.lower() in t["display_name"].lower())
        topic_concentration_score = topic_count / works_count if works_count else 0
        score += topic_concentration_score

        # Calculate Recent Activity Score
        recent_activity_score = sum(
            year_data["works_count"] for year_data in author_data["counts_by_year"]
            if year_data["year"] in recent_years
        )
        score += recent_activity_score / 10  # Normalize weight for recent activity

        # Institutional Influence Score
        institution_influence_score = any(
            aff["institution"]["display_name"] in notable_institutions
            for aff in author_data["affiliations"]
        )
        score += 0.5 if institution_influence_score else 0  # Small boost for notable institutions

        # Weighted Citation Score for Topic
        topic_specific_citations = sum(
            t["count"] for t in author_data["topics"]
            if topic.lower() in t["display_name"].lower()
        )
        avg_topic_specific_citations = topic_specific_citations / max(topic_count, 1)
        score += avg_topic_specific_citations / 1000  # Normalize score
        # Assign authors score
        author_profiles[author_name] = {
            "id": author_id,
            "score": score,
            "h_index": author_h_index,
            "works_count": works_count,
            "cited_by_count": cited_by_count,
            "institution": institution,
            "country_code": country_code,
            "orcid": orcid
        }

    # Sort authors by score in descending order
    sorted_authors = sorted(author_profiles.items(), key=lambda item: item[1]["score"], reverse=True)

    # Format output
    sorted_experts = [{
        "expert_name": name,
        "expert_id": data["id"],
        "expert_score": data["score"],
        "expert_h_index": data["h_index"],
        "expert_works_count": data["works_count"],
        "expert_cited_by_count": data["cited_by_count"],
        "expert_institution": data["institution"],
        "expert_country_code": data["country_code"],
        "expert_orcid": data["orcid"]
    } for name, data in sorted_authors]

    return sorted_experts
