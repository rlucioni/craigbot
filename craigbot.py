import logging
from logging.config import dictConfig
from urllib.parse import quote_plus, urlencode

import requests
from bs4 import BeautifulSoup


dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '{asctime} {levelname} {process} [{filename}:{lineno}] - {message}',
            'style': '{',
        }
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
            'propagate': True,
        },
        'werkzeug': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
})

logger = logging.getLogger(__name__)


def check():
    # TODO: Consider pulling from https://www.zillow.com/homes/for_rent/02139_rb/
    # or https://www.walkscore.com/MA/Cambridge/02139
    logger.info('Proxying Craigslist search through Google Translate.')

    querystring = [
        ('min_price', 2000),
        ('max_price', 2500),
        # ('search_distance', 2),
        # ('postal', '02139'),
    ]

    q = urlencode(querystring)
    url = f'https://boston.craigslist.org/search/gbs/aap?{q}'

    logger.info(f'Craigslist URL: {url}')

    quoted = quote_plus(url)

    # Request made by iframe on the page at f'https://translate.google.com/translate?hl=en&sl=es&tl=en&u={quoted}'
    # usg param may be tied to URL or a specific translation of what was on that page at one time.
    # Param might need to be pulled from the page that contains the iframe.
    # curl 'https://translate.googleusercontent.com/translate_c?depth=2&hl=en&rurl=translate.google.com&sl=es&sp=nmt4&tl=en&u=https://boston.craigslist.org/search/gbs/aap%3Fmin_price%3D2000%26max_price%3D2500&usg=ALkJrhhUNVNDaWftLkh4p9p1RGKiYgJKrQ' -H 'pragma: no-cache' -H 'dnt: 1' -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: en-US,en;q=0.9' -H 'upgrade-insecure-requests: 1' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36' -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'cache-control: no-cache' -H 'authority: translate.googleusercontent.com' -H 'referer: https://translate.googleusercontent.com/translate_p?hl=en&rurl=translate.google.com&sl=es&sp=nmt4&tl=en&u=https://boston.craigslist.org/search/gbs/aap%3Fmin_price%3D2000%26max_price%3D2500&depth=2&usg=ALkJrhgAAAAAWgE339SiCZ7VkLp0AEOx2u_vHOHgOgUP' --compressed
    proxied = f'https://translate.googleusercontent.com/translate_c?depth=2&hl=en&rurl=translate.google.com&sl=es&sp=nmt4&tl=en&u={quoted}&usg=ALkJrhhUNVNDaWftLkh4p9p1RGKiYgJKrQ'

    logger.info(f'Google Translate URL: {proxied}')

    response = requests.get(proxied)
    soup = BeautifulSoup(response.text, 'html.parser')
    postings = soup.find_all('p', class_='result-info')

    # Expect 120 postings
    count = len(postings)
    logger.info(f'Found {count} postings')

    titles = [posting.find('a', class_='result-title') for posting in postings]
    metas = [posting.find('span', class_='result-meta') for posting in postings]

    logger.info(titles[0])
