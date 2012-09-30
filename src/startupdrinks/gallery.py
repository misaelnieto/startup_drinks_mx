from dolmen.blob import BlobProperty
from plone.i18n.normalizer.interfaces import IURLNormalizer
from zope.component import getUtility
from zope.schema.fieldproperty import FieldProperty
from zope.traversing.api import getParent
import grok
import megrok.z3cform.base as z3cform

from . import interfaces as ifaces
from . import _
from . import resource


class Gallery(grok.OrderedContainer):
    grok.implements(ifaces.IGallery)


class Photo(grok.Model):
    grok.implements(ifaces.IPhoto)

    picture = BlobProperty(ifaces.IPhoto['picture'])
    description = FieldProperty(ifaces.IPhoto['description'])

    def __init__(self, picture=None, description=u''):
        super(Photo, self).__init__()
        self.picture = picture
        self.description = description


class Index(grok.View):
    grok.context(ifaces.IGallery)
    grok.require('sd.manage')

    def update(self):
        super(Index, self).update()
        resource.bootstrap.need()
        resource.admin_css.need()


class AddPhoto(z3cform.AddForm):
    grok.name('add')
    grok.context(ifaces.IGallery)
    grok.require('sd.manage')
    fields = z3cform.Fields(ifaces.IPhoto)
    label = _(u'Use this form to add a new photo')

    def application_url(self, name=None, data=None):
        return grok.util.application_url(self.request, self.context, name, data)

    def update(self):
        super(AddPhoto, self).update()
        resource.bootstrap.need()
        resource.admin_css.need()

    def create(self, data):
        return Photo(
            picture=data['picture'], 
            description=data['description']
        )

    def add(self, nw_photo):
        #Now, get a url-safe title for the photo
        util = getUtility(IURLNormalizer)
        photo_id = util.normalize(nw_photo.picture.filename)

        #Add it to parent/context
        self.context[photo_id] = nw_photo
        self.status = _(u'Yay! New photo added!')

    def nextURL(self):
        return self.url(self.context)



class DeletePhoto(grok.View):
    grok.context(ifaces.IPhoto)
    grok.name('delete')
    grok.require('sd.manage')

    def render(self):
        parent = getParent(self.context)
        name = self.context.__name__
        del parent[name]

        self.flash((u'The photo %s has been deleted' % name))
        return self.redirect(self.url(parent))
