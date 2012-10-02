from zope.interface import Interface
from zope import schema
from dolmen.file import ImageField

from . import _

#########################################################
# This is the main application

class IMainApp(Interface):
    """This is the marker interface for the new application"""


#########################################################
# All this is for the map

class IMap(Interface):
    """
    A container for map places
    """

class IPlace(Interface):
    title = schema.TextLine(
        title=_(u"Title")
    )

    description = schema.Text(
        title=_(u'Description'),
        required=False
    )

    url = schema.URI(
        title=_(u'URL of the site')
    )

    latitude = schema.ASCIILine(
        title=_(u'Latitude'),
    )

    longitude = schema.ASCIILine(
        title=_(u'Longitude'),
    )

class IMapForm(Interface):
    """
    Marker interface for z3c.forms that use a google map
    """

######################################################
# All this is for the gallery

class IGallery(Interface):
    """
    This is the gallery. It contains photos
    """


class IPhoto(Interface):
    description = schema.Text(
        title=_(u"Description"),
        required=False
    )
    picture = ImageField(
        title=_(u"Picture"),
        required=True
    )

######################################################
# All this is for the banner

class IBanner(Interface):
    """
    A Banner
    """
    url = schema.URI(
        title=_(u'URL of the site'),
        description=_(u'Define this if you want the main banner to be clickable (useful for campaigns or selling spaces).'),
        required=False
    )
    picture = ImageField(
        title=_(u"Picture"),
        required=True
    )


######################################################
# All this is for the pages

class IPageFolder(Interface):
    """
    This is a container for Pages 
    """

class IPage(Interface):
    title = schema.TextLine(
        title = _(u'Title'),
        description = _(u'The title of the document')
    )

    body = schema.Text(
        title = _(u'Text body'),
    )
