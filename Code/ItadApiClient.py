import requests
from GameMapper import GameMapper

class ItadApiClient:
    def __init__(self):
        self
        
    def fetchFreeGames(self, apiKey):
        httpResponse = requests.get(f"https://api.isthereanydeal.com/deals/v2?key={apiKey}&country=CH&shops=61&sort=price")
        games = GameMapper.mapMultipleFromJson(httpResponse.json())
        return games