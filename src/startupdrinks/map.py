from megrok.pagetemplate import PageTemplate
from plone.i18n.normalizer.interfaces import IURLNormalizer
from zope.component import getUtility
from zope.schema.fieldproperty import FieldProperty
from zope.traversing.api import getParent
import grok
import megrok.z3cform.base as z3cform

from . import interfaces as ifaces
from . import _
from . import resource


class Map(grok.Container):
    """
    This contains all the places in the map.
    """
    grok.implements(ifaces.IMap)


class Place(grok.Context):
    """
    This is a place on the map
    """
    grok.implements(ifaces.IPlace)

    title = FieldProperty(ifaces.IPlace['title'])
    description = FieldProperty(ifaces.IPlace['description'])
    url = FieldProperty(ifaces.IPlace['url'])
    latitude = FieldProperty(ifaces.IPlace['latitude'])
    longitude = FieldProperty(ifaces.IPlace['longitude'])

    def __init__(self, title=u'', description=u'', url='', latitude=0.0, longitude=0.0):
        super(Place, self).__init__()
        self.title = title
        self.description = description
        self.url = url
        self.latitude = latitude
        self.longitude = longitude


class Index(grok.View):
    """
    This is the main view in the map (equivalent to index.html)
    """
    grok.context(ifaces.IMap)
    grok.require('sd.manage')

    def update(self):
        super(Index, self).update()
        resource.bootstrap.need()
        resource.admin_css.need()


class Places(grok.JSON):
    grok.context(ifaces.IMap)

    def places_json(self):
        result = []
        for place in self.context.values():
            result.append({
                'title': place.title,
                'description': place.description,
                'url': place.url,
                'latitude': place.latitude,
                'longitude': place. longitude
            })
        return result


class AddPlace(z3cform.AddForm):
    """
    Used to add a place to the map
    """
    grok.name('add')
    grok.context(ifaces.IMap)
    grok.implements(ifaces.IMapForm)
    grok.require('sd.manage')

    fields = z3cform.Fields(ifaces.IPlace)
    label = _(u'Add a place to the map')

    def application_url(self, name=None, data=None):
        return grok.util.application_url(self.request, self.context, name, data)

    def update(self):
        super(AddPlace, self).update()
        resource.bootstrap.need()
        resource.admin_css.need()
        resource.map_edit_js.need()

    def create(self, data):
        #New instance of Place class with form data
        return Place(
            title = data['title'],
            description = data['description'],
            url = data['url'],
            latitude = data['latitude'],
            longitude = data['longitude']
        )

    def add(self, nw_place):
        #Get a url-safe name for the place object
        util = getUtility(IURLNormalizer)
        place_id = util.normalize(nw_place.title)

        #Add it to parent/context
        self.context[place_id] = nw_place

        #Have fun!
        self.status = _(u'Yeah! New place added')

    def nextURL(self):
        return self.url(self.context)


class FormTemplate(PageTemplate):
    grok.view(ifaces.IMapForm)
    grok.require('sd.manage')


class EditPlace(z3cform.EditForm):
    """
    Form to edit an already existing place
    """
    grok.context(ifaces.IPlace)
    grok.implements(ifaces.IMapForm)
    grok.name('edit')
    grok.require('sd.manage')
    label = _(u'You are editing a place')

    def application_url(self, name=None, data=None):
        return grok.util.application_url(self.request, self.context, name, data)

    def update(self):
        super(EditPlace, self).update()
        resource.bootstrap.need()
        resource.admin_css.need()
        resource.map_edit_js.need()


class DeletePlace(grok.View):
    grok.context(ifaces.IPlace)
    grok.name('delete')
    grok.require('sd.manage')

    def render(self):
        parent = getParent(self.context)
        name = self.context.__name__
        del parent[name]

        self.flash((u'The place %s has been deleted' % name))
        return self.redirect(self.url(parent))
