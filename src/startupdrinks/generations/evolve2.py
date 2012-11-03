import logging
from zope.annotation.interfaces import IAnnotations
from startupdrinks import interfaces as ifaces
from startupdrinks.thumbnails import update_thumbs

logger = logging.getLogger('startupdrinks')


def evolve(site):
    """
    * Generates thumbnais for all images.
    """

    #Banner
    logger.info("generations 2 re-generate banner thumbnais" % site)
    update_thumbs(site['banner'], 'picture')
    
    #Gallery
    logger.info("generations 2 re-generate gallery thumbnais" % site)
    for pic in site['gallery'].values():
        if ifaces.IPhoto.providedBy(pic):
            update_thumbs(pic, 'picture')
    
    logger.info("generations: 2 (%r) Ready." % site)

