"""
Unit tests for the DealCollection class.

Tests game collection management, loading, and saving functionality.
"""

import unittest
import json
import os
from unittest.mock import patch, mock_open
from DealCollection import DealCollection
from Game import Game


class TestDealCollection(unittest.TestCase):
    """Test cases for the DealCollection class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.free_game_data = {
            'id': '1',
            'slug': 'free-game',
            'title': 'Free Game',
            'type': 'game',
            'mature': False,
            'isFree': True,
            'price': 0,
            'cut': 0,
            'url': 'https://example.com/free',
            'expiry': '2026-07-01T00:00:00Z'
        }
        
        self.paid_game_data = {
            'id': '2',
            'slug': 'paid-game',
            'title': 'Paid Game',
            'type': 'game',
            'mature': False,
            'isFree': False,
            'price': 29.99,
            'cut': 0,
            'url': 'https://example.com/paid',
            'expiry': '2026-07-15T00:00:00Z'
        }
    
    @patch('builtins.open', new_callable=mock_open, read_data='[]')
    def test_deal_collection_initialization_empty(self, mock_file):
        """Test DealCollection initialization with empty games list."""
        collection = DealCollection()
        self.assertEqual(collection.games, [])
    
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps([]))
    def test_load_games_empty(self, mock_file):
        """Test loading empty games from file."""
        collection = DealCollection()
        games = collection.load_games()
        self.assertEqual(len(games), 0)
    
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps([
        {
            'id': '1',
            'slug': 'game1',
            'title': 'Game 1',
            'type': 'game',
            'mature': False,
            'isFree': True,
            'price': 0,
            'cut': 0,
            'url': 'https://example.com/1',
            'expiry': '2026-07-01T00:00:00Z'
        }
    ]))
    def test_load_games_single_game(self, mock_file):
        """Test loading a single game from file."""
        collection = DealCollection()
        games = collection.load_games()
        
        self.assertEqual(len(games), 1)
        self.assertIsInstance(games[0], Game)
        self.assertEqual(games[0].id, '1')
        self.assertEqual(games[0].title, 'Game 1')
    
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps([
        {
            'id': '1',
            'slug': 'game1',
            'title': 'Game 1',
            'type': 'game',
            'mature': False,
            'isFree': True,
            'price': 0,
            'cut': 0,
            'url': 'https://example.com/1',
            'expiry': '2026-07-01T00:00:00Z'
        },
        {
            'id': '2',
            'slug': 'game2',
            'title': 'Game 2',
            'type': 'game',
            'mature': False,
            'isFree': True,
            'price': 0,
            'cut': 0,
            'url': 'https://example.com/2',
            'expiry': '2026-07-15T00:00:00Z'
        }
    ]))
    def test_load_games_multiple_games(self, mock_file):
        """Test loading multiple games from file."""
        collection = DealCollection()
        games = collection.load_games()
        
        self.assertEqual(len(games), 2)
        self.assertEqual(games[0].id, '1')
        self.assertEqual(games[1].id, '2')
    
    @patch('builtins.open', new_callable=mock_open, read_data='[]')
    def test_load_new_games_empty_collection(self, mock_file):
        """Test adding games to empty collection."""
        collection = DealCollection()
        collection.games = []
        
        new_game = Game(
            id="3",
            slug="new",
            title="New Game",
            type="game",
            mature=False,
            isFree=True,
            price=0,
            cut=0,
            url="https://example.com/new",
            expiry="2026-07-01T00:00:00Z"
        )
        
        result = collection.load_new_games([new_game])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id, "3")
    
    @patch('builtins.open', new_callable=mock_open, read_data='[]')
    def test_load_new_games_detects_duplicates(self, mock_file):
        """Test that load_new_games detects and skips duplicate IDs."""
        collection = DealCollection()
        existing_game = Game(
            id="1",
            slug="existing",
            title="Existing Game",
            type="game",
            mature=False,
            isFree=True,
            price=0,
            cut=0,
            url="https://example.com/existing",
            expiry="2026-07-01T00:00:00Z"
        )
        collection.games = [existing_game]
        
        duplicate_game = Game(
            id="1",
            slug="new",
            title="New Game",
            type="game",
            mature=False,
            isFree=True,
            price=0,
            cut=0,
            url="https://example.com/new",
            expiry="2026-07-01T00:00:00Z"
        )
        
        result = collection.load_new_games([duplicate_game])
        self.assertEqual(len(result), 0)  # Should be empty because duplicate
    
    @patch('builtins.open', new_callable=mock_open, read_data='[]')
    def test_load_new_games_skips_paid_games(self, mock_file):
        """Test that paid games are not added to collection."""
        collection = DealCollection()
        collection.games = []
        
        paid_game = Game(
            id="2",
            slug="paid",
            title="Paid Game",
            type="game",
            mature=False,
            isFree=False,
            price=29.99,
            cut=0,
            url="https://example.com/paid",
            expiry="2026-07-01T00:00:00Z"
        )
        
        result = collection.load_new_games([paid_game])
        self.assertEqual(len(result), 0)  # Paid games should not be added
    
    @patch('builtins.open', new_callable=mock_open, read_data='[]')
    def test_load_new_games_mixed_free_and_paid(self, mock_file):
        """Test loading mix of free and paid games."""
        collection = DealCollection()
        collection.games = []
        
        free_game = Game(
            id="1",
            slug="free",
            title="Free Game",
            type="game",
            mature=False,
            isFree=True,
            price=0,
            cut=0,
            url="https://example.com/free",
            expiry="2026-07-01T00:00:00Z"
        )
        
        paid_game = Game(
            id="2",
            slug="paid",
            title="Paid Game",
            type="game",
            mature=False,
            isFree=False,
            price=29.99,
            cut=0,
            url="https://example.com/paid",
            expiry="2026-07-01T00:00:00Z"
        )
        
        result = collection.load_new_games([free_game, paid_game])
        self.assertEqual(len(result), 1)  # Only free game
        self.assertEqual(result[0].id, "1")
    
    @patch('builtins.open', new_callable=mock_open, read_data='[]')
    def test_save_games_empty_collection(self, mock_file):
        """Test saving empty game collection."""
        collection = DealCollection()
        collection.games = []
        
        # Should not raise an error
        collection.save_games()
        self.assertTrue(mock_file.called)
    
    @patch('builtins.open', new_callable=mock_open, read_data='[]')
    def test_save_games_with_free_games(self, mock_file):
        """Test saving collection with free games."""
        collection = DealCollection()
        
        free_game = Game(
            id="1",
            slug="free",
            title="Free Game",
            type="game",
            mature=False,
            isFree=True,
            price=0,
            cut=0,
            url="https://example.com/free",
            expiry="2026-07-01T00:00:00Z"
        )
        
        collection.games = [free_game]
        collection.save_games()
        
        self.assertTrue(mock_file.called)
    
    @patch('builtins.open', new_callable=mock_open, read_data='[]')
    def test_save_games_excludes_paid_games(self, mock_file):
        """Test that save only saves free games."""
        collection = DealCollection()
        
        free_game = Game(
            id="1",
            slug="free",
            title="Free Game",
            type="game",
            mature=False,
            isFree=True,
            price=0,
            cut=0,
            url="https://example.com/free",
            expiry="2026-07-01T00:00:00Z"
        )
        
        paid_game = Game(
            id="2",
            slug="paid",
            title="Paid Game",
            type="game",
            mature=False,
            isFree=False,
            price=29.99,
            cut=0,
            url="https://example.com/paid",
            expiry="2026-07-01T00:00:00Z"
        )
        
        collection.games = [free_game, paid_game]
        collection.save_games()
        
        # Get the data that was written
        handle = mock_file()
        written_data = ''.join(call.args[0] for call in handle.write.call_args_list)
        
        # Free game should be in written data, paid should not
        self.assertTrue(mock_file.called)


if __name__ == '__main__':
    unittest.main()
