from five import grok

from zope.schema import TextLine
from zope.interface import alsoProvides
from plone.namedfile.field import NamedImage
from plone.autoform.interfaces import IFormFieldProvider
from collective.dexteritytextindexer import IDynamicTextIndexExtender
from plone.directives import form
from Products.CMFCore.utils import getToolByName

from seantis.dir.base import item
from seantis.dir.base import core

from seantis.dir.facility import _

from seantis.reservation import utils
  
class IFacilityDirectoryItem(form.Schema):
    """Extends the seantis.dir.IDirectoryItem."""

    image = NamedImage(
            title=_(u'Image'),
            required=False
        )

    opening_hours = TextLine(
            title=_(u'Opening Hours'),
            required=False
        )

alsoProvides(IFacilityDirectoryItem, IFormFieldProvider)

@core.ExtendedDirectory
class FacilityDirectoryItemFactory(core.DirectoryMetadataBase): # enterprisey!
    interface = IFacilityDirectoryItem

class FacilityDirectoryItem(item.DirectoryItem):

    def resources(self):
        catalog = getToolByName(self, 'portal_catalog')
        path = '/'.join(self.getPhysicalPath())

        results = catalog(
            path={'query': path, 'depth': 1},
            portal_type='seantis.reservation.resource'
        )

        return [r.getObject() for r in results]

class DirectoryItemSearchableTextExtender(grok.Adapter):
    grok.context(item.IDirectoryItem)
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

class View(item.View):
    grok.context(item.IDirectoryItem)
    template = grok.PageTemplateFile('templates/item.pt')

    @property
    def compare_link(self):
        resources = self.context.resources()
        return utils.compare_link(resources)

    @property
    def monthly_report_link(self):
        resources = self.context.resources()
        return utils.monthly_report_link(resources)
        
    def availability(self, resource):
        return int(resource.scheduler().availability())
        
