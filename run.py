#!/usr/bin/env python
import logging
from time import sleep

from craigbot import settings
from craigbot.utils import search_listings, Slack


logger = logging.getLogger(__name__)


if __name__ == '__main__':
    logging.basicConfig(
        style='{',
        format='{asctime} {levelname} {process} [{filename}:{lineno}] - {message}',
        level=logging.INFO
    )

    logger.info('Bot initialized.')

    while True:
        logger.info('Searching Craigslist.')
        hits = search_listings()

        logger.info('Search complete.')

        if hits:
            logger.info(f'[{len(hits)}] hit(s) found. Posting to Slack.')
            Slack().post_listings(hits)

        logger.info(f'Sleeping for [{settings.REFRESH_INTERVAL}] seconds.')
        sleep(settings.REFRESH_INTERVAL)
