from five import grok

from zope.schema import TextLine
from zope.interface import alsoProvides
from plone.namedfile.field import NamedImage
from plone.autoform.interfaces import IFormFieldProvider
from plone.app.dexterity.behaviors.metadata import MetadataBase
from plone.app.dexterity.behaviors.metadata import DCFieldProperty
from collective.dexteritytextindexer import IDynamicTextIndexExtender
from plone.directives import form

from seantis.dir.base.item import IDirectoryItem
from seantis.dir.facility import _
  
class IFacilityDirectoryItem(form.Schema):
    """Extends the seantis.dir.IDirectoryItem."""

    image = NamedImage(
            title=_(u'Image'),
            required=False,
            default=None
        )

    opening_hours = TextLine(
            title=_(u'Opening Hours'),
            required=False,
            default=u''
        )

alsoProvides(IFacilityDirectoryItem, IFormFieldProvider)

class FacilityDirectoryItem(MetadataBase):
    image = DCFieldProperty(IFacilityDirectoryItem['image'])
    opening_hours = DCFieldProperty(IFacilityDirectoryItem['opening_hours'])


class DirectoryItemSearchableTextExtender(grok.Adapter):
    grok.context(IDirectoryItem)
    grok.name('IFacilityDirectoryItem')
    grok.provides(IDynamicTextIndexExtender)

    def __init__(self, context):
        self.context = context

    def __call__(self):
        """Extend the searchable text with a custom string"""
        context = self.context
        get = lambda ctx, attr: hasattr(ctx, attr) and unicode(getattr(ctx, attr)) or u''

        result = ' '.join((
                         get(context, 'opening_hours')
                    ))

        return result