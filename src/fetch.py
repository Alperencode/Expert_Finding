import requests


def fetch_works(search_url, params):
    response = requests.get(search_url, params=params)
    if response.status_code == 200:
        return response.json()["results"]
    else:
        print(f"Error: {response.status_code}")
        return []


def fetch_author(authorID):
    response = requests.get(f"https://api.openalex.org/authors/{authorID}")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return []
