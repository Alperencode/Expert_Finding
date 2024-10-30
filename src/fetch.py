import requests


def fetch_works(params):
    response = requests.get("https://api.openalex.org/works", params=params)
    if response.status_code == 200:
        return response.json()["results"]
    else:
        print(f"Error: {response.status_code}")
        return []


def fetch_author(author_id):
    url = f"https://api.openalex.org/authors/{author_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
