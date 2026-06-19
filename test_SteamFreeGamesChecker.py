"""
Unit tests for the SteamFreeGamesChecker class.

Tests orchestration of the entire game checking workflow.
"""

import unittest
from unittest.mock import patch, MagicMock, call
from Code.SteamFreeGamesChecker import SteamFreeGamesChecker
from Code.Game import Game


class TestSteamFreeGamesChecker(unittest.TestCase):
    """Test cases for the SteamFreeGamesChecker class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sample_game = Game(
            id="1",
            slug="sample-game",
            title="Sample Game",
            type="game",
            mature=False,
            isFree=True,
            price=0,
            cut=0,
            url="https://example.com/sample",
            expiry="2026-07-01T00:00:00Z"
        )
    
    def test_steam_checker_initialization(self):
        """Test that SteamFreeGamesChecker can be initialized."""
        checker = SteamFreeGamesChecker()
        self.assertIsNotNone(checker)
    
    @patch('MailService.MailService.sendMail')
    @patch('DealCollection.DealCollection.loadNewGames')
    @patch('DealCollection.DealCollection.load_games')
    @patch('ItadApiClient.ItadApiClient.fetchFreeGames')
    @patch('ConfigReader.ConfigReader.readConfigFile')
    def test_fetch_games_calls_all_components(
        self,
        mock_config,
        mock_api,
        mock_load_games,
        mock_load_new,
        mock_send
    ):
        """Test that fetchGames calls all required components."""
        # Setup mocks
        mock_config.return_value = {"APIKey": "test_key"}
        mock_api.return_value = [self.sample_game]
        mock_load_games.return_value = []
        mock_load_new.return_value = [self.sample_game]
        
        checker = SteamFreeGamesChecker()
        
        with patch('builtins.print'):
            checker.fetchGames()
        
        # Verify all components were called
        mock_config.assert_called_once()
        mock_api.assert_called_once_with("test_key")
        mock_load_new.assert_called_once()
        mock_send.assert_called_once()
    
    @patch('MailService.MailService.sendMail')
    @patch('DealCollection.DealCollection.loadNewGames')
    @patch('DealCollection.DealCollection.load_games')
    @patch('ItadApiClient.ItadApiClient.fetchFreeGames')
    @patch('ConfigReader.ConfigReader.readConfigFile')
    def test_fetch_games_with_no_new_games(
        self,
        mock_config,
        mock_api,
        mock_load_games,
        mock_load_new,
        mock_send
    ):
        """Test fetchGames when no new free games are found."""
        mock_config.return_value = {"APIKey": "test_key"}
        mock_api.return_value = []
        mock_load_games.return_value = []
        mock_load_new.return_value = []
        
        checker = SteamFreeGamesChecker()
        
        with patch('builtins.print'):
            checker.fetchGames()
        
        # Should still send email (with "None" message)
        mock_send.assert_called_once()
    
    @patch('MailService.MailService.sendMail')
    @patch('DealCollection.DealCollection.loadNewGames')
    @patch('DealCollection.DealCollection.load_games')
    @patch('ItadApiClient.ItadApiClient.fetchFreeGames')
    @patch('ConfigReader.ConfigReader.readConfigFile')
    def test_fetch_games_prints_new_game_titles(
        self,
        mock_config,
        mock_api,
        mock_load_games,
        mock_load_new,
        mock_send
    ):
        """Test that fetchGames prints new game titles."""
        game1 = Game(
            id="1",
            slug="game1",
            title="Game 1",
            type="game",
            mature=False,
            isFree=True,
            price=0,
            cut=0,
            url="https://example.com/1",
            expiry="2026-07-01T00:00:00Z"
        )
        game2 = Game(
            id="2",
            slug="game2",
            title="Game 2",
            type="game",
            mature=False,
            isFree=True,
            price=0,
            cut=0,
            url="https://example.com/2",
            expiry="2026-07-15T00:00:00Z"
        )
        
        mock_config.return_value = {"APIKey": "test_key"}
        mock_api.return_value = [game1, game2]
        mock_load_games.return_value = []
        mock_load_new.return_value = [game1, game2]
        
        checker = SteamFreeGamesChecker()
        
        with patch('builtins.print') as mock_print:
            checker.fetchGames()
        
        # Verify print was called for each game
        calls = [c for c in mock_print.call_args_list if 'Game' in str(c)]
        self.assertGreaterEqual(len(calls), 2)
    
    @patch('MailService.MailService.sendMail')
    @patch('DealCollection.DealCollection.loadNewGames')
    @patch('DealCollection.DealCollection.load_games')
    @patch('ItadApiClient.ItadApiClient.fetchFreeGames')
    @patch('ConfigReader.ConfigReader.readConfigFile')
    def test_fetch_games_with_api_key_from_config(
        self,
        mock_config,
        mock_api,
        mock_load_games,
        mock_load_new,
        mock_send
    ):
        """Test that API key from config is used correctly."""
        mock_config.return_value = {"APIKey": "my_secret_key"}
        mock_api.return_value = []
        mock_load_games.return_value = []
        mock_load_new.return_value = []
        
        checker = SteamFreeGamesChecker()
        
        with patch('builtins.print'):
            checker.fetchGames()
        
        # Verify API was called with correct key
        mock_api.assert_called_once_with("my_secret_key")
    
    @patch('MailService.MailService.sendMail')
    @patch('Message.Message.createMessage')
    @patch('DealCollection.DealCollection.loadNewGames')
    @patch('DealCollection.DealCollection.load_games')
    @patch('ItadApiClient.ItadApiClient.fetchFreeGames')
    @patch('ConfigReader.ConfigReader.readConfigFile')
    def test_fetch_games_email_contains_message(
        self,
        mock_config,
        mock_api,
        mock_load_games,
        mock_load_new,
        mock_message,
        mock_send
    ):
        """Test that email is sent with message content."""
        mock_config.return_value = {"APIKey": "test_key"}
        mock_api.return_value = [self.sample_game]
        mock_load_games.return_value = []
        mock_load_new.return_value = [self.sample_game]
        mock_message.return_value = "Test message content"
        
        checker = SteamFreeGamesChecker()
        
        with patch('builtins.print'):
            checker.fetchGames()
        
        # Verify message was created and sent
        mock_message.assert_called_once()
        mock_send.assert_called_once_with("Test message content")


if __name__ == '__main__':
    unittest.main()
