import json
import os

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

    def _load(self, path):
        if os.path.isfile(path):
            with open(path) as fp:
                self.config = json.load(fp)
        else:
            raise ValueError(f"Config file doesn't exist: {path}")

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
        res = self.config.copy()
        for p in path:
            res = res[p]

        return res

    def __getitem__(self, item):
        return self.get(item)


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
        if isinstance(config, str):
            config = Config()
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

        with open(self.local, "w") as fp:
            json.dump(self.pulses, fp, indent=2)

    def run(self):

        self.merge_pulses(self.get_existing_pulses(), self.get_new_pulses())
        self.save()


if __name__ == "__main__":

    conf = Config(
        {"name": "social pulse demo", "social": {"douban": {"id": "emptymalei"}}}
    )

    print(conf["name"], conf[["social", "douban"]])

    pass
