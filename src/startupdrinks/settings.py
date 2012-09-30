# from plone.registry import Registry
# from plone.registry.interfaces import IRegistry
from megrok.pagetemplate import PageTemplate
from megrok.z3cform.base.components import GrokForm
from zope.interface import Interface
import grok

from . import interfaces as ifaces
from .events import OnAppInit
from . import resource


class AdminMacros(grok.View):
    """
    This is a helper view for ZPT macros
    """
    grok.context(Interface)
    grok.require('sd.manage')


class Admin(grok.View):
    grok.context(ifaces.IMainApp)
    grok.require('sd.manage')

    def update(self):
        super(Admin, self).update()
        resource.bootstrap.need()
        resource.admin_css.need()


class AdminFormTemplate(PageTemplate):
    grok.view(GrokForm)
    grok.require('sd.manage')
