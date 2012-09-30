import grok
from zope.interface import Interface

from . import interfaces as ifaces
from . import resource

class AdminPermission(grok.Permission):
    grok.name('sd.manage')


class AdminRole(grok.Role):
    grok.name('sd.administrator')
    grok.title('Administrator')
    grok.permissions(AdminPermission)
    grok.description('An admin can use the control panel')


class Login(grok.View):
    grok.context(Interface)
    camefrom = None

    def update(self, camefrom=None, SUBMIT=None):
        resource.bootstrap.need()
        self.camefrom=camefrom
        if SUBMIT is not None and camefrom is not None:
            # The credentials were entered. Go back. If the entered
            # credentials are not valid, another redirect will happen
            # to this view.
            self.redirect(camefrom)
        return
