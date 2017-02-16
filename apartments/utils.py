from collections import namedtuple

from geopy.distance import vincenty

from apartments import settings


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

    if geotag:
        result['neighborhood'] = bounding_box(geotag)
        result['nearest_stop'] = nearest_stop(geotag)
    elif where:
        result['neighborhood'] = normalized_neighborhood(where)
