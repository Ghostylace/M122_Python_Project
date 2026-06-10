"""
Unit tests for the ItadApiClient class.

Tests API client functionality for fetching free games.
"""

import unittest
from unittest.mock import patch, MagicMock
from ItadApiClient import ItadApiClient
from Game import Game


class TestItadApiClient(unittest.TestCase):
    """Test cases for the ItadApiClient class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.api_response_single = [
            {
                'id': '1',
                'slug': 'free-game',
                'title': 'Free Game',
                'type': 'game',
                'mature': False,
                'deal': {
                    'price': {'amount': 0},
                    'cut': 0,
                    'url': 'https://example.com/free',
                    'expiry': '2026-07-01T19:00:00+02:00'
                }
            }
        ]
        
        self.api_response_multiple = [
            {
                'id': '1',
                'slug': 'game1',
                'title': 'Game 1',
                'type': 'game',
                'mature': False,
                'deal': {
                    'price': {'amount': 0},
                    'cut': 0,
                    'url': 'https://example.com/1',
                    'expiry': '2026-07-01T00:00:00Z'
                }
            },
            {
                'id': '2',
                'slug': 'game2',
                'title': 'Game 2',
                'type': 'game',
                'mature': False,
                'deal': {
                    'price': {'amount': 0},
                    'cut': 0,
                    'url': 'https://example.com/2',
                    'expiry': '2026-07-15T00:00:00Z'
                }
            }
        ]
    
    def test_itad_api_client_initialization(self):
        """Test that ItadApiClient can be initialized."""
        client = ItadApiClient()
        self.assertIsNotNone(client)
    
    @patch('requests.get')
    def test_fetch_free_games_single_game(self, mock_get):
        """Test fetching a single free game from API."""
        mock_response = MagicMock()
        mock_response.json.return_value = self.api_response_single
        mock_get.return_value = mock_response
        
        client = ItadApiClient()
        games = client.fetchFreeGames("test_api_key")
        
        self.assertEqual(len(games), 1)
        self.assertIsInstance(games[0], Game)
        self.assertEqual(games[0].id, '1')
        self.assertEqual(games[0].title, 'Free Game')
        self.assertTrue(games[0].isFree)
    
    @patch('requests.get')
    def test_fetch_free_games_multiple_games(self, mock_get):
        """Test fetching multiple free games from API."""
        mock_response = MagicMock()
        mock_response.json.return_value = self.api_response_multiple
        mock_get.return_value = mock_response
        
        client = ItadApiClient()
        games = client.fetchFreeGames("test_api_key")
        
        self.assertEqual(len(games), 2)
        self.assertEqual(games[0].id, '1')
        self.assertEqual(games[1].id, '2')
    
    @patch('requests.get')
    def test_fetch_free_games_empty_response(self, mock_get):
        """Test handling empty API response."""
        mock_response = MagicMock()
        mock_response.json.return_value = []
        mock_get.return_value = mock_response
        
        client = ItadApiClient()
        games = client.fetchFreeGames("test_api_key")
        
        self.assertEqual(len(games), 0)
    
    @patch('requests.get')
    def test_fetch_free_games_api_url_format(self, mock_get):
        """Test that correct API URL is called."""
        mock_response = MagicMock()
        mock_response.json.return_value = []
        mock_get.return_value = mock_response
        
        client = ItadApiClient()
        api_key = "my_test_key"
        client.fetchFreeGames(api_key)
        
        # Verify the API was called with correct URL
        called_url = mock_get.call_args[0][0]
        self.assertIn("api.isthereanydeal.com", called_url)
        self.assertIn(api_key, called_url)
        self.assertIn("country=CH", called_url)
        self.assertIn("shops=61", called_url)
    
    @patch('requests.get')
    def test_fetch_free_games_returns_game_objects(self, mock_get):
        """Test that fetched games are proper Game objects."""
        mock_response = MagicMock()
        mock_response.json.return_value = self.api_response_single
        mock_get.return_value = mock_response
        
        client = ItadApiClient()
        games = client.fetchFreeGames("test_key")
        
        game = games[0]
        self.assertIsInstance(game, Game)
        self.assertTrue(hasattr(game, 'id'))
        self.assertTrue(hasattr(game, 'title'))
        self.assertTrue(hasattr(game, 'url'))
        self.assertTrue(hasattr(game, 'expiry'))
    
    @patch('requests.get')
    def test_fetch_free_games_with_different_api_keys(self, mock_get):
        """Test API calls with different API keys."""
        mock_response = MagicMock()
        mock_response.json.return_value = []
        mock_get.return_value = mock_response
        
        client = ItadApiClient()
        
        # Call with first key
        client.fetchFreeGames("key1")
        first_call_url = mock_get.call_args[0][0]
        
        # Call with second key
        client.fetchFreeGames("key2")
        second_call_url = mock_get.call_args[0][0]
        
        # Both calls should be made with different keys
        self.assertIn("key1", first_call_url)
        self.assertIn("key2", second_call_url)


if __name__ == '__main__':
    unittest.main()
