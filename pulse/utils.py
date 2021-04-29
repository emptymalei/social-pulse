import feedparser


def rss_data(uri):
    """
    rss_data fetches the data from RSS

    :param uri: URI of the RSS
    :type uri: str
    """

    feed_data = feedparser.parse(uri)

    return feed_data
