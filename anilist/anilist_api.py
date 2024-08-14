import requests
import logging
import json

def fetch_anime_suggestions(search_term):
    url = 'https://graphql.anilist.co'
    
    try:
        with open('anilist/fetch_anime.gql', 'r') as file:
            query = file.read()
    except FileNotFoundError:
        logging.error("GraphQL query file not found")
        return []

    variables = {
        'search_term': search_term,
        'page': 1,
        'perPage': 5
    }

    try:
        response = requests.post(url, json={'query': query, 'variables': variables})
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.json()
    except requests.RequestException as e:
        logging.error(f"API request failed: {e}")
        if hasattr(e.response, 'text'):
            logging.error(f"Response content: {e.response.text}")
        return []

    anime_list = []
    if data and 'data' in data and 'Page' in data['data'] and 'media' in data['data']['Page']:
        for anime in data['data']['Page']['media']:
            title = anime['title']['english'] or anime['title']['romaji']
            anime_list.append(title)
    else:
        logging.warning(f"Unexpected API response structure: {json.dumps(data, indent=2)}")

    return anime_list
