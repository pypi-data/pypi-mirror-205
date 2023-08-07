import os
from pathlib import Path

import toml


class ConfigManager:
    """
    Singleton class to manage the config file and keep the config in memory.
    """
    __instance = None

    def __new__(cls, *args, **kwargs):
        """
        Create and return a new ConfigManager instance if one does not already exist.

        If a ConfigManager instance already exists, return that instance instead.

        Read in the `promptbot.toml` file if it exists, otherwise raise `FileNotFoundError`.

        Parameters:
            cls: The class being instantiated.
            *args: Any positional arguments to be passed to the class constructor.
            **kwargs: Any keyword arguments to be passed to the class constructor.

        Returns:
            An instance of the ConfigManager class.
        """
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            try:
                with open(Path(os.curdir, 'promptbot.toml'), 'r') as f:
                    cls.__instance.config = toml.load(f)
            except FileNotFoundError:
                raise FileNotFoundError(
                    "promptbot.toml not found. Please create one in the root directory of the project.")
        return cls.__instance

    def get_config(self):
        """
        Get the config file as a dictionary.

        Returns:
            A dictionary containing the contents of the config file.
        """
        return self.config
