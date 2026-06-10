"""
Module for mapping JSON data to Game objects.

This module provides the GameMapper class for converting JSON game data
from API responses into Game objects.
"""

from Game import Game

class GameMapper:
    """
    A mapper class for converting JSON game data to Game objects.
    """
    
    def map(jsonGame):
        """
        Map a single JSON game object to a Game instance.
        
        Handles two different JSON structures - one from the ITAD API and one
        from the games.json file. Attempts to parse the API structure first,
        then falls back to the local file structure on KeyError.
        
        Args:
            jsonGame (dict): A dictionary containing game data from JSON.
            
        Returns:
            Game: A Game object created from the JSON data.
        """
        try:
            isFree = jsonGame['deal']['price']['amount'] == 0
            game = Game(jsonGame['id'], jsonGame['slug'], jsonGame['title'], jsonGame['type'], jsonGame['mature'], isFree, jsonGame['deal']['price']['amount'], jsonGame['deal']['cut'], jsonGame['deal']['url'], jsonGame['deal']['expiry'])
        except KeyError:
            game = Game(jsonGame['id'], jsonGame['slug'], jsonGame['title'], jsonGame['type'], jsonGame['mature'], jsonGame['isFree'], jsonGame['price'], jsonGame['cut'], jsonGame['url'], jsonGame['expiry'])
        return game
    
    def mapMultipleFromJson(json):
        """
        Map multiple JSON game objects to Game instances.
        
        Converts a JSON array or a JSON object with a 'list' key into
        a list of Game objects.
        
        Args:
            json: A JSON object or list containing game data.
            
        Returns:
            list: A list of Game objects created from the JSON data.
        """
        try:
            gamesList = json['list']
        except:
            gamesList = json
        games = []
        for game in gamesList:
            games.append(GameMapper.map(game))
            
        return games