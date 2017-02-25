#!/usr/bin/env python
import logging
from time import sleep

from sqlalchemy import literal

from craigbot import settings
from craigbot.models import Listing, session
from craigbot.utils import annotate, is_ip_banned, Slack


logger = logging.getLogger(__name__)


def search_listings():
    """
    Search recent listings on Craigslist.

    Writes all results to the database to avoid reporting duplicates.

    Returns:
        list: Results matching configured search criteria.
    """
    filters = {
        'min_price': settings.PRICE['min'],
        'max_price': settings.PRICE['max'],
        'has_image': True,
    }

    try:
        # Importing and initializing CraigslistHousing occasionally raises an exception.
        from craigslist import CraigslistHousing
        housing = CraigslistHousing(**settings.CRAIGSLIST, filters=filters)
    except:
        logger.exception('Unable to initialize CraigslistHousing. Skipping and checking for IP ban.')

        if is_ip_banned():
            Slack().post_ip_ban_warning()

        return

    result_generator = housing.get_results(limit=20, sort_by='newest', geotagged=True)

    hits = []
    while True:
        try:
            # Calling next() causes a request to be made to Craigslist, which
            # may in turn raise an exception.
            result = next(result_generator)
        except StopIteration:
            break
        except:
            logger.exception('Unable to fetch a result. Skipping.')
            continue

        craigslist_id = result['id']

        logger.info(f'Found listing [{craigslist_id}].')

        # Check if we've seen this listing.
        q = session.query(Listing).filter(Listing.craigslist_id == craigslist_id)
        seen = session.query(literal(True)).filter(q.exists()).scalar()

        if not seen:
            logger.info(f'Listing [{craigslist_id}] is new. Recording it.')

            # Record the listing.
            listing = Listing(craigslist_id=craigslist_id, url=result['url'])
            session.add(listing)
            session.commit()

            # Annotate the result in-place.
            annotate(result)

            # If a neighborhood is present, the result is in a configured region
            # of interest.
            if result.get('neighborhood'):
                hits.append(result)

    return hits


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
