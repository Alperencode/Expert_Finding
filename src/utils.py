def create_expert_display_string(expert):
    return (
        f"Name: {expert['name']}\n" +
        f"ID: {expert['id']}\n" +
        f"Work ID: {expert['work_id']}\n" +
        f"Expert's Cited by Count: {expert['author_cited_by_count']}\n" +
        f"Expert's h index: {expert['author_h_index']}\n"
    )
