import grok

from . import resource
from . import _
from . import interfaces as ifaces


class StartupDrinks(grok.Application, grok.Container):
    grok.implements(ifaces.IMainApp)

    def __init__(self):
        super(StartupDrinks, self).__init__()

        #Add Map

        #Add Gallery

        #Add settings?


class Index(grok.View):
    def update(self):
        resource.bootstrap.need()
        resource.styles.need()
