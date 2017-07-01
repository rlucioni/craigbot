import os
from enum import Enum


class Condition(Enum):
    NEW = 10
    LIKE_NEW = 20
    EXCELLENT = 30


# Max number of new results to skim from Craigslist each time the bot runs.
CRAIGSLIST_RESULT_COUNT = int(os.environ.get('CRAIGSLIST_RESULT_COUNT', 20))

# Seconds to sleep before checking for new listings.
CRAIGSLIST_READ_DELAY = int(os.environ.get('CRAIGSLIST_READ_DELAY', 60 * 30))

# Max seconds that can be added or subtracted to CRAIGSLIST_READ_DELAY to create
# irregular access patterns.
CRAIGSLIST_JITTER = int(os.environ.get('CRAIGSLIST_JITTER', 60 * 10))

CRAIGSLIST_FORM = {
    'area': os.environ.get('CRAIGSLIST_AREA', 'boston'),
    'subarea': os.environ.get('CRAIGSLIST_SUBAREA', 'gbs'),
    'category': os.environ.get('CRAIGSLIST_CATEGORY', 'cta'),
}

CRAIGSLIST_CONDITIONS = os.environ.get('CRAIGSLIST_CONDITIONS', 'new,like_new,excellent').split(',')

CRAIGSLIST_QUERYSTRING = [
    ('min_price', int(os.environ.get('CRAIGSLIST_MIN_PRICE', 1000))),
    ('max_price', int(os.environ.get('CRAIGSLIST_MAX_PRICE', 7000))),
] + [
    ('condition', Condition[condition.upper()].value) for condition in CRAIGSLIST_CONDITIONS if condition
]

DEBUG = os.environ.get('DEBUG', False)

SLACK_USERNAME = 'craigbot'
SLACK_TOKEN = os.environ.get('SLACK_TOKEN')
SLACK_CHANNEL = os.environ.get('SLACK_CHANNEL', '#cars')
SLACK_ICON_URL = os.environ.get('SLACK_ICON_URL', 'http://i.imgur.com/txH8qrZ.png')
