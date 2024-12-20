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
        """
        Retrieve the value for a given key from the configuration data.
        If the key does not exist, return the default value.

        :param key: The configuration key to look up.
        :param default: The value to return if the key is not found.
        :return: The value associated with the key or the default value.
        """
        return self.data.get(key, default)

    def set(self, key, value):
        """
        Set a new value for a configuration key and update the config file.

        :param key: The configuration key to set.
        :param value: The value to set for the key.
        """
        self.data[key] = value
        self._write_config()

    def _write_config(self, path='config.json'):
        """
        Write the current configuration data to the specified file path.

        :param path: The path where the config file should be written.
        """
        with open(path, 'w') as f:
            json.dump(self.data, f, indent=4)

    def _write_default_config(self, path='config.json'):
        """
        Write a default configuration to the file if it does not exist.

        :param path: The path where the default config file should be written.
        """
        default_config = {
            "message_count": 5,
            "delay_between_messages": 2,
            "max_threads": 10,
            "use_colors": True,
            "num_threads": 4,
            "delay_between_stages": 1,
            "array_size": 1000000,
            "num_processes": 4,
            "num_arrays": 100,
            "words_to_count": ["python", "multiprocessing", "example"],
            "file_prefix": "text",
            "start_number": 2,
            "end_number": 100000
        }
        self.data = default_config
        self._write_config(path)