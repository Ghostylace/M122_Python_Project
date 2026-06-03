from Game import Game

class GameMapper:
    def map(jsonGame):
        try:
            isFree = jsonGame['deal']['price']['amount'] == 0
            game = Game(jsonGame['id'], jsonGame['slug'], jsonGame['title'], jsonGame['type'], jsonGame['mature'], isFree, jsonGame['deal']['price']['amount'], jsonGame['deal']['cut'], jsonGame['deal']['url'], jsonGame['deal']['expiry'])
        except KeyError:
            game = Game(jsonGame['id'], jsonGame['slug'], jsonGame['title'], jsonGame['type'], jsonGame['mature'], jsonGame['isFree'], jsonGame['price'], jsonGame['cut'], jsonGame['url'], jsonGame['expiry'])
        return game
    
    def mapMultipleFromJson(json):
        try:
            gamesList = json['list']
        except:
            gamesList = json
        games = []
        for game in gamesList:
            games.append(GameMapper.map(game))
            
        return games