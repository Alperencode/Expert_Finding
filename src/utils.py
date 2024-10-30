import time


def create_expert_display_string(expert):
    return (
        f"Name: {expert['expert_name']}\n" +
        f"ID: {expert['expert_id']}\n" +
        f"Expert's h index: {expert['expert_h_index']}\n" +
        f"Expert's works count: {expert['expert_works_count']}\n" +
        f"Expert's Cited by Count: {expert['expert_cited_by_count']}\n" +
        f"Expert's affiliation: {expert['expert_affiliation']}\n" +
        f"Expert's country code: {expert['expert_country_code']}\n" +
        f"Expert score: {expert['expert_score']}\n"
    )


def get_recent_years(num_years=2):
    current_year = time.localtime().tm_year
    return [current_year - i for i in range(num_years)]
