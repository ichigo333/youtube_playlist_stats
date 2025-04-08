import os
import json

class Config:
    
    def __init__(self, config_file_name):
        self.config_file_name = config_file_name
        self.config = self._load_config()
    
    def _load_config(self):
        location = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(location, self.config_file_name)
        with open(path) as jsonFile:
          config = json.load(jsonFile)
        return config
    
    @property
    def client_secrets_file_name(self):
        return self.config["client_secrets_file_name"]
    
    @property
    def token_file_name(self):
        return self.config["token_file_name"]
    
    @property
    def playlist_id(self):
        return self.config["playlist_id"]