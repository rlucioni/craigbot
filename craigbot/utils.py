from collections import namedtuple
from functools import partial

from geopy.distance import vincenty
import requests
from slackclient import SlackClient

from craigbot import settings


Point = namedtuple('Point', ['latitude', 'longitude'])
Stop = namedtuple('Stop', ['name', 'distance'])


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


def nearest_stop(geotag):
    """
    Find the name and distance to the nearest public transportation stop.

    Arguments:
        geotag (tuple): Latitude and longitude.

    Returns:
        Stop (namedtuple): Name of the nearest stop and the distance to it.
    """
    stops = []
    for name, location in settings.TRANSPORTATION['stops'].items():
        distance = vincenty(geotag, location).miles
        distance = round(distance, 2)
        stops.append(Stop(name, distance))

    return min(stops, key=lambda stop: stop.distance)


def normalized_neighborhood(where):
    """
    Normalize raw location labels from Craigslist.

    Arguments:
        where (str): Raw location label from Craigslist.

    Returns:
        str: Label of the matching neighborhood.
        None: If no matching labels were found.
    """
    for label, fragments in settings.NEIGHBORHOODS.items():
        if any(fragment in where.lower() for fragment in fragments):
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
        result['nearest_stop'] = nearest_stop(geotag)

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
            username='craigbot',
            icon_emoji=':robot_face:'
        )

    def post_listings(self, listings):
        """
        Post one message for each listing to the channel.

        Arguments:
            listings (list): Containing dicts representing Craigslist listings.

        Returns:
            None
        """
        for listing in listings:
            price = listing['price']
            neighborhood = listing['neighborhood']
            nearest_stop = listing.get('nearest_stop')
            url = listing['url']

            message = f'{price} in {neighborhood}. '

            if nearest_stop:
                message += f'{nearest_stop.distance} miles from {nearest_stop.name} stop. '

            message += f'{url}'

            self.post_message(text=message)

    def post_ip_ban_warning(self):
        """
        Warn the channel that the bot's current IP has been banned.

        Returns:
            None
        """
        self.post_message(text='Help! Craigslist has banned my IP.')
