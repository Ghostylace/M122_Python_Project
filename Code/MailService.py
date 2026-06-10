"""
Module for sending emails via SMTP.

This module provides the MailService class for composing and sending
emails using Gmail's SMTP server with credentials from the configuration.
"""

import smtplib
import json
import os
from email.message import EmailMessage

class MailService:
    """
    A service for sending emails via SMTP.
    
    Attributes:
        smtp_host (str): The SMTP server hostname.
        smtp_port (int): The SMTP server port.
        smtp_mail (str): The sender's email address.
        smtp_pass (str): The password or app password for authentication.
        to_address (str): The recipient's email address.
    """
    
    def __init__(self):
        """
        Initialize the MailService by loading SMTP configuration.
        
        Reads the SMTP configuration from config.json and sets up the
        connection parameters and email addresses. If the file is missing
        or corrupted, it will be deleted and recreated, then the
        configuration will be loaded again.
        """
        self._load_config()
    
    def _load_config(self):
        """
        Load SMTP configuration from config.json.
        
        Private helper method that loads configuration and handles file
        recreation if needed. Calls itself recursively after file recreation.
        """
        try:
            file = open("config.json")
            config = json.load(file)
            file.close()
            self.smtp_host = config["SMTPHost"]
            self.smtp_port = config["SMTPPort"]
            self.smtp_mail = config["SMTPMail"]
            self.smtp_pass = config["SMTPPassword"]
            self.to_address = config["Email"]
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            try:
                os.remove("config.json")
            except FileNotFoundError:
                pass
            with open("config.json", "w") as file:
                json.dump({}, file, indent=2)
            self._load_config()

    def send_mail(self, body):
        """
        Compose and send an email.
        
        Connects to the SMTP server, authenticates, and sends an email
        with the provided body content. The email subject is fixed as
        "Current free games on steam".
        
        Args:
            body (str): The body/content of the email message.
        """
        message = EmailMessage()
        message["From"] = self.smtp_mail
        message["To"] = self.to_address
        message["Subject"] = "Current free games on steam"
        message.set_content(body)

        with smtplib.SMTP(self.smtp_host, self.smtp_port) as smtp:
            smtp.starttls()
            smtp.login(self.smtp_mail, self.smtp_pass)
            smtp.send_message(message)