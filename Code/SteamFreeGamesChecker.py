from ItadApiClient import ItadApiClient as Client
from DealCollection import DealCollection
from ConfigReader import ConfigReader as reader
from Message import Message

class SteamFreeGamesChecker:
    def fetchGames(self):
        client = Client()
        r = reader()
        d = DealCollection()
        config = r.read_config_file()
        games = client.fetchFreeGames(config["APIKey"])
        d.load_new_games(games)
        for game in games:
            if game.isFree:
                print(game.title)
        m = Message(games)
        print(m.create_message())