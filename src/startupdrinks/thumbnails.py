from cStringIO import StringIO
import struct
from dolmen.blob import BlobValue
from dolmen.file import IImageField
from dolmen.thumbnailer import IImageMiniaturizer, Miniaturizer
from dolmen.thumbnailer.traversal import ThumbnailTraverser
from zope import component
from zope import schema
from zope.annotation.interfaces import IAnnotations
from zope.publisher.interfaces.http import IHTTPRequest
import grok

from . import interfaces as ifaces


class PhotoMiniaturizer(Miniaturizer):
    grok.context(ifaces.IPhoto)
    scales = {
        'large': (700, 700),
        'preview': (400, 400),
        'gallery': (300, 300),
        'mini': (250, 250),
        'thumb': (150, 150),
        'small': (128, 128),
        'button': (64, 64),
        'icon': (32, 32),
    }

    factory = BlobValue


def getImageInfo(data):
    data = str(data)
    size = len(data)
    height = -1
    width = -1
    content_type = ''

    # handle GIFs
    if (size >= 10) and data[:6] in ('GIF87a', 'GIF89a'):
        # Check to see if content_type is correct
        content_type = 'image/gif'
        w, h = struct.unpack("<HH", data[6:10])
        width = int(w)
        height = int(h)

    # See PNG 2. Edition spec (http://www.w3.org/TR/PNG/)
    # Bytes 0-7 are below, 4-byte chunk length, then 'IHDR'
    # and finally the 4-byte width, height
    elif ((size >= 24) and data.startswith('\211PNG\r\n\032\n')
          and (data[12:16] == 'IHDR')):
        content_type = 'image/png'
        w, h = struct.unpack(">LL", data[16:24])
        width = int(w)
        height = int(h)

    # Maybe this is for an older PNG version.
    elif (size >= 16) and data.startswith('\211PNG\r\n\032\n'):
        # Check to see if we have the right content type
        content_type = 'image/png'
        w, h = struct.unpack(">LL", data[8:16])
        width = int(w)
        height = int(h)

    # handle JPEGs
    elif (size >= 2) and data.startswith('\377\330'):
        content_type = 'image/jpeg'
        jpeg = StringIO(data)
        jpeg.read(2)
        b = jpeg.read(1)
        try:
            w = -1
            h = -1
            while (b and ord(b) != 0xDA):
                while (ord(b) != 0xFF): b = jpeg.read(1)
                while (ord(b) == 0xFF): b = jpeg.read(1)
                if (ord(b) >= 0xC0 and ord(b) <= 0xC3):
                    jpeg.read(3)
                    h, w = struct.unpack(">HH", jpeg.read(4))
                    break
                else:
                    jpeg.read(int(struct.unpack(">H", jpeg.read(2))[0])-2)
                b = jpeg.read(1)
            width = int(w)
            height = int(h)
        except struct.error:
            pass
        except ValueError:
            pass

    # handle BMPs
    elif (size >= 30) and data.startswith('BM'):
        kind = struct.unpack("<H", data[14:16])[0]
        if kind == 40: # Windows 3.x bitmap
            content_type = 'image/x-ms-bmp'
            width, height = struct.unpack("<LL", data[18:26])

    return content_type, width, height



IMG_INFO_KEY = 'IMG-INFO'

def annotate_pic_info(pic):
    info = dict(zip(('content_type', 'width', 'height'),
                    getImageInfo(pic.data)))
    annotations = IAnnotations(pic)
    v = annotations[IMG_INFO_KEY] = info
    return v

def update_thumbs(obj, fieldname):
    """Generates/Deletes thumbnails for field fieldname in object obj
    Of course, field must be an ImageField.
    """

    original = getattr(obj, fieldname, None)
    handler = IImageMiniaturizer(obj)

    # The image has been deleted if 'original' is None
    if original is None:
        # We delete the thumbnails.
        handler.delete(fieldname=fieldname)
    else:
        # We generate the thumbnails.
        handler.generate(fieldname=fieldname)
        for nm, item in handler.storage.items():
            annotate_pic_info(item)


@grok.subscribe(ifaces.IPhoto, grok.IObjectModifiedEvent)
def update_thumbnails_on_modify(obj, event):
    for attr in event.descriptions:
        if attr.interface is None: continue
        fields = [x for x, y in schema.getFields(attr.interface).items() if
                  IImageField.providedBy(y)]
        for fname in attr.attributes:
            if fname in fields:
                update_thumbs(obj, fname)


@grok.subscribe(ifaces.IPhoto, grok.IObjectCreatedEvent)
def update_thumbnails_on_create(obj, event):
    for iface in component.providedBy(obj).flattened():
        for fname, field in schema.getFields(iface).items():
            if IImageField.providedBy(field):
                update_thumbs(obj, fname)