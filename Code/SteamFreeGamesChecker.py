from ItadApiClient import ItadApiClient as Client
from DealCollection import DealCollection

class SteamFreeGamesChecker:
    def __init__(self):
        self
        
    def fetchGames(self):
        client = Client()
        games = client.fetchFreeGames()
        Deals = DealCollection(games)
        for game in games:
            if game.isFree:
                print(game.title)