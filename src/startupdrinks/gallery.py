from dolmen.blob import BlobProperty
from plone.i18n.normalizer.interfaces import IURLNormalizer
from zope.component import getUtility
from zope.schema.fieldproperty import FieldProperty
import grok

from . import interfaces as ifaces
from . import _


class Gallery(grok.OrderedContainer):
    grok.implements(ifaces.IGallery)


class Photo(grok.Model):
    grok.implements(ifaces.IPhoto)

    picture = BlobProperty(ifaces.IPhoto['picture'])
    description = FieldProperty(ifaces.IPhoto['description'])


class Index(grok.View):
    grok.context(ifaces.IGallery)


class AddPhoto(grok.AddForm):
    grok.context(ifaces.IGallery)
    grok.name('add')
    form_fields = grok.AutoFields(ifaces.IPhoto)
    label = _(u'Add new photo')

    @grok.action(_('Add'))
    def handleAdd(self, **data):
        #New instance of Photo class with from attributes applied
        nw_photo = Photo()
        self.applyData(nw_photo, **data)

        #Now, get a url-safe title for the photo
        util = getUtility(IURLNormalizer)
        photo_id = util.normalize(nw_place.picture.blob.filename)

        #Add it to parent/context
        self.context[photo_id] = nw_photo
        grok.notify(grok.ObjectCreatedEvent(nw_photo))

        #Have fun!
        self.status = _(u'Yay! New photo added!')
        return self.redirect(self.url(self.context))


class DeletePhoto(grok.Form):
    grok.context(ifaces.IPhoto)
    grok.name('delete')

    @property 
    def label(self):
        return _(u'Do you really want to delete %s' % self.title)

    @grok.action(_(u'Delete'))
    def handleDelete(self, **data):
        parent = getParent(self.context)
        name = self.context.__name__
        del parent[name]

        self.status=_(u'The photo %s has been deleted' % name)
        self.redirect(self.url(self.context))
