"""
Unit tests for the GameMapper class.

Tests mapping JSON data to Game objects from different sources.
"""

import unittest
from Code.GameMapper import GameMapper
from Code.Game import Game


class TestGameMapper(unittest.TestCase):
    """Test cases for the GameMapper class."""
    
    def test_map_from_api_structure(self):
        """Test mapping from ITAD API JSON structure."""
        json_game = {
            'id': '123',
            'slug': 'test-game',
            'title': 'Test Game',
            'type': 'game',
            'mature': False,
            'deal': {
                'price': {'amount': 0},
                'cut': 0,
                'url': 'https://example.com/test',
                'expiry': '2026-07-01T00:00:00Z'
            }
        }
        game = GameMapper.map(json_game)
        
        self.assertIsInstance(game, Game)
        self.assertEqual(game.id, '123')
        self.assertEqual(game.slug, 'test-game')
        self.assertEqual(game.title, 'Test Game')
        self.assertEqual(game.type, 'game')
        self.assertFalse(game.mature)
        self.assertTrue(game.isFree)
        self.assertEqual(game.price, 0)
        self.assertEqual(game.cut, 0)
        self.assertEqual(game.url, 'https://example.com/test')
        self.assertEqual(game.expiry, '2026-07-01T00:00:00Z')
    
    def test_map_from_api_structure_paid_game(self):
        """Test mapping a paid game from ITAD API structure."""
        json_game = {
            'id': '456',
            'slug': 'paid-game',
            'title': 'Paid Game',
            'type': 'game',
            'mature': True,
            'deal': {
                'price': {'amount': 29.99},
                'cut': 50,
                'url': 'https://example.com/paid',
                'expiry': '2026-08-01T00:00:00Z'
            }
        }
        game = GameMapper.map(json_game)
        
        self.assertEqual(game.id, '456')
        self.assertFalse(game.isFree)
        self.assertEqual(game.price, 29.99)
        self.assertEqual(game.cut, 50)
        self.assertTrue(game.mature)
    
    def test_map_from_local_file_structure(self):
        """Test mapping from local games.json structure."""
        json_game = {
            'id': '789',
            'slug': 'local-game',
            'title': 'Local Game',
            'type': 'game',
            'mature': False,
            'isFree': True,
            'price': 0,
            'cut': 0,
            'url': 'https://example.com/local',
            'expiry': '2026-07-15T00:00:00Z'
        }
        game = GameMapper.map(json_game)
        
        self.assertIsInstance(game, Game)
        self.assertEqual(game.id, '789')
        self.assertEqual(game.title, 'Local Game')
        self.assertTrue(game.isFree)
        self.assertEqual(game.price, 0)
    
    def test_map_from_local_structure_paid(self):
        """Test mapping a paid game from local structure."""
        json_game = {
            'id': '999',
            'slug': 'local-paid',
            'title': 'Local Paid Game',
            'type': 'dlc',
            'mature': True,
            'isFree': False,
            'price': 14.99,
            'cut': 25,
            'url': 'https://example.com/local-paid',
            'expiry': '2026-09-01T00:00:00Z'
        }
        game = GameMapper.map(json_game)
        
        self.assertFalse(game.isFree)
        self.assertEqual(game.price, 14.99)
        self.assertEqual(game.type, 'dlc')
    
    def test_map_multiple_from_list(self):
        """Test mapping multiple games from a list."""
        json_data = [
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
        ]
        games = GameMapper.mapMultipleFromJson(json_data)
        
        self.assertEqual(len(games), 2)
        self.assertIsInstance(games[0], Game)
        self.assertIsInstance(games[1], Game)
        self.assertEqual(games[0].id, '1')
        self.assertEqual(games[1].id, '2')
    
    def test_map_multiple_from_dict_with_list(self):
        """Test mapping multiple games from dict with 'list' key."""
        json_data = {
            'list': [
                {
                    'id': '3',
                    'slug': 'game3',
                    'title': 'Game 3',
                    'type': 'game',
                    'mature': False,
                    'isFree': True,
                    'price': 0,
                    'cut': 0,
                    'url': 'https://example.com/3',
                    'expiry': '2026-08-01T00:00:00Z'
                },
                {
                    'id': '4',
                    'slug': 'game4',
                    'title': 'Game 4',
                    'type': 'game',
                    'mature': False,
                    'isFree': True,
                    'price': 0,
                    'cut': 0,
                    'url': 'https://example.com/4',
                    'expiry': '2026-08-15T00:00:00Z'
                }
            ]
        }
        games = GameMapper.mapMultipleFromJson(json_data)
        
        self.assertEqual(len(games), 2)
        self.assertEqual(games[0].id, '3')
        self.assertEqual(games[1].id, '4')
    
    def test_map_multiple_empty_list(self):
        """Test mapping from empty list."""
        json_data = []
        games = GameMapper.mapMultipleFromJson(json_data)
        
        self.assertEqual(len(games), 0)
    
    def test_map_multiple_empty_dict_list(self):
        """Test mapping from dict with empty list."""
        json_data = {'list': []}
        games = GameMapper.mapMultipleFromJson(json_data)
        
        self.assertEqual(len(games), 0)


if __name__ == '__main__':
    unittest.main()
