import requests
from GameMapper import GameMapper

class ItadApiClient:
    def __init__(self):
        self
        
    def fetchFreeGames(self):
        httpResponse = requests.get("https://api.isthereanydeal.com/deals/v2?key=9ac875596860b62aa398c2f384ff369d51f17286&country=CH&shops=61&sort=price")
        games = GameMapper.mapMultipleFromJson(httpResponse.json())
        return games