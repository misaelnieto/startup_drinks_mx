from dolmen.blob import BlobProperty
from megrok import pagetemplate
from zope.traversing.api import getParent
import grok
import grokcore.layout
import megrok.z3cform.base as z3cform

from . import interfaces as ifaces
from . import _
from . import resource

class Banner(grok.Model):
    grok.implements(ifaces.IBanner)    
    picture = BlobProperty(ifaces.IPhoto['picture'])


class BannerEditForm(z3cform.EditForm):
    grok.name('edit')
    grok.context(ifaces.IBanner)
    # grok.require('sd.manage')
    
    fields = z3cform.Fields(ifaces.IBanner)
    label = _ (u'Use this form to upload a new banner or replace the existing one.')

    def application_url(self, name=None, data=None):
        """Return the URL of the closest :class:`grok.Application` object in
        the hierarchy or the URL of a named object (``name``
        parameter) relative to the closest application object.
        """
        return grok.util.application_url(self.request, self.context, name, data)

    def update(self):
        super(BannerEditForm, self).update()
        resource.bootstrap.need()
        resource.admin_css.need()

    @z3cform.button.buttonAndHandler(_('Save'))
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        changes = self.applyChanges(data)
        if changes:
            self.status = self.successMessage
        else:
            self.status = self.noChangesMessage

        parent = getParent(self.context)
        self.redirect(self.url(parent, 'admin'))


# class BannerEditPageTemplate(pagetemplate.PageTemplate):
#     grok.view(BannerEditForm)
#     template = grok.template('edit')
