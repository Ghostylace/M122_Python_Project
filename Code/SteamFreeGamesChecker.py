"""
Module for checking and reporting new free games on Steam.

This module provides the SteamFreeGamesChecker class which orchestrates
the entire workflow of fetching free games, storing them, and sending
notification emails.
"""

from ItadApiClient import ItadApiClient as Client
from DealCollection import DealCollection
from ConfigReader import ConfigReader as reader
from Message import Message
from MailService import MailService

class SteamFreeGamesChecker:
    """
    A checker for fetching and notifying about new free games on Steam.
    
    Orchestrates the entire workflow: fetching free games from the API,
    checking for new games, storing them locally, and sending email
    notifications about newly found free games.
    """
    
    def fetchGames(self):
        """
        Fetch new free games and send notification email.
        
        This method performs the following steps:
        1. Fetches free games from the ITAD API
        2. Loads configuration and existing games
        3. Identifies and stores new free games
        4. Prints new game titles to console
        5. Creates a formatted message with the new games
        6. Sends an email notification with the game list
        """
        client = Client()
        r = reader()
        d = DealCollection()
        config = r.readConfigFile()
        games = client.fetchFreeGames(config["APIKey"])
        games = d.loadNewGames(games)
        for game in games:
            if game.isFree:
                print(game.title)
        m = Message(games)
        srv = MailService()
        msg = m.createMessage()
        srv.sendMail(msg)
