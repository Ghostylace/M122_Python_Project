"""
Main entry point for the Steam Free Games Checker application.

This script creates an instance of SteamFreeGamesChecker and triggers
the workflow to fetch new free games and send notifications.
"""

from SteamFreeGamesChecker import SteamFreeGamesChecker

# Initialize the Steam Free Games Checker and start fetching games
steamChecker = SteamFreeGamesChecker()
steamChecker.fetchGames()