import json
from logging import debug, log
import os
import pandas as pd
from loguru import logger


class Config:
    """
    Builds the configs from a file.

    ```
    >>> c = Config("path/to/my/config.json")
    >>> c_2 = Config({"name": "this is a demo"})
    >>> print(c["name"])
    >>> print()
    ```
    """

    def __init__(self, config):

        if isinstance(config, dict):
            self.config = config
        elif isinstance(config, str):
            self.config = self._load(config)
        else:
            raise Exception(
                f"Specify either a path to config file or a dictionary as the config"
            )
        logger.debug(f"Intialized to {self.config}")

    def _load(self, path):

        if os.path.isfile(path):
            logger.debug(f"Loading content from {path}")
            with open(path) as fp:
                config = json.load(fp)
            logger.debug(f"Loaded content as config ({type(config)}):\n{config}")
            if config is None:
                raise Exception(f"Could not load content from {path}")
        else:
            raise ValueError(f"Config file doesn't exist: {path}")

        return config

    def get(self, path):
        """
        Get value of the configs under specified path
        :param list path: path to the value to be obtained
        ```
        >>> c.get(['etl','raw'])
        {'local':'data/raw', 'remote': 's3://haferml-tutorials/rideindego/marshall/data/raw'}
        ```
        """

        # Construct the path
        if not isinstance(path, (list, tuple)):
            logger.warning(f"path is not list nor tuple, converting to list: {path}")
            path = [path]

        # Find the values
        logger.debug(f"{self.config}")
        res = self.config.copy()
        for p in path:
            res = res[p]
        if isinstance(res, dict):
            res = Config(res)

        return res

    def __getitem__(self, item):
        return self.get(item)

    def __str__(self) -> str:
        return f"{self.config}"


class Pulse:
    """
    Pulse is responsible for the aggregation of all social pulse data:

    - Take in raw data of specific format
      - e.g., time series data
    - Take in existing data
      - from a data file
    - aggregate the existing data and new data
    - save
      - as a data file, e.g., json
    """

    def __init__(self, config, base_folder=None):
        self.name = "Pulse is a data holder and processor"
        if isinstance(config, (str, dict)):
            config = Config(config)
        self.config = config
        self.base_folder = base_folder
        self.local = self.config[["artifacts", "local"]]
        if self.base_folder:
            self.local = os.path.join(self.base_folder, self.local)

    def get_new_pulses(self):
        """
        get_new_pulses collects new pulses: self.new_pulses
        """
        raise NotImplementedError(f"Please implement this method...")

    def get_existing_pulses(self):
        """
        get_existing_pulses loads the existing pulse records
        """

        if not os.path.isfile(self.local):
            logger.warning(
                f"artifacts do not exist:\n{self.local}; will create new file."
            )
            self.existing_pulses = {}
        else:
            with open(self.local, "r") as fp:
                self.existing_pulses = json.load(fp)

        return self.existing_pulses

    def merge_pulses(self, existing, new):
        """
        merge_pulses merges the existing pulses and the new pulses
        """
        self.pulses = {**existing, **new}
        return self.pulses

    def save(self):
        """
        save dumps the pulses into a file
        """

        logger.debug(f"Saving pulses to {self.local}...")
        logger.debug("checking if folder exists...")
        if not os.path.exists(os.path.dirname(self.local)):
            os.makedirs(os.path.dirname(self.local))

        with open(self.local, "w") as fp:
            json.dump(self.pulses, fp, indent=2)

        logger.debug(f"Saving csv to {self.local}...")
        df = pd.DataFrame(list(self.pulses.items()), columns=['Date', 'Value'])
        df.to_csv(self.local.replace(".json", ".csv"))

    def run(self):

        self.merge_pulses(self.get_existing_pulses(), self.get_new_pulses())
        self.save()


class CombinedPulse:
    def __init__(self, pulses, config, base_folder=None):
        if not isinstance(pulses, (list, tuple)):
            raise ValueError("Input should be a list of pulses")

        self._combine(pulses)

        self.name = "Combined Pulses"
        if isinstance(config, (str, dict)):
            config = Config(config)
        self.config = config
        self.base_folder = base_folder

        self.local = self.config[["artifacts", "local"]]
        if self.base_folder:
            self.local = os.path.join(self.base_folder, self.local)

    def _combine(self, pulses):
        self.pulses = {}
        for p in pulses:
            self.pulses.update(p)

    def save(self):
        """
        save dumps the pulses into a file
        """

        logger.debug(f"Saving pulses to {self.local}...")
        logger.debug(f"checking if folder exists...")
        if not os.path.exists(os.path.dirname(self.local)):
            os.makedirs(os.path.dirname(self.local))

        with open(self.local, "w") as fp:
            json.dump(self.pulses, fp, indent=2)

        logger.debug(f"Saving csv to {self.local}...")
        df = pd.DataFrame(list(self.pulses.items()), columns=['Date', 'Value'])
        df.to_csv(self.local.replace(".json", ".csv"))


if __name__ == "__main__":

    conf = Config(
        {"name": "social pulse demo", "social": {"douban": {"id": "emptymalei"}}}
    )

    print(conf["name"], conf[["social", "douban"]])

    pass
