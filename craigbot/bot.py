import logging
import random
from time import sleep
from urllib.parse import parse_qs, urlparse

from sqlalchemy import literal

from craigbot import settings
from craigbot.models import Result, session
from craigbot.utils import Craigslist, Slack


logger = logging.getLogger(__name__)


class Bot:
    """
    Bot for watching Craigslist listings and posting to Slack when it finds
    results matching certain criteria.
    """
    def __init__(self):
        logger.info('Initializing craigbot.')

        self.slack = Slack()

    @property
    def jitter(self):
        """
        Generate a random float in a configured range to make access patterns irregular.
        """
        return random.uniform(-settings.CRAIGSLIST_JITTER, settings.CRAIGSLIST_JITTER)

    def extract_url(self, result):
        """
        Extract original Craigslist URL from URL substituted by Google Translate.
        """
        raw_url = result.find_element_by_tag_name('a').get_attribute('href')
        qs = parse_qs(urlparse(raw_url).query)

        return qs['u'][0]

    def read(self):
        craigslist = Craigslist()

        try:
            results = craigslist.search()
        except:
            logger.exception('There was a problem searching Craigslist.')

            if craigslist.is_ip_banned():
                self.slack.post('Help! Craigslist has banned my IP.')

        # Craigslist seems to use pages of 120 results.
        logger.info(f'Found {len(results)} results.')

        count = 0
        for result in results:
            try:
                if count >= settings.CRAIGSLIST_RESULT_COUNT:
                    break

                pid = result.get_attribute('data-pid')
                repost_pid = result.get_attribute('data-repost-of')
                detail_url = self.extract_url(result)

                if self.seen(pid) or self.seen(repost_pid):
                    logger.info(f'Result at {detail_url} has already been seen. Skipping.')
                    continue

                self.share(result)
                self.save(result)

                count += 1

                logger.info(f'Processed {count} of {settings.CRAIGSLIST_RESULT_COUNT} results.')
            except:
                logger.exception('There was a problem processing a result. Continuing.')

    def save(self, result):
        """
        Write the result to the database, for future reference.
        """
        pid = result.get_attribute('data-pid')
        url = self.extract_url(result)

        obj = Result(craigslist_id=pid, url=url)
        session.add(obj)
        session.commit()

    def seen(self, pid):
        """
        Check if a result appears in the database.
        """
        q = session.query(Result).filter(Result.craigslist_id == pid)

        return session.query(literal(True)).filter(q.exists()).scalar()

    def share(self, result):
        """
        Share the provided result by posting a message to Slack.

        If debug mode is enabled, the message is logged instead.
        """
        title = result.find_element_by_css_selector('.result-title').get_attribute('innerText')
        price = result.find_element_by_css_selector('.result-price').get_attribute('innerText')
        hood = result.find_element_by_css_selector('.result-hood').get_attribute('innerText')
        timestamp = result.find_element_by_css_selector('.result-date').get_attribute('title')
        url = self.extract_url(result)

        message = f'Found {title} for {price} in {hood}. Posted {timestamp}. More details at {url}.'

        if settings.DEBUG:
            # When debugging, log messages instead of posting them to Slack.
            logger.info(message)
        else:
            self.slack.post(message)

    def watch(self):
        logger.info('Watching Craigslist.')

        while True:
            logger.info('Checking Craigslist for new results.')
            self.read()

            seconds = settings.CRAIGSLIST_READ_DELAY + self.jitter

            logger.info(f'Sleeping for {seconds} seconds.')
            sleep(seconds)
