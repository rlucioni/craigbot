import os


# Yields https://boston.craigslist.org/search/gbs/aap.
CRAIGSLIST = {
    'site': 'boston',
    'area': 'gbs',
    'category': 'aap',
}

PRICE = {
    'min': 1500,
    'max': 2500,
}

# Create these using http://boundingbox.klokantech.com.
# You can verify using https://www.mapcustomizer.com.
BOUNDING_BOXES = {
    'Central Square': {
        'bottom_left': (42.359475, -71.111831),
        'top_right': (42.369441, -71.09563)
    },
}

# Used to handle listings without coordinates.
NEIGHBORHOODS = {
    'Porter Square': ['porter'],
    'Harvard Square': ['harvard'],
    'Central Square': ['central'],
    'Cambridgeport': ['cambridgeport'],
    'Kendall Square': ['kendall', 'mit'],
}

TRANSPORTATION = {
    'stops': {
        'Porter': (42.3841468, -71.12447),
        'Harvard': (42.3733705, -71.1211481),
        'Central': (42.3653208, -71.1055381),
        'Kendall': (42.3654375, -71.0949984),
    },
}

SLACK_TOKEN = os.environ.get('SLACK_TOKEN')
SLACK_CHANNEL = '#apartments'
SLACK_USERNAME = 'craigbot'
SLACK_ICON_URL = 'http://i.imgur.com/txH8qrZ.png'

# Seconds to sleep between searches.
REFRESH_INTERVAL = 60 * 20
