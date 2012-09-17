import grok
from plone.registry import Registry
from plone.registry.interfaces import IRegistry

from . import interfaces as ifaces
from .events import OnAppInit

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


class ControlPanel(grok.View):
    grok.context(ifaces.IMainApp)

