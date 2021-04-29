from os import stat
from utils import rss_data as _rss_data
from pulse import Pulse
from dateutil import parser


class Douban(Pulse):
    """Pulse for douban"""

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


if __name__ == "__main__":
    from pulse import Config

    conf = Config(
        {
            "user_id": "emptymalei",
            "artifacts": {"local": "douban__book_movie_music.json"},
        }
    )

    douban = Douban(conf, base_folder="dashboard/douban")

    douban.run()

    pass
