from os import stat
import requests
from pulse import Pulse
from dateutil import parser
from loguru import logger
import datetime
import os
import json
import pandas as pd

class GitHub(Pulse):
    """Pulse for github"""

    def __init__(self, config, base_folder=None):
        super().__init__(config, base_folder)

    @staticmethod
    def events(id):
        """
        events fetches the interests of a douban user

        :param id: id of the douban user
        :type id: str
        """

        events_uri = f"https://api.github.com/users/{id}/events"

        events = requests.get(url=events_uri).json()

        return events

    @staticmethod
    def orgs(id: str) -> dict:

        orgs_uri = f"https://api.github.com/users/{id}/orgs"

        orgs = requests.get(url=orgs_uri).json()

        return orgs

    @staticmethod
    def user_repos(id: str) -> dict:
        """
        repos fetches the repositories of a github user

        :param id: id of the github user
        :type id: str
        """

        repos_uri = f"https://api.github.com/users/{id}/repos"

        repos = requests.get(url=repos_uri).json()

        return repos

    @staticmethod
    def org_repos(org: str) -> dict:
        """
        org_repos fetches the repositories of a github organization

        :param org: name of the github organization
        :type org: str
        """

        repos_uri = f"https://api.github.com/orgs/{org}/repos"

        repos = requests.get(url=repos_uri).json()

        return repos

    @staticmethod
    def get_stats(data):
        """
        get_stats finds the dates of the activities
        """
        records = {}
        for d in data:
            d_dt = parser.parse(d["created_at"]).date().isoformat()
            if d_dt not in records:
                records[d_dt] = 1

        return records

    def get_new_pulses(self):

        self.new_pulses = self.get_stats(self.events(self.config["user_id"]))

        return self.new_pulses


class GitHubStats(Pulse):
    """Stats for github
    """

    def __init__(self, config, base_folder=None):
        super().__init__(config, base_folder)

        self.dt = datetime.datetime.now().date().isoformat()
        self.json_folder = os.path.join(self.local, "json")

    @staticmethod
    def orgs(id: str) -> dict:

        orgs_uri = f"https://api.github.com/users/{id}/orgs"

        orgs = requests.get(url=orgs_uri).json()

        return orgs

    @staticmethod
    def user_repos(id: str) -> dict:
        """
        repos fetches the repositories of a github user

        :param id: id of the github user
        :type id: str
        """

        repos_uri = f"https://api.github.com/users/{id}/repos"

        repos = requests.get(url=repos_uri).json()

        return repos

    @staticmethod
    def org_repos(org: str) -> dict:
        """
        org_repos fetches the repositories of a github organization

        :param org: name of the github organization
        :type org: str
        """

        repos_uri = f"https://api.github.com/orgs/{org}/repos"

        repos = requests.get(url=repos_uri).json()

        return repos

    @staticmethod
    def get_stats(data):
        """
        get_stats finds the dates of the activities
        """
        records = {}
        for d in data:
            d_dt = parser.parse(d["created_at"]).date().isoformat()
            if d_dt not in records:
                records[d_dt] = 1

        return records

    def get_new_pulses(self):

        self.new_pulses = self.get_all_repos()

        logger.debug(f"Saving data to {self.local}...")
        logger.debug("checking if folder exists...")
        if not os.path.exists(self.local):
            os.makedirs(self.local)


        if not os.path.exists(self.json_folder):
            os.makedirs(self.json_folder)

        snapshot_file_path = os.path.join(self.json_folder, f"{self.dt}.json")

        with open(snapshot_file_path, "w") as fp:
            json.dump(self.new_pulses, fp, indent=2)

        return self.new_pulses

    def get_existing_pulses(self):
        """
        get_existing_pulses loads the existing pulse records
        """

        if not os.path.exists(self.json_folder):
            logger.warning(
                f"artifacts do not exist:\n{self.json_folder}; will create empty content."
            )
            self.existing_pulses = []
        else:
            json_files = [
                p for p in os.listdir(self.json_folder)
                if p.endswith('.json')
            ]
            logger.debug(f"Found {len(json_files)} json files ...")
            self.existing_pulses = []
            for i in json_files:
                with open(i, "r") as fp:
                    self.existing_pulses += json.load(fp)

        return self.existing_pulses

    def merge_pulses(self, existing, new):
        """
        merge_pulses merges the existing pulses and the new pulses
        """
        self.pulses = existing + new
        return self.pulses

    def get_all_repos(self):

        user_repos = self.user_repos(self.config["user_id"])

        dt = self.dt

        logger.debug("User repos ...")
        repos_data = [
            {
                "date": dt,
                "full_name": r["full_name"],
                "stargazers_count": r["stargazers_count"],
                "watchers_count": r["watchers_count"],
                "forks_count": r["forks_count"],
                "domain": f"{self.config['user_id']}",
            }
            for r in user_repos
        ]
        logger.debug(f"In total {len(repos_data)} user repos found ...")

        logger.debug("Gettin org data ...")
        all_orgs = self.orgs(self.config["user_id"])
        for org in all_orgs:
            logger.debug(f"Getting repos for {org['login']} ...")
            org_repos = self.org_repos(org["login"])
            org_repos_data = [
                {
                    "date": dt,
                    "full_name": r["full_name"],
                    "stargazers_count": r["stargazers_count"],
                    "watchers_count": r["watchers_count"],
                    "forks_count": r["forks_count"],
                    "domain": f"{org['login']}",
                }
                for r in org_repos
            ]
            repos_data += org_repos_data

        logger.debug(f"In total {len(repos_data)} repos found ...")

        return repos_data

    def save(self):
        """
        save dumps the pulses into a file
        """
        full_csv_path = self.local + ".csv"
        logger.debug(f"Saving csv to {full_csv_path}...")
        df = pd.DataFrame(self.existing_pulses)
        df.to_csv(full_csv_path, index=False)

    def run(self):
        self.get_new_pulses()
        self.get_existing_pulses()
        self.save()


if __name__ == "__main__":

    from pulse import Config

    conf = Config(
        {
            "user_id": "emptymalei",
            "artifacts": {"local": "douban__book_movie_music.json"},
        }
    )

    github = GitHub(conf, base_folder="dashboard/github")

    github.run()

    pass
