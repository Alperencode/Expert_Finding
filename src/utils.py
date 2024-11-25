import time


def create_expert_display_string(expert):
    return (
        f"Name: {expert['expert_name']}\n" +
        f"ID: {expert['expert_id']}\n" +
        f"Expert's h index: {expert['expert_h_index']}\n" +
        f"Expert's works count: {expert['expert_works_count']}\n" +
        f"Expert's Cited by Count: {expert['expert_cited_by_count']}\n" +
        f"Expert's institution: {expert['expert_institution']}\n" +
        f"Expert's country code: {expert['expert_country_code']}\n" +
        f"Expert' orcid: {expert['expert_orcid']}\n" +
        f"Expert score: {round(expert['expert_score'], 2)}\n"
    )


def generate_expert_info(expert):
    return {
        "expert_name": expert["expert_name"],
        "expert_id": expert["expert_id"],
        "expert_institution": expert["expert_institution"],
        "expert_country_code": expert["expert_country_code"],
        "expert_h_index": expert["expert_h_index"],
        "expert_works_count": expert["expert_works_count"],
        "expert_cited_by_count": expert["expert_cited_by_count"],
        "expert_orcid": f"https://orcid.org/{expert['expert_orcid']}",
        "expert_url": f"https://openalex.org/authors/{expert['expert_id']}",
    }


def generate_author_info(author):
    result = dict()
    result["author_name"] = author["display_name"]
    result["author_id"] = author["id"].split("/")[-1]
    if author["summary_stats"]:
        result["author_h_index"] = author['summary_stats']['h_index']
    result["author_works_count"] = author["works_count"]
    result['author_cited_by_count'] = author['cited_by_count']
    if author['last_known_institutions']:
        result["author_institution"] = author["last_known_institutions"][0]["display_name"]
    if author['topics']:
        result["author_topics"] = [topic['display_name'] for topic in author['topics']]
    if author['orcid']:
        result["author_orcid"] = author['orcid']
    return result


def get_recent_years(num_years=2):
    current_year = time.localtime().tm_year
    return [current_year - i for i in range(num_years)]


def parse_filters(filters):
    if not filters:
        return ""
    fined_filters = []

    if 'expert_country' in filters:
        fined_filters.append(f"authorships.countries:{filters['expert_country']}")

    if 'article_language' in filters:
        fined_filters.append(f"language:{filters['article_language']}")

    if 'min_publication_year' in filters:
        fined_filters.append(f"publication_year:>{filters['min_publication_year']}")

    if 'min_publication_year' in filters:
        fined_filters.append(f"publication_year:>{filters['min_publication_year']}")

    fined_filters = ",".join(fined_filters)

    return f",{fined_filters}" if fined_filters else ""


def parse_topics(topics):
    return "|".join(t.strip().replace(" ", "+") for t in topics.split(","))
