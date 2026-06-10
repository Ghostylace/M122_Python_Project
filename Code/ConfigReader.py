"""
Module for reading configuration files.

This module provides the ConfigReader class for loading JSON configuration
files used to configure the application.
"""

import json
import os

class ConfigReader:
    """
    A class to read and load configuration from JSON files.
    """
    
    def read_config_file(self):
        """
        Read and parse the configuration file.
        
        Reads the config.json file from the current directory and returns
        the parsed JSON configuration. If the file is missing or corrupted,
        it will be deleted and recreated with an empty configuration, then
        the function will be called again to read the newly created file.
        
        Returns:
            dict: A dictionary containing the configuration data.
        """
        try:
            file = open("config.json")
            config = json.load(file)
            file.close()
            return config
        except (FileNotFoundError, json.JSONDecodeError):
            try:
                os.remove("config.json")
            except FileNotFoundError:
                pass
            with open("config.json", "w") as file:
                json.dump({}, file, indent=2)
            return self.read_config_file()