from five import grok

from zope.schema import TextLine, Text
from zope.interface import alsoProvides, implements
from plone.namedfile.field import NamedImage
from plone.autoform.interfaces import IFormFieldProvider
from collective.dexteritytextindexer import IDynamicTextIndexExtender
from plone.directives import form
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from Products.CMFCore.utils import getToolByName

from seantis.dir.base import item
from seantis.dir.base import core
from seantis.dir.base.interfaces import IFieldMapExtender
from seantis.dir.base.fieldmap import FieldMap

from seantis.dir.facility import _

from seantis.reservation.overview import IOverview
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

    form.widget(contact=WysiwygFieldWidget)
    contact = Text(
            title=_(u'Location / Contact'),
            required=False
        )

    form.widget(infrastructure=WysiwygFieldWidget)
    infrastructure = Text(
            title=_(u'Infrastructure'),
            required=False
        )

    form.widget(terms_of_use=WysiwygFieldWidget)
    terms_of_use = Text(
            title=_(u'Terms of Use'),
            required = False
        )

    form.widget(notes=WysiwygFieldWidget)
    notes = Text(
            title=_(u'Notes'),
            required = False
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
            portal_type='seantis.reservation.resource',
            sort_on='sortable_title'
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
                         get(context, 'opening_hours'),
                         get(context, 'contact'),
                         get(context, 'infrastructure'),
                         get(context, 'terms_of_use'),
                         get(context, 'notes')
                    ))

        return result

class ExtendedDirectoryItemFieldMap(grok.Adapter):
    """Adapter extending the import/export fieldmap of seantis.dir.facilty.item."""
    grok.context(FieldMap)
    grok.provides(IFieldMapExtender)

    def __init__(self, context):
        self.context = context

    def extend_import(self):
        itemmap = self.context
        itemmap.interface = IFacilityDirectoryItem

        extended = ['opening_hours', 'contact', 'infrastructure',
                    'terms_of_use', 'notes']
        
        itemmap.add_fields(extended, len(itemmap))

class View(item.View):
    implements(IOverview)
    grok.context(item.IDirectoryItem)
    template = grok.PageTemplateFile('templates/item.pt')

    @property
    def compare_link(self):
        resources = self.context.resources()
        return utils.compare_link(resources)

    @property
    def monthly_report_link(self):
        resources = self.context.resources()
        return utils.monthly_report_link(self.context, resources)

    @property
    def items(self):
        return [self.context]