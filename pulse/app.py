import click
from pulse import Config
from douban import Douban
from loguru import logger



@click.command()
@click.option("-c", '--config', type=click.Path(), help='Path to config')
def pulse(config):

    conf = Config(config)
    logger.debug(f"The full config: {conf}")

    # Douban
    logger.debug(f'Douban config: {conf[["social", "douban", "book_movie_music"]]}')
    douban = Douban(conf[["social", "douban", "book_movie_music"]], base_folder="dashboard/data")
    douban.run()


if __name__ == "__main__":
    pulse()