import grok
from itertools import izip_longest
import megrok.login

from . import _
from . import interfaces as ifaces
from . import resource
from .banner import Banner
from .gallery import Gallery
from .map import Map
from .pages import PageFolder, Page
from .sponsors import SponsorsContainer


class StartupDrinks(grok.Application, grok.Container):
    grok.implements(ifaces.IMainApp)
    megrok.login.enable()
    megrok.login.viewname('login')

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

        #Add Pages
        self['pages'] = PageFolder()
        grok.notify(grok.ObjectCreatedEvent(self['pages']))
        self['pages']['asistentes'] = Page(title=u'Asistentes', body=u'Editame')
        self['pages']['acerca-de'] = Page(title=u'Acerca de...', body=u'Editame')
        self['pages']['ciudades'] = Page(title=u'Ciudades', body=u'Editame')

        # Add Sponsors
        self['sponsors'] = SponsorsContainer()
        grok.notify(grok.ObjectCreatedEvent(self['gallery']))


class Index(grok.View):

    def update(self):
        resource.bootstrap.need()
        resource.styles_css.need()
        resource.map_init_js.need()
        resource.landing_page_js.need()

    def gallery_groups(self):
        """
        Returns all gallery pictures in groups of three each.
        modified version of grouper function found in itertools documentation
        """

        "Collect data into fixed-length chunks or blocks"
        # grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
        n = 3
        iterable = self.context['gallery'].values()
        args = [iter(iterable)] * 3
        return izip_longest(fillvalue=None, *args)
