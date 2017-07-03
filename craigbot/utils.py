import logging
from urllib.parse import quote_plus, urlencode

from selenium import webdriver
from slackclient import SlackClient

from craigbot import settings


logger = logging.getLogger(__name__)


class Craigslist:
    """
    Provides methods for interacting with a Craigslist result page.
    """
    def __init__(self):
        logger.info('Starting Chrome.')

        options = webdriver.ChromeOptions()
        options.binary_location = '/usr/bin/google-chrome-stable'
        options.add_argument('headless')
        # https://developers.google.com/web/updates/2017/04/headless-chrome#faq
        options.add_argument('disable-gpu')
        options.add_argument('window-size=1200x600')

        self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.implicitly_wait(10)

    @property
    def is_ip_banned(self):
        """
        Check if the current IP has been banned.

        Returns:
            Boolean
        """
        logger.info('Checking for IP ban.')

        craigslist_url = 'https://www.craigslist.org'
        self.proxy(craigslist_url)

        return 'blocked' in self.driver.page_source.lower()

    def proxy(self, craigslist_url):
        """
        Proxy the given Craigslist URL through Google Translate.
        """
        quoted = quote_plus(craigslist_url)
        url = f'https://translate.google.com/translate?hl=en&sl=es&tl=en&u={quoted}'

        self.driver.get(url)

        # Translated content is in an iframe named 'c'.
        self.driver.switch_to.frame('c')

    def search(self):
        logger.info('Proxying Craigslist search through Google Translate.')

        querystring = urlencode(settings.CRAIGSLIST_QUERYSTRING)
        craigslist_url = 'https://{area}.craigslist.org/search/{subarea}/{category}?{querystring}'.format(
            **settings.CRAIGSLIST_FORM,
            querystring=querystring
        )

        self.proxy(craigslist_url)

        logger.info('Loaded proxied results.')

        return self.driver.find_elements_by_css_selector('.result-row')


class Slack:
    """
    Provides methods for posting messages to a configured Slack channel.
    """
    def __init__(self):
        self.client = SlackClient(settings.SLACK_TOKEN)

    def post(self, message):
        """
        Post a message to the configured channel.
        """
        logger.info('Posting message to Slack.')

        self.client.api_call(
            # https://api.slack.com/methods/chat.postMessage
            'chat.postMessage',
            text=message,
            channel=settings.SLACK_CHANNEL,
            icon_url=settings.SLACK_ICON_URL,
            username=settings.SLACK_USERNAME,
            # Defaults to False
            unfurl_media=True,
        )
