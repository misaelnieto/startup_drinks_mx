"""
Add page for cities
"""
import logging
import grok
from startupdrinks import interfaces as ifaces
from startupdrinks.pages import Page

logger = logging.getLogger('startupdrinks')


def evolve(site):
    """Describe changes here"""

    if ifaces.IMainApp.providedBy(site):
        nw_obj = Page(title=u'Ciudades', body=u'Editame')
        site['pages']['ciudades'] = nw_obj
        grok.notify(grok.ObjectCreatedEvent(nw_obj))

        logger.info("Generations: 1 (%r)" % site)
