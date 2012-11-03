import transaction
from zope.generations.generations import SchemaManager
from zope.generations.utility import findObjectsProviding, getRootFolder
from zope.site.hooks import setSite

from .. import interfaces as ifaces

GENERATION = 2

class MySchemaManager(SchemaManager):
    def evolve(self, context, generation):
        name = "%s.evolve%d" % (self.package_name, generation)

        evolver = __import__(name, {}, {}, ['*'])

        root = getRootFolder(context)
        for site in findObjectsProviding(root, ifaces.IMainApp):
            setSite(site)
            evolver.evolve(site)
        transaction.commit()


schemaManager = MySchemaManager(
    minimum_generation=GENERATION,
    generation=GENERATION,
    package_name='startupdrinks.generations')
