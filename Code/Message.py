"""
Module for creating formatted email messages about free games.

This module provides the Message class for generating email content
that lists free games with their details.
"""


class Message:
    """
    A class to create formatted messages about free games.
    
    Attributes:
        games (list): A list of Game objects to include in the message.
    """
    
    def __init__(self, games):
        """
        Initialize the Message with a list of games.
        
        Args:
            games (list): A list of Game objects to include in the message.
        """
        self.games = games
        
    def create_message(self):
        """
        Generate a formatted message with free games.
        
        Iterates through the games list and includes only free games in the
        message. Each game includes title, link, and expiration date. If no
        free games are found, appends "None" to the message.
        
        Returns:
            str: A formatted string containing the list of free games or "None"
                 if no free games are available.
        """
        message = "Current free games:"
        found_free_games = False
        for game in self.games:
            if game.isFree:
                found_free_games = True
                message += f"""
Title: {game.title}
Link: {game.url}
Expiration date: {game.expiry[:10]}
"""
        if not found_free_games:
            message += "\nNone"
        return message