import grok
import zope.interface
import zope.component
from zope.component.interfaces import ObjectEvent, IObjectEvent


class IApplicationInitializationEvent(IObjectEvent):
    """Main application has been added.

    Subscribers should add something to the initialization process.
    """


class ApplicationInitializationEvent(ObjectEvent):
    zope.interface.implements(IApplicationInitializationEvent)


def OnAppInit(func):
    """Decorator to bind func to the initialization process."""
    f = zope.component.adapter(ApplicationInitializationEvent)(func)
    zope.component.provideHandler(f)
    return f
