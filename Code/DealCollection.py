"""
Module for managing a collection of free game deals.

This module provides the DealCollection class for loading, managing,
and persisting a collection of free game deals from a JSON file.
"""

import json
import os
from GameMapper import GameMapper

class DealCollection:
    """
    A collection manager for free game deals.
    
    Manages loading, updating, and saving a collection of games from
    the local games.json file.
    
    Attributes:
        games (list): A list of Game objects representing all loaded games.
    """
    
    def __init__(self):
        """
        Initialize the DealCollection by loading games from file.
        
        Loads the games from games.json on instantiation.
        """
        self.games = self.loadGames()
        
    def loadGames(self):
        """
        Load games from the games.json file.
        
        Reads the games.json file and converts the JSON data into
        a list of Game objects. If the file is missing or corrupted,
        it will be deleted and recreated with an empty list, then
        the function will be called again to read the newly created file.
        
        Returns:
            list: A list of Game objects loaded from games.json.
        """
        try:
            file = open("games.json")
            data = json.load(file)
            file.close()
            games = GameMapper.mapMultipleFromJson(data)
            return games
        except (FileNotFoundError, json.JSONDecodeError):
            try:
                os.remove("games.json")
            except FileNotFoundError:
                pass
            with open("games.json", "w") as file:
                json.dump([], file, indent=2)
            return self.loadGames()
    
    def loadNewGames(self, new_games):
        """
        Add new free games to the collection and save.
        
        Checks for duplicate games (by ID) and only adds new free games
        to the collection. Updates the games.json file after adding new games.
        
        Args:
            new_games (list): A list of Game objects to potentially add.
            
        Returns:
            list: A list of newly added Game objects.
        """
        new_games_to_return = []
        existing_ids = {game.id for game in self.games}

        for new_game in new_games:
            if new_game.id in existing_ids:
                continue

            if new_game.isFree:
                self.games.append(new_game)
                new_games_to_return.append(new_game)
                existing_ids.add(new_game.id)

        self.saveGames()
        return new_games_to_return
    
    def saveGames(self):
        """
        Save all free games in the collection to games.json.
        
        Filters the collection to include only free games and writes them
        to games.json in a formatted JSON structure. If the file cannot be
        written, it will be deleted and recreated, then the function will
        be called again to save the data to the newly created file.
        """
        try:
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
            file.close()
            print("Successfully saved games")
        except (IOError, json.JSONDecodeError):
            try:
                os.remove("games.json")
            except FileNotFoundError:
                pass
            with open("games.json", "w") as file:
                json.dump([], file, indent=2)
            self.saveGames()