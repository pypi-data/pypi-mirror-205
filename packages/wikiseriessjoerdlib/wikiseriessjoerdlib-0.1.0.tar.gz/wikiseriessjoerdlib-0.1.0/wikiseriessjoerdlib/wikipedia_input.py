# wikipedia_input.py

import requests
from bs4 import BeautifulSoup as Bfs


def search_series(name):
    api_url = 'https://en.wikipedia.org/w/api.php'
    limit = 10
    term = f'List_of_{name}_episodes'
    parameters = {'action': 'opensearch',
                  'format': 'json',
                  'formatversion': '1',
                  'namespace': '0',
                  'limit': limit,
                  'search': term}
    search_response = requests.get(api_url, params=parameters, timeout=5)
    series_url = search_response.json()[3][0]
    series_response = requests.get(series_url, timeout=5)
    soup = Bfs(series_response.text, features="html.parser")
    overview_table = soup.find('table', class_='wikitable')
    season_numbers = [item.text for item in overview_table.find_all('span', class_='nowrap')]
    season_table = soup.find_all('table', class_='wikiepisodetable')
    return {f'Season {key}': [entry.text.split('"')[1]
                              for entry in value.find_all('td', class_='summary')]
            for key, value in dict(zip(season_numbers, season_table)).items()}
