from logging.config import dictConfig


dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s %(levelname)s %(process)d [%(filename)s:%(lineno)d] - %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
    },
})

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
    # Furthest acceptable distance from a public transportation stop, specified in miles.
    'max_distance': 1,
    'stops': {
        'Porter': (42.3841468, -71.12447),
        'Harvard': (42.3733705, -71.1211481),
        'Central': (42.3653208, -71.1055381),
        'Kendall': (42.3654375, -71.0949984),
    },
}

# Seconds to sleep between searches.
REFRESH_INTERVAL = 60 * 10
