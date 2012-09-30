from zope.schema.fieldproperty import FieldProperty
from zope.traversing.api import getParent
import grok
import megrok.z3cform.base as z3cform

from . import _
from . import interfaces as ifaces
from . import resource


class PageFolder(grok.Container):
    """
    This contains simple pages
    """
    grok.implements(ifaces.IPageFolder)


class Page(grok.Context):
    """
    This a very simple page
    """
    grok.implements(ifaces.IPage)

    title = FieldProperty(ifaces.IPage['title'])
    body = FieldProperty(ifaces.IPage['body'])


    def __init__(self, title, body):
        super(Page, self).__init__()
        self.title = title
        self.body = body


class EditPage(z3cform.EditForm):
    grok.context(ifaces.IPage)
    grok.name('edit')
    grok.require('sd.manage')
    label = _(u'You are editing a page')

    def application_url(self, name=None, data=None):
        return grok.util.application_url(self.request, self.context, name, data)

    def update(self):
        super(EditPage, self).update()
        resource.bootstrap.need()
        resource.admin_css.need()
        resource.wysihtml5_init.need()
