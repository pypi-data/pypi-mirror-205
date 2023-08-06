# -*- coding: utf-8 -*-
import yaml

from coppyr.collections import DotDict
from coppyr.error import CoppyrError


# errors


class CoppyrConfigIOError(CoppyrError):
    description = "Error opening the config file."


class CoppyrConfigYAMLError(CoppyrError):
    description = "Couldn't load YAML."


# objects


class YAMLConfig(DotDict):
    def __init__(self, file_path=None):
        """
        :param file_path: String
            Path to the YAML file to load.  This can be absolute or relative.
        """
        if file_path is None:
            raise CoppyrConfigIOError(
                "File path not specified."
            )

        try:
            with open(file_path, "r") as f:
                raw = yaml.load(f, Loader=yaml.CLoader)
        except IOError as e:
            raise CoppyrConfigIOError(
                f"Failed to load file path \"{file_path}\".",
                caught=e
            )
        except Exception as e:
            raise CoppyrConfigYAMLError(caught=e)

        # Now load parsed yaml values into object attributes.
        super().__init__(**raw)

# TODO: Add an environment lookup for the configuration bit.
