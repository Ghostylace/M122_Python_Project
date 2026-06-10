"""
Unit tests for the ConfigReader class.

Tests reading and error handling for configuration files.
"""

import unittest
import json
import os
import tempfile
from unittest.mock import patch, mock_open
from ConfigReader import ConfigReader


class TestConfigReader(unittest.TestCase):
    """Test cases for the ConfigReader class."""
    
    @patch('builtins.open', new_callable=mock_open, read_data='{"SMTPHost": "smtp.gmail.com", "APIKey": "test_key"}')
    def test_read_valid_config(self, mock_file):
        """Test reading a valid config file."""
        reader = ConfigReader()
        config = reader.read_config_file()
        
        self.assertIsInstance(config, dict)
        self.assertEqual(config["SMTPHost"], "smtp.gmail.com")
        self.assertEqual(config["APIKey"], "test_key")
    
    @patch('builtins.open', new_callable=mock_open, read_data='{}')
    def test_read_empty_config(self, mock_file):
        """Test reading an empty config file."""
        reader = ConfigReader()
        config = reader.read_config_file()
        
        self.assertIsInstance(config, dict)
        self.assertEqual(len(config), 0)
    
    @patch('os.remove')
    @patch('builtins.open', side_effect=FileNotFoundError())
    def test_read_missing_config_creates_empty(self, mock_file, mock_remove):
        """Test that missing config file triggers recreation."""
        reader = ConfigReader()
        # Mock the second open call to return empty dict
        with patch('builtins.open', mock_open(read_data='{}')):
            config = reader.read_config_file()
        
        self.assertEqual(config, {})
    
    @patch('os.remove')
    @patch('builtins.open', side_effect=json.JSONDecodeError("msg", "doc", 0))
    def test_read_corrupted_config_recreates(self, mock_file, mock_remove):
        """Test that corrupted config file triggers recreation."""
        reader = ConfigReader()
        with patch('builtins.open', mock_open(read_data='{}')):
            config = reader.read_config_file()
        
        self.assertEqual(config, {})
    
    @patch('builtins.open', new_callable=mock_open, read_data='{"key": "value", "nested": {"inner": "data"}}')
    def test_read_nested_config(self, mock_file):
        """Test reading config with nested structure."""
        reader = ConfigReader()
        config = reader.read_config_file()
        
        self.assertEqual(config["key"], "value")
        self.assertIn("nested", config)
        self.assertEqual(config["nested"]["inner"], "data")
    
    def test_read_config_with_temp_file(self):
        """Test reading actual config file with temporary file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            test_config = {"test": "value", "number": 42}
            json.dump(test_config, f)
            temp_path = f.name
        
        try:
            # Patch open to use our temp file
            with patch('builtins.open', mock_open(read_data=json.dumps(test_config))):
                reader = ConfigReader()
                config = reader.read_config_file()
                self.assertEqual(config["test"], "value")
                self.assertEqual(config["number"], 42)
        finally:
            os.unlink(temp_path)


if __name__ == '__main__':
    unittest.main()
