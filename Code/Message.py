class Message:
    def __init__(self, games):
        self.games = games
        
    def create_message(self):
        message = "Current free games:"
        for game in self.games:
            if game.isFree:
                message += f"""
{game.title}
{game.url}
{game.expiry}"""
        return message