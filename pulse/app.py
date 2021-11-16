import click
from pulse import Config
from douban import DoubanInterest, DoubanStatus
from github import GitHub
from loguru import logger
from pulse import CombinedPulse


@click.command()
@click.option("-c", "--config", type=click.Path(), help="Path to config")
def pulse(config):

    conf = Config(config)
    logger.debug(f"The full config: {conf}")

    # Douban
    logger.debug(f'Douban interest config: {conf[["social", "douban", "book_movie_music"]]}')
    douban_interests = DoubanInterest(
        conf[["social", "douban", "book_movie_music"]], base_folder="dashboard/data"
    )
    douban_interests.run()

    logger.debug(f'Douban status config: {conf[["social", "douban", "status"]]}')
    douban_status = DoubanStatus(
        conf[["social", "douban", "status"]], base_folder="dashboard/data"
    )
    douban_status.run()


    # GitHub
    logger.debug(f'GitHub config: {conf[["social", "github", "events"]]}')
    github = GitHub(conf[["social", "github", "events"]], base_folder="dashboard/data")
    github.run()

    # Combine
    combined_publse = CombinedPulse(
        [douban_interests.pulses, github.pulses], conf[["combined"]], base_folder="dashboard/data"
    )
    combined_publse.save()

    sm_combined_publse = CombinedPulse(
        [douban_interests.pulses, douban_status.pulses], conf[["combined-social-media"]], base_folder="dashboard/data"
    )
    sm_combined_publse.save()

    tech_combined_publse = CombinedPulse(
        [github.pulses], conf[["combined-tech"]], base_folder="dashboard/data"
    )
    tech_combined_publse.save()


if __name__ == "__main__":
    pulse()
