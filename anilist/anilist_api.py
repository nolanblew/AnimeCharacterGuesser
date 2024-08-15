import requests
import logging
import json
import re

def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

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
            anime_info = {
                'id': anime['id'],
                'title': title,
                'coverImage': anime['coverImage']['medium'],
                'season': anime['season'],
                'seasonYear': anime['seasonYear'],
                'format': anime['format'],
                'description': clean_html(anime['description']) if anime['description'] else ''
            }
            anime_list.append(anime_info)
    else:
        logging.warning(f"Unexpected API response structure: {json.dumps(data, indent=2)}")

    return anime_list

def fetch_characters(anime_id):
    url = 'https://graphql.anilist.co'
    
    try:
        with open('anilist/fetch_characters.gql', 'r') as file:
            query = file.read()
    except FileNotFoundError:
        logging.error("GraphQL query file for characters not found")
        return [], ''

    variables = {
        'anime_id': anime_id,
        'page': 1,
        'per_page': 10
    }

    try:
        response = requests.post(url, json={'query': query, 'variables': variables})
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        logging.error(f"API request failed: {e}")
        if hasattr(e.response, 'text'):
            logging.error(f"Response content: {e.response.text}")
        return [], ''

    characters = []
    anime_description = ''
    if data and 'data' in data and 'Media' in data['data']:
        anime_description = clean_html(data['data']['Media']['description']) if data['data']['Media']['description'] else ''
        if 'characters' in data['data']['Media']:
            for character in data['data']['Media']['characters']['nodes']:
                character_info = {
                    'name': character['name']['full'],
                    'image': character['image']['medium'],
                    'description': clean_html(character['description']) if character['description'] else ''
                }
                characters.append(character_info)
    else:
        logging.warning(f"Unexpected API response structure: {json.dumps(data, indent=2)}")

    return characters, anime_description
