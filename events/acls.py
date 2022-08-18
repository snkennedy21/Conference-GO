from .keys import PEXELS_API_KEY, OPEN_WEATHER_API_KEY

import json
import requests


def get_picture(city, state):
    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": f"{city} {state}", "page": 1, "per_page": 1}
    response = requests.get(url, headers=headers, params=params)
    data = json.loads(response.content)
    picture_url = data['photos'][0]['src']['original']
    return {"picture_url": picture_url}
