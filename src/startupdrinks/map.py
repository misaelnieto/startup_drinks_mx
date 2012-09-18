from plone.i18n.normalizer.interfaces import IURLNormalizer
from zope.component import getUtility
from zope.schema.fieldproperty import FieldProperty
from zope.traversing.api import getParent
import grok

from . import interfaces as ifaces

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


class Index(grok.View):
    """
    This is the main view in the map (equivalent to index.html)
    """
    grok.context(ifaces.IMap)


class AddPlace(grok.AddForm):
    """
    Used to add a place to the map
    """
    grok.context(ifaces.IMap)
    grok.name('add')
    form_fields = grok.AutoFields(ifaces.IPlace)
    label = _(u'Add a place to the map')

    @grok.action(_('Add'))
    def handleAdd(self, **data):
        #New instance of Place class with form data
        nw_place = Place()
        self.applyData(nw_place, **data)

        #Get a url-safe name for the place object
        util = getUtility(IURLNormalizer)
        place_id = util.normalize(nw_place.title)

        #Add it to parent/context
        self.context[place_id] = nw_place
        grok.notify(grok.ObjectCreatedEvent(nw_place))

        #Have fun!
        self.status = _(u'Yeah! New place added')
        return self.redirect(self.url(self.context))


class EditPlace(grok.EditForm):
    """
    Form to edit an already existing place
    """
    grok.context(ifaces.IPlace)
    grok.name('edit')
    form_fields = grok.AutoFields(ifaces.IPlace)
    
    @property
    def label(self):
        return _(u'You are editing: %s' % self.title)


class DeletePlace(grok.Form):
    """
    Form to delete already existing place
    """
    grok.context(ifaces.IPlace)
    grok.name('delete')
    
    @property 
    def label(self):
        return _(u'Do you really want to delete %s' % self.title)

    @grok.action(_(u'Delete'))
    def handleDelete(self, **data):
        parent = getParent(self.context)
        name = self.context.__name__
        del parent[name]

        self.status = _(u'The place %s has been deleted' % name)
        self.redirect(self.url(self.context))
