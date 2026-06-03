import json
from GameMapper import GameMapper

class DealCollection:
    def __init__(self):
        self.games = self.load_games()
        
    def load_games(self):
        file = open("games.json")
        data = json.load(file)
        games = GameMapper.mapMultipleFromJson(data)
        return games
    
    def load_new_games(self, new_games):
        new_games_to_return = []
        existing_ids = {game.id for game in self.games}

        for new_game in new_games:
            if new_game.id in existing_ids:
                continue

            if new_game.isFree:
                self.games.append(new_game)
                new_games_to_return.append(new_game)
                existing_ids.add(new_game.id)

        self.save_games()
        return new_games_to_return
    
    def save_games(self):
        file = open("games.json", "w")
        games = []
        for game in self.games:
            if game.isFree:
                game_dict = {
                    'id': game.id,
                    'slug': game.slug,
                    'title': game.title,
                    'type': game.type,
                    'mature': game.mature,
                    'isFree': game.isFree,
                    'price': game.price,
                    'cut': game.cut,
                    'url': game.url,
                    'expiry': game.expiry
                }
                games.append(game_dict)
        json.dump(games, file, indent=2)
        print("Successfully saved games")