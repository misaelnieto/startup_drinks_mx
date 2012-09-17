import grok
from dolmen.blob import BlobProperty

from . import interfaces as ifaces
from . import _


class Banner(grok.Model):
    grok.implements(ifaces.IBanner)    
    picture = BlobProperty(ifaces.IPhoto['picture'])


class Edit(grok.EditForm):
    grok.context(ifaces.IBanner)
    form_fields = grok.AutoFields(ifaces.IBanner)

    label = _ (u'Want to upload a new banner?')
