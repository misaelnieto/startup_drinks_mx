# from plone.registry import Registry
# from plone.registry.interfaces import IRegistry
from megrok.pagetemplate import PageTemplate
from megrok.z3cform.base.components import GrokForm
from zope.interface import Interface
import grok

from . import interfaces as ifaces
from .events import OnAppInit
from . import resource

# Utilities

# class GlobalRegistry(Registry, grok.LocalUtility):
#     grok.site(ifaces.IConsworks)


# @OnAppInit
# def setup(event):
#     app = event.object

#     logger.info("Adding global settings.")
#     registry = GlobalRegistry()
#     sm = app.getSiteManager()
#     sm.registerUtility(
#         registry, provided=IRegistry, name="settings")

#     registry.registerInterface(ifaces.IMailerSettings,
#                                prefix='sd.MailerSettings')


class AdminMacros(grok.View):
    """
    This is a helper view for ZPT macros
    """
    grok.context(Interface)


class Admin(grok.View):
    grok.context(ifaces.IMainApp)

    def update(self):
        super(Admin, self).update()
        resource.bootstrap.need()
        resource.admin_css.need()


class AdminFormTemplate(PageTemplate):
    grok.view(GrokForm)
