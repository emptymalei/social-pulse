from os import stat
from utils import rss_data as _rss_data
from pulse import Pulse
from dateutil import parser


class DoubanInterest(Pulse):
    """Pulse for douban interests"""

    def __init__(self, config, base_folder=None):
        super().__init__(config, base_folder)

    @staticmethod
    def book_movie_music(id):
        """
        book_movie_music fetches the interests of a douban user

        :param id: id of the douban user
        :type id: str
        """

        interests_uri = f"https://www.douban.com/feed/people/{id}/interests"

        feed_data = _rss_data(interests_uri)

        interests = feed_data.get("entries")

        return interests

    @staticmethod
    def get_stats(data):
        """
        get_stats finds the dates of the activities
        """
        records = {}
        for d in data:
            d_dt = parser.parse(d["published"]).date().isoformat()
            if d_dt not in records:
                records[d_dt] = 1

        return records

    def get_new_pulses(self):

        self.new_pulses = self.get_stats(self.book_movie_music(self.config["user_id"]))

        return self.new_pulses




class DoubanStatus(Pulse):
    """Pulse for douban status"""

    def __init__(self, config, base_folder=None):
        super().__init__(config, base_folder)

    @staticmethod
    def status(num_id):
        """
        status get douban status

        Beware that the num_id should be the numerical id (e.g., 1587390). [More Details](https://docs.rsshub.app/social-media.html#dou-ban)
        """

        status_uri = f"https://rsshub.app/douban/people/{num_id}/status"

        feed_data = _rss_data(status_uri)

        status = feed_data.get("entries")

        return status

    @staticmethod
    def get_stats(data):
        """
        get_stats finds the dates of the activities
        """
        records = {}
        for d in data:
            d_dt = parser.parse(d["published"]).date().isoformat()
            if d_dt not in records:
                records[d_dt] = 1

        return records

    def get_new_pulses(self):

        self.new_pulses = self.get_stats(self.status(self.config["user_id"]))

        return self.new_pulses



if __name__ == "__main__":

    from pulse import Config

    conf_interests = Config(
        {
            "user_id": "emptymalei",
            "artifacts": {"local": "douban__book_movie_music.json"},
        }
    )

    douban_interests = DoubanInterest(conf_interests, base_folder="dashboard/data/douban")

    douban_interests.run()

    conf_status = Config(
        {
            "user_id": "1587390",
            "artifacts": {"local": "douban__status.json"},
        }
    )

    douban_status = DoubanStatus(conf_status, base_folder="dashboard/data/douban")

    douban_status.run()

    pass
