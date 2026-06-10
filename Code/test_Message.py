"""
Unit tests for the Message class.

Tests message creation and formatting with various game scenarios.
"""

import unittest
from Message import Message
from Game import Game


class TestMessage(unittest.TestCase):
    """Test cases for the Message class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.free_game1 = Game(
            id="1",
            slug="free-game-1",
            title="Free Game 1",
            type="game",
            mature=False,
            isFree=True,
            price=0,
            cut=0,
            url="https://example.com/free1",
            expiry="2026-07-01T19:00:00+02:00"
        )
        self.free_game2 = Game(
            id="2",
            slug="free-game-2",
            title="Free Game 2",
            type="game",
            mature=False,
            isFree=True,
            price=0,
            cut=0,
            url="https://example.com/free2",
            expiry="2026-07-15T19:00:00+02:00"
        )
        self.paid_game = Game(
            id="3",
            slug="paid-game",
            title="Paid Game",
            type="game",
            mature=False,
            isFree=False,
            price=29.99,
            cut=0,
            url="https://example.com/paid",
            expiry="2026-07-25T19:00:00+02:00"
        )
    
    def test_message_with_single_free_game(self):
        """Test creating a message with a single free game."""
        message = Message([self.free_game1])
        msg_text = message.create_message()
        
        self.assertIn("Current free games:", msg_text)
        self.assertIn("Free Game 1", msg_text)
        self.assertIn("https://example.com/free1", msg_text)
        self.assertIn("2026-07-01", msg_text)
    
    def test_message_with_multiple_free_games(self):
        """Test creating a message with multiple free games."""
        message = Message([self.free_game1, self.free_game2])
        msg_text = message.create_message()
        
        self.assertIn("Current free games:", msg_text)
        self.assertIn("Free Game 1", msg_text)
        self.assertIn("Free Game 2", msg_text)
        self.assertIn("2026-07-01", msg_text)
        self.assertIn("2026-07-15", msg_text)
    
    def test_message_excludes_paid_games(self):
        """Test that paid games are not included in the message."""
        message = Message([self.free_game1, self.paid_game])
        msg_text = message.create_message()
        
        self.assertIn("Free Game 1", msg_text)
        self.assertNotIn("Paid Game", msg_text)
    
    def test_message_with_no_free_games(self):
        """Test creating a message when no free games exist."""
        message = Message([self.paid_game])
        msg_text = message.create_message()
        
        self.assertIn("Current free games:", msg_text)
        self.assertIn("None", msg_text)
        self.assertNotIn("Paid Game", msg_text)
    
    def test_message_with_empty_list(self):
        """Test creating a message with empty game list."""
        message = Message([])
        msg_text = message.create_message()
        
        self.assertIn("Current free games:", msg_text)
        self.assertIn("None", msg_text)
    
    def test_message_format_includes_title_field(self):
        """Test message format includes Title field."""
        message = Message([self.free_game1])
        msg_text = message.create_message()
        
        self.assertIn("Title:", msg_text)
    
    def test_message_format_includes_link_field(self):
        """Test message format includes Link field."""
        message = Message([self.free_game1])
        msg_text = message.create_message()
        
        self.assertIn("Link:", msg_text)
    
    def test_message_format_includes_expiration_field(self):
        """Test message format includes Expiration date field."""
        message = Message([self.free_game1])
        msg_text = message.create_message()
        
        self.assertIn("Expiration date:", msg_text)
    
    def test_message_date_formatting_date_only(self):
        """Test that expiration date is formatted as date only (YYYY-MM-DD)."""
        message = Message([self.free_game1])
        msg_text = message.create_message()
        
        # Should have date in YYYY-MM-DD format
        self.assertIn("2026-07-01", msg_text)
        # Should NOT have full timestamp
        self.assertNotIn("T19:00:00", msg_text)
        self.assertNotIn("+02:00", msg_text)
    
    def test_message_date_formatting_consistency(self):
        """Test that all dates are formatted consistently."""
        message = Message([self.free_game1, self.free_game2])
        msg_text = message.create_message()
        
        # Both should be in YYYY-MM-DD format
        self.assertIn("2026-07-01", msg_text)
        self.assertIn("2026-07-15", msg_text)
    
    def test_message_structure_multiline(self):
        """Test that message has proper multiline structure."""
        message = Message([self.free_game1])
        msg_text = message.create_message()
        
        lines = msg_text.split('\n')
        # Should have multiple lines with content
        self.assertGreater(len(lines), 3)
    
    def test_message_with_mixed_games_only_free_shown(self):
        """Test that mixed game list only shows free games."""
        games = [self.free_game1, self.paid_game, self.free_game2, self.paid_game]
        message = Message(games)
        msg_text = message.create_message()
        
        # Only free games should appear
        self.assertIn("Free Game 1", msg_text)
        self.assertIn("Free Game 2", msg_text)
        # Paid games should not appear
        for line in msg_text.split('\n'):
            if "Paid Game" in line:
                self.fail("Paid game should not appear in message")


if __name__ == '__main__':
    unittest.main()
