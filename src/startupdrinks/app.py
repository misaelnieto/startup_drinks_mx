import grok

from . import resource
from . import _
from . import interfaces as ifaces
from .banner import Banner
from .gallery import Gallery
from .map import Map

class StartupDrinks(grok.Application, grok.Container):
    grok.implements(ifaces.IMainApp)

    def __init__(self):
        super(StartupDrinks, self).__init__()

        #Add banner
        self['banner'] = Banner()
        grok.notify(grok.ObjectCreatedEvent(self['banner']))

        #Add Gallery
        self['gallery'] = Gallery()
        grok.notify(grok.ObjectCreatedEvent(self['gallery']))

        #Add Map
        self['map'] = Map()
        grok.notify(grok.ObjectCreatedEvent(self['map']))

        #Add settings?


class Index(grok.View):

    def update(self):
        resource.bootstrap.need()
        resource.styles_css.need()
        resource.map_init_js.need()

