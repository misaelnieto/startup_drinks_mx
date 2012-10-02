import logging
from zope.generations.utility import findObjectsProviding, getRootFolder

from .. import interfaces as ifaces


logger = logging.getLogger('startupdrinks')


def evolve(context):
    root = getRootFolder(context)
    for site in findObjectsProviding(root, ifaces.IMainApp):
        evolve_site(site)


def evolve_site(site):
    logging.info("generations: 0 (%r)" % site)
