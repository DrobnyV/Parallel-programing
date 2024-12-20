import json
import os


class Config:
    def __init__(self, path='config.json'):
        self.data = {}
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    self.data = json.load(f)
            except json.JSONDecodeError:
                print(f"Error: The config file at {path} is not valid JSON. Using default configurations.")
        else:
            print(f"Warning: Config file at {path} not found. Using default configurations.")
            self._write_default_config(path)

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self._write_config()

    def _write_config(self, path='config.json'):
        with open(path, 'w') as f:
            json.dump(self.data, f, indent=4)

    def _write_default_config(self, path='config.json'):
        default_config = {
            "message_count": 5,
            "delay_between_messages": 2,
            "max_threads": 10,
            "use_colors": True
        }
        self.data = default_config
        self._write_config(path)