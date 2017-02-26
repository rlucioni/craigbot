from collections import namedtuple
from functools import partial
import logging

from geopy.distance import vincenty
import requests
from slackclient import SlackClient
from sqlalchemy import literal

from craigbot import settings
from craigbot.models import Listing, session


logger = logging.getLogger(__name__)

POI = namedtuple('POI', ['name', 'distance'])
Point = namedtuple('Point', ['latitude', 'longitude'])


class Slack:
    """
    Utility class for posting messages to a configured Slack channel.
    """
    def __init__(self):
        client = SlackClient(settings.SLACK_TOKEN)

        self.post_message = partial(
            client.api_call,
            'chat.postMessage',
            channel=settings.SLACK_CHANNEL,
            username=settings.SLACK_USERNAME,
            icon_url=settings.SLACK_ICON_URL
        )

    def post_listing(self, listing):
        """
        Post a message describing the provided listing to the configured channel.

        Arguments:
            listing (dict): Representing an annotated Craigslist listing.

        Returns:
            None
        """
        price = listing['price']
        neighborhood = listing['neighborhood']
        nearest_points_of_interest = listing.get('nearest_points_of_interest')
        url = listing['url']

        message = f'{price} in {neighborhood}. '

        if nearest_points_of_interest:
            for poi in nearest_points_of_interest:
                message += f'{poi.distance} miles from {poi.name}. '

        message += f'{url}'

        self.post_message(text=message)

    def post_ip_ban_warning(self):
        """
        Warn the channel that the bot's current IP has been banned.

        Returns:
            None
        """
        self.post_message(text='Help! Craigslist has banned my IP.')


def bounding_box(geotag):
    """
    Find the bounding box containing the given point.

    Arguments:
        geotag (tuple): Latitude and longitude.

    Returns:
        str: Label corresponding to the bounding box.
        None: If no bounding box contains the point.
    """
    point = Point(*geotag)
    for label, box in settings.BOUNDING_BOXES.items():
        bottom_left = Point(*box['bottom_left'])
        top_right = Point(*box['top_right'])

        within_latitudes = bottom_left.latitude < point.latitude < top_right.latitude
        within_longitudes = bottom_left.longitude < point.longitude < top_right.longitude
        if within_latitudes and within_longitudes:
            return label


def nearest_points_of_interest(geotag):
    """
    Find the names and distances to the nearest points of interest.

    Arguments:
        geotag (tuple): Latitude and longitude.

    Returns:
        dict: Containing POI namedtuples.
    """
    nearest_points_of_interest = []

    for location_map in settings.POINTS_OF_INTEREST:
        pois = []

        for name, coordinates in location_map.items():
            distance = vincenty(geotag, coordinates).miles
            distance = round(distance, 2)
            pois.append(POI(name, distance))

        nearest = min(pois, key=lambda poi: poi.distance)
        nearest_points_of_interest.append(nearest)

    return nearest_points_of_interest


def normalized_neighborhood(where):
    """
    Normalize raw location labels from Craigslist.

    Arguments:
        where (str): Raw location label from Craigslist.

    Returns:
        str: Label of the matching neighborhood.
        None: If the listing is ignored, or no matching labels were found.
    """
    where = where.lower()

    is_ignored = any(string in where for string in settings.IGNORE)
    if is_ignored:
        return

    for label, strings in settings.NEIGHBORHOODS.items():
        is_match = any(string in where for string in strings)
        if is_match:
            return label


def annotate(result):
    """
    Annotate the given result with additional data.

    This function mutates the provided result.

    Arguments:
        result (dict)

    Returns:
        None
    """
    geotag = result['geotag']
    where = result['where']

    # TODO: Support overlapping bounding boxes and tags shared across
    # neighborhoods (e.g., 'mit' may be associated with Central and Kendall).
    if geotag:
        result['neighborhood'] = bounding_box(geotag)
        result['nearest_points_of_interest'] = nearest_points_of_interest(geotag)

    # If the listing wasn't in one of the configured bounding boxes (or was missing
    # coordinates), we may still be able to get something useful from the where label.
    if not result.get('neighborhood') and where:
        result['neighborhood'] = normalized_neighborhood(where)


def is_ip_banned():
    """
    Check if the current IP has been banned.

    Returns:
        Boolean
    """
    response = requests.get('https://www.craigslist.org')

    # Craigslist responds to requests from banned IPs with a 403.
    return response.status_code == 403


def search_listings():
    """
    Search recent listings on Craigslist.

    Writes all results to the database to avoid reporting duplicates.

    Returns:
        int: Count of new results matching configured search criteria.
    """
    count = 0
    slack = Slack()

    filters = {
        'min_price': settings.MIN_PRICE,
        'max_price': settings.MAX_PRICE,
        'has_image': True,
    }

    try:
        # Importing and initializing CraigslistHousing involves making a request
        # to Craigslist. This may raise an exception if the bot's IP is banned.
        from craigslist import CraigslistHousing
        housing = CraigslistHousing(**settings.CRAIGSLIST, filters=filters)
    except:
        logger.exception('Unable to initialize CraigslistHousing. Skipping and checking for IP ban.')

        if is_ip_banned():
            slack.post_ip_ban_warning()

        return count

    result_generator = housing.get_results(
        limit=settings.LISTING_LIMIT,
        sort_by='newest',
        geotagged=True
    )

    while True:
        try:
            # Calling next() causes a request to be made to Craigslist. This may
            # raise an exception if the bot's IP is banned.
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
                count += 1

                logger.info(f'Posting listing [{craigslist_id}] to Slack.')
                slack.post_listing(result)

    return count
