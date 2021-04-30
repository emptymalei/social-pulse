from os import stat
import requests
from pulse import Pulse
from dateutil import parser


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
