import feedparser


def douban_interests(id):
    """
    interests fetches the interests of a douban user

    :param id: id of the douban user
    :type id: str
    """

    interests_uri = f"https://www.douban.com/feed/people/{id}/interests"

    feed_data = feedparser.parse(interests_uri)

    interests = feed_data.get("entries")

    return interests







if __name__ == "__main__":

    test_id = "emptymalei"

    douban_interests(test_id)

    pass

