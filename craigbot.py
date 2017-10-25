import logging
from logging.config import dictConfig


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
    logger.info('Checking Craigslist for new results.')
