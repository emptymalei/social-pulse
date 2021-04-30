import click
from pulse import Config
from douban import Douban
from github import GitHub
from loguru import logger
from pulse import CombinedPulse


@click.command()
@click.option("-c", "--config", type=click.Path(), help="Path to config")
def pulse(config):

    conf = Config(config)
    logger.debug(f"The full config: {conf}")

    # Douban
    logger.debug(f'Douban config: {conf[["social", "douban", "book_movie_music"]]}')
    douban = Douban(
        conf[["social", "douban", "book_movie_music"]], base_folder="dashboard/data"
    )
    douban.run()

    # GitHub
    logger.debug(f'GitHub config: {conf[["social", "github", "events"]]}')
    github = GitHub(conf[["social", "github", "events"]], base_folder="dashboard/data")
    github.run()

    # Combine
    combined_publse = CombinedPulse(
        [douban.pulses, github.pulses], conf[["combined"]], base_folder="dashboard/data"
    )
    combined_publse.save()


if __name__ == "__main__":
    pulse()
