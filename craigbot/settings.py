import os


# Yields https://boston.craigslist.org/search/gbs/aap.
CRAIGSLIST = {
    'site': 'boston',
    'area': 'gbs',
    'category': 'aap',
}

# Price range used to filter listings.
MIN_PRICE = 1500
MAX_PRICE = 2500

# Number of raw listings to fetch from Craigslist each time the bot runs.
LISTING_LIMIT = 50

# Create these using http://boundingbox.klokantech.com.
# You can verify using https://www.mapcustomizer.com.
BOUNDING_BOXES = {
    'Central Sq': {
        'bottom_left': (42.359475, -71.111831),
        'top_right': (42.369441, -71.09563)
    },
}

# Used to handle listings without coordinates.
NEIGHBORHOODS = {
    'Porter Sq': ['porter'],
    'Harvard Sq': ['harvard'],
    'Central Sq': ['central'],
    'Cambridgeport': ['cambridgeport'],
    'Kendall Sq': ['kendall', 'mit'],
}

# Grouped points of interest (e.g., public transportation stops, grocery stores,
# gyms) whose proximity we care about. If a listing has a geotag, the bot will find
# the point nearest to it in each group.
POINTS_OF_INTEREST = [
    # T stations
    {
        'Davis station': (42.3967488, -71.1240042),
        'Porter station': (42.3883876, -71.1213363),
        'Harvard station': (42.3733705, -71.1211481),
        'Central station': (42.3653248, -71.1057794),
        'Kendall/MIT station': (42.3625441, -71.0886322),
        'Charles/MGH station': (42.3611376, -71.0727132),
    },
    # Grocery stores
    {
        'Mass Ave H Mart': (42.3650305, -71.1047913),
        'Broadway Marketplace': (42.3738145, -71.115356),
        'Somerville Ave Market Basket': (42.3807302, -71.1037855),
        'Beacon St Star Market': (42.3836354, -71.1139615),
        'McGrath Highway Star Market': (42.3715417, -71.0856603),
        'Sidney St Star Market': (42.3619648, -71.1018443),
        'White St Star Market': (42.3900509, -71.1200286),
        'Boylston St Trader Joe\'s': (42.3484452, -71.0862902),
        'Memorial Dr Trader Joe\'s': (42.358235, -71.1164017),
        'Beacon St Whole Foods': (42.3757734, -71.1052882),
        'Prospect St Whole Foods': (42.3680644, -71.1044664),
        'River St Whole Foods': (42.360995, -71.1161267),
    },
]

SLACK_TOKEN = os.environ.get('SLACK_TOKEN')
SLACK_CHANNEL = '#apartments'
SLACK_USERNAME = 'craigbot'
SLACK_ICON_URL = 'http://i.imgur.com/txH8qrZ.png'

# Seconds to sleep between searches.
REFRESH_INTERVAL = 60 * 20
