import logging
import grok
from startupdrinks.sponsors import SponsorsContainer

logger = logging.getLogger('startupdrinks')

def evolve(site):
    """Add sponsors as a gallery"""
    site['sponsors'] = SponsorsContainer()
    grok.notify(grok.ObjectCreatedEvent(site['gallery']))
    logger.info("generations: 3 (%r) Ready" % site)
