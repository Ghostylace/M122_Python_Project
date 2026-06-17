"""
Unit tests for the MailService class.

Tests email configuration loading and sending functionality.
"""

import unittest
import json
from unittest.mock import patch, mock_open, MagicMock
from Code.MailService import MailService


class TestMailService(unittest.TestCase):
    """Test cases for the MailService class."""
    
    def setUp(self):
        """Set up test configuration."""
        self.valid_config = {
            "SMTPHost": "smtp.gmail.com",
            "SMTPPort": 587,
            "SMTPMail": "sender@gmail.com",
            "SMTPPassword": "app_password_123",
            "Email": "recipient@example.com"
        }
    
    @patch('builtins.open', new_callable=mock_open)
    def test_mail_service_initialization_valid_config(self, mock_file):
        """Test MailService initialization with valid config."""
        mock_file.return_value.read.return_value = json.dumps(self.valid_config)
        
        with patch('builtins.open', mock_open(read_data=json.dumps(self.valid_config))):
            service = MailService()
            
            self.assertEqual(service.smtp_host, "smtp.gmail.com")
            self.assertEqual(service.smtp_port, 587)
            self.assertEqual(service.smtp_mail, "sender@gmail.com")
            self.assertEqual(service.smtp_pass, "app_password_123")
            self.assertEqual(service.to_address, "recipient@example.com")
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('smtplib.SMTP')
    def test_send_mail_success(self, mock_smtp_class, mock_file):
        """Test sending email successfully."""
        mock_file.return_value.read.return_value = json.dumps(self.valid_config)
        
        # Setup mock SMTP
        mock_smtp_instance = MagicMock()
        mock_smtp_class.return_value.__enter__.return_value = mock_smtp_instance
        
        with patch('builtins.open', mock_open(read_data=json.dumps(self.valid_config))):
            service = MailService()
            service.send_mail("Test email body")
        
        # Verify SMTP operations were called
        mock_smtp_instance.starttls.assert_called_once()
        mock_smtp_instance.login.assert_called_once_with("sender@gmail.com", "app_password_123")
        mock_smtp_instance.send_message.assert_called_once()
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('smtplib.SMTP')
    def test_send_mail_uses_correct_credentials(self, mock_smtp_class, mock_file):
        """Test that send_mail uses correct credentials."""
        mock_file.return_value.read.return_value = json.dumps(self.valid_config)
        mock_smtp_instance = MagicMock()
        mock_smtp_class.return_value.__enter__.return_value = mock_smtp_instance
        
        with patch('builtins.open', mock_open(read_data=json.dumps(self.valid_config))):
            service = MailService()
            service.send_mail("Test body")
            
            # Verify login used correct credentials
            call_args = mock_smtp_instance.login.call_args
            self.assertEqual(call_args[0][0], "sender@gmail.com")
            self.assertEqual(call_args[0][1], "app_password_123")
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('smtplib.SMTP')
    def test_send_mail_message_attributes(self, mock_smtp_class, mock_file):
        """Test that email message has correct attributes."""
        mock_file.return_value.read.return_value = json.dumps(self.valid_config)
        mock_smtp_instance = MagicMock()
        mock_smtp_class.return_value.__enter__.return_value = mock_smtp_instance
        
        with patch('builtins.open', mock_open(read_data=json.dumps(self.valid_config))):
            service = MailService()
            service.send_mail("Test body content")
            
            # Verify send_message was called
            self.assertTrue(mock_smtp_instance.send_message.called)
            
            # Get the message object that was sent
            message = mock_smtp_instance.send_message.call_args[0][0]
            self.assertEqual(message["From"], "sender@gmail.com")
            self.assertEqual(message["To"], "recipient@example.com")
            self.assertEqual(message["Subject"], "Current free games on steam")
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('smtplib.SMTP')
    def test_send_mail_with_different_body(self, mock_smtp_class, mock_file):
        """Test sending email with different body content."""
        mock_file.return_value.read.return_value = json.dumps(self.valid_config)
        mock_smtp_instance = MagicMock()
        mock_smtp_class.return_value.__enter__.return_value = mock_smtp_instance
        
        test_bodies = [
            "Simple body",
            "Body with\nmultiple\nlines",
            "Special chars: @#$%^&*()"
        ]
        
        with patch('builtins.open', mock_open(read_data=json.dumps(self.valid_config))):
            service = MailService()
            
            for body in test_bodies:
                mock_smtp_instance.reset_mock()
                service.send_mail(body)
                self.assertTrue(mock_smtp_instance.send_message.called)


if __name__ == '__main__':
    unittest.main()
