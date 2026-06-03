import json

class ConfigReader:
    def read_config_file(self):
        file = open("config.json")
        config = json.load(file)
        return config