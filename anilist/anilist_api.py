import requests

def fetch_anime_suggestions(search_term):
    url = 'https://graphql.anilist.co'
    
    with open('anilist/fetch_anime.gql', 'r') as file:
        query = file.read()

    variables = {
        'search': search_term,
        'page': 1,
        'perPage': 10
    }

    response = requests.post(url, json={'query': query, 'variables': variables})
    data = response.json()

    anime_list = []
    if 'data' in data and 'Page' in data['data'] and 'media' in data['data']['Page']:
        for anime in data['data']['Page']['media']:
            title = anime['title']['english'] or anime['title']['romaji']
            anime_list.append(title)

    return anime_list
