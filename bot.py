#!/usr/bin/env python
import logging
from pprint import pprint
from time import sleep

from craigslist import CraigslistHousing
from sqlalchemy import literal
from tqdm import trange

from apartments import settings
from apartments.models import Listing, session
from apartments.utils import annotate


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
    }

    housing = CraigslistHousing(**settings.CRAIGSLIST, filters=filters)
    results = housing.get_results(limit=20, sort_by='newest', geotagged=True)

    hits = []
    for result in results:
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
                nearest_stop = result.get('nearest_stop')
                # Listings which don't include geotags won't include a nearest stop.
                if nearest_stop is None or nearest_stop.distance <= settings.TRANSPORTATION['max_distance']:
                    hits.append(result)

    return hits


if __name__ == '__main__':
    logger.info('Bot initialized.')

    while True:
        logger.info('Searching Craigslist.')
        hits = search_listings()

        logger.info(f'Search complete. There were [{len(hits)}] hits.')
        pprint(hits)

        logger.info(f'Sleeping for [{settings.REFRESH_INTERVAL}] seconds.')
        for _ in trange(settings.REFRESH_INTERVAL):
            sleep(1)
