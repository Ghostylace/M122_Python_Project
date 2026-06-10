"""
Module for representing a game object.

This module defines the Game class which represents a video game with
its associated properties and metadata.
"""

class Game:
    """
    A class to represent a video game.
    
    Attributes:
        id (str): Unique identifier for the game.
        slug (str): URL-friendly version of the game title.
        title (str): The game's display title.
        type (str): Type of game (e.g., 'game', 'dlc').
        mature (bool): Whether the game is marked as mature.
        isFree (bool): Whether the game is available for free.
        price (float): The price of the game.
        cut (float): The discount percentage.
        url (str): Link to the game's store page.
        expiry (str): The expiration date for the free offer (ISO format).
    """
    
    def __init__(self, id, slug, title, type, mature, isFree, price, cut, url, expiry):
        """
        Initialize a Game object.
        
        Args:
            id (str): Unique identifier for the game.
            slug (str): URL-friendly version of the game title.
            title (str): The game's display title.
            type (str): Type of game (e.g., 'game', 'dlc').
            mature (bool): Whether the game is marked as mature.
            isFree (bool): Whether the game is available for free.
            price (float): The price of the game.
            cut (float): The discount percentage.
            url (str): Link to the game's store page.
            expiry (str): The expiration date for the free offer (ISO format).
        """
        self.id = id
        self.slug = slug
        self.title = title
        self.type = type
        self.mature = mature
        self.isFree = isFree
        self.price = price
        self.cut = cut
        self.url = url
        self.expiry = expiry

    def __eq__(self, other):
        """
        Check equality between two Game objects based on ID.
        
        Args:
            other: Another object to compare with.
            
        Returns:
            bool: True if both are Game objects with the same ID, False otherwise.
        """
        return isinstance(other, Game) and self.id == other.id

    def __hash__(self):
        """
        Generate a hash value for the Game object based on its ID.
        
        Returns:
            int: Hash value of the game's ID.
        """
        return hash(self.id)
