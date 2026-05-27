from Game import Game

class GameMapper:
    def map(jsonGame):
        isFree = jsonGame['deal']['price']['amount'] == 0
        game = Game(jsonGame['id'], jsonGame['slug'], jsonGame['title'], jsonGame['type'], jsonGame['mature'], isFree, jsonGame['deal']['price']['amount'], jsonGame['deal']['cut'], jsonGame['deal']['url'], jsonGame['deal']['expiry'])
        return game
    
    def mapMultipleFromJson(json):
        gamesList = json['list']
        games = []
        for game in gamesList:
            games.append(GameMapper.map(game))
            
        return games