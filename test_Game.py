"""
Unit tests for the Game class.

Tests game creation, equality, hashing, and set operations.
"""

import unittest
from Code.Game import Game


class TestGame(unittest.TestCase):
    """Test cases for the Game class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.game1 = Game(
            id="1",
            slug="game-one",
            title="Game One",
            type="game",
            mature=False,
            isFree=True,
            price=0,
            cut=0,
            url="https://example.com/game1",
            expiry="2026-07-01T19:00:00+02:00"
        )
        self.game2 = Game(
            id="2",
            slug="game-two",
            title="Game Two",
            type="game",
            mature=False,
            isFree=True,
            price=0,
            cut=0,
            url="https://example.com/game2",
            expiry="2026-07-15T19:00:00+02:00"
        )
    
    def test_game_creation(self):
        """Test that a game can be created with all attributes."""
        self.assertEqual(self.game1.id, "1")
        self.assertEqual(self.game1.title, "Game One")
        self.assertEqual(self.game1.slug, "game-one")
        self.assertEqual(self.game1.type, "game")
        self.assertFalse(self.game1.mature)
        self.assertTrue(self.game1.isFree)
        self.assertEqual(self.game1.price, 0)
        self.assertEqual(self.game1.cut, 0)
        self.assertEqual(self.game1.url, "https://example.com/game1")
        self.assertEqual(self.game1.expiry, "2026-07-01T19:00:00+02:00")
    
    def test_game_equality_same_id(self):
        """Test that games are equal based on ID."""
        game_same_id = Game(
            id="1",
            slug="different-slug",
            title="Different Title",
            type="dlc",
            mature=True,
            isFree=False,
            price=10,
            cut=50,
            url="https://different.com",
            expiry="2026-08-01T00:00:00Z"
        )
        self.assertEqual(self.game1, game_same_id)
    
    def test_game_inequality_different_id(self):
        """Test that games with different IDs are not equal."""
        self.assertNotEqual(self.game1, self.game2)
    
    def test_game_inequality_with_non_game_object(self):
        """Test inequality with non-Game objects."""
        self.assertNotEqual(self.game1, "not a game")
        self.assertNotEqual(self.game1, 123)
        self.assertNotEqual(self.game1, None)
    
    def test_game_hash_same_id(self):
        """Test that game hash is based on ID."""
        game_same_id = Game(
            id="1",
            slug="other",
            title="Other",
            type="game",
            mature=False,
            isFree=True,
            price=0,
            cut=0,
            url="https://other.com",
            expiry="2026-07-01T00:00:00Z"
        )
        self.assertEqual(hash(self.game1), hash(game_same_id))
    
    def test_game_hash_different_id(self):
        """Test that games with different IDs have different hashes."""
        self.assertNotEqual(hash(self.game1), hash(self.game2))
    
    def test_game_in_set_deduplication(self):
        """Test that games can be used in sets (testing hash and equality)."""
        game_set = {self.game1, self.game2}
        self.assertEqual(len(game_set), 2)
        
        # Add a game with same ID as game1
        game_duplicate = Game(
            id="1",
            slug="dup",
            title="Duplicate",
            type="game",
            mature=False,
            isFree=True,
            price=0,
            cut=0,
            url="https://dup.com",
            expiry="2026-07-01T00:00:00Z"
        )
        game_set.add(game_duplicate)
        self.assertEqual(len(game_set), 2)  # Still 2 because ID is same
    
    def test_game_in_dictionary(self):
        """Test that games can be used as dictionary keys."""
        game_dict = {self.game1: "value1", self.game2: "value2"}
        self.assertEqual(len(game_dict), 2)
        
        # Access with different object but same ID
        game_same_id = Game(
            id="1",
            slug="key",
            title="Key",
            type="game",
            mature=False,
            isFree=True,
            price=0,
            cut=0,
            url="https://key.com",
            expiry="2026-07-01T00:00:00Z"
        )
        self.assertEqual(game_dict[game_same_id], "value1")


if __name__ == '__main__':
    unittest.main()
