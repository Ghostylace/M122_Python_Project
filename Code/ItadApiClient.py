"""
Module for interacting with the IsThereAnyDeal API.

This module provides the ItadApiClient class for fetching free game deals
from the IsThereAnyDeal API.
"""

import requests
from GameMapper import GameMapper

class ItadApiClient:
    """
    A client for the IsThereAnyDeal API.
    
    Provides methods to fetch free game deals from the API with
    specific filtering parameters.
    """
    
    def __init__(self):
        """
        Initialize the ItadApiClient.
        """
        pass
        
    def fetchFreeGames(self, apiKey):
        """
        Fetch free games from the IsThereAnyDeal API.
        
        Queries the ITAD API for free games in Switzerland (country code CH)
        from Steam (shop ID 61), sorted by price.
        
        Args:
            apiKey (str): The API key for authenticating with the ITAD API.
            
        Returns:
            list: A list of Game objects representing free games.
        """
        httpResponse = requests.get(f"https://api.isthereanydeal.com/deals/v2?key={apiKey}&country=CH&shops=61&sort=price")
        games = GameMapper.mapMultipleFromJson(httpResponse.json())
        return games