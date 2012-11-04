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


class SponsorsContainer(grok.OrderedContainer):
    grok.implements(ifaces.ISponsorsContainer)


class Sponsor(grok.Model):
    grok.implements(ifaces.ISponsor, ifaces.IPhoto)

    description = FieldProperty(ifaces.ISponsor['description'])
    picture = BlobProperty(ifaces.ISponsor['picture'])
    url = FieldProperty(ifaces.ISponsor['url'])

    def __init__(self, picture=None, description=u'', url=''):
        super(Sponsor, self).__init__()
        self.picture = picture
        self.description = description
        self.url = url


class Index(grok.View):
    grok.context(ifaces.ISponsorsContainer)
    grok.require('sd.manage')

    def update(self):
        super(Index, self).update()
        resource.bootstrap.need()
        resource.admin_css.need()


class AddSponsor(z3cform.AddForm):
    grok.name('add')
    grok.context(ifaces.ISponsorsContainer)
    grok.require('sd.manage')
    fields = z3cform.Fields(ifaces.ISponsor)
    label = _(u'Use this form to add a new sponsor')

    def application_url(self, name=None, data=None):
        return grok.util.application_url(self.request, self.context, name, data)

    def update(self):
        super(AddSponsor, self).update()
        resource.bootstrap.need()
        resource.admin_css.need()

    def create(self, data):
        return Sponsor(
            picture=data['picture'], 
            description=data['description'],
            url=data['url']
        )

    def add(self, nw_sponsor):
        #Now, get a url-safe title for the photo
        util = getUtility(IURLNormalizer)
        photo_id = util.normalize(nw_sponsor.picture.filename)

        #Add it to parent/context
        self.context[photo_id] = nw_sponsor
        self.status = _(u'Yay! New sponsor added!')

    def nextURL(self):
        return self.url(self.context)


class EditSponsor(z3cform.EditForm):
    grok.name('edit')
    grok.context(ifaces.ISponsor)
    grok.require('sd.manage')
    label = _(u'Edit the sponsor')

    def application_url(self, name=None, data=None):
        return grok.util.application_url(self.request, self.context, name, data)

    def update(self):
        super(EditSponsor, self).update()
        resource.bootstrap.need()
        resource.admin_css.need()

    def nextURL(self):
        return self.url(self.context)


class DeletePhoto(grok.View):
    grok.context(ifaces.ISponsor)
    grok.name('delete')
    grok.require('sd.manage')

    def render(self):
        parent = getParent(self.context)
        name = self.context.__name__
        del parent[name]

        self.flash((u'The sponsor %s has been deleted' % name))
        return self.redirect(self.url(parent))
