from five import grok

from zope.schema import TextLine, Text
from zope.interface import implements, Interface, alsoProvides

from collective.dexteritytextindexer import searchable
from plone.namedfile.field import NamedImage
from plone.directives import form
from plone.autoform.interfaces import IFormFieldProvider
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from plone.app.layout.viewlets.interfaces import IAboveContentBody

from seantis.dir.base import item, core
from seantis.dir.base.interfaces import (
    IFieldMapExtender,
    IDirectoryItem,
    IDirectoryItemBase,
    IDirectoryPage,
    IDirectoryCategorized
)

from seantis.dir.facility import _
from seantis.dir.facility.directory import IFacilityDirectory
from seantis.dir.facility.utils import get_resources_in_context

from seantis.reservation.overview import IOverview, OverviewletManager
from seantis.reservation import utils


class IFacilityDirectoryItem(IDirectoryItem):
    """Extends the seantis.dir.IDirectoryItem."""

    image = NamedImage(
        title=_(u'Image'),
        required=False
    )

    searchable('opening_hours')
    opening_hours = TextLine(
        title=_(u'Opening Hours'),
        required=False
    )

    searchable('contact')
    form.widget(contact=WysiwygFieldWidget)
    contact = Text(
        title=_(u'Location / Contact'),
        required=False
    )

    searchable('infrastructure')
    form.widget(infrastructure=WysiwygFieldWidget)
    infrastructure = Text(
        title=_(u'Infrastructure'),
        required=False
    )

    searchable('terms_of_use')
    form.widget(terms_of_use=WysiwygFieldWidget)
    terms_of_use = Text(
        title=_(u'Terms of Use'),
        required=False
    )

    searchable('notes')
    form.widget(notes=WysiwygFieldWidget)
    notes = Text(
        title=_(u'Notes'),
        required=False
    )

    form.fieldset(
        'facility_fields',
        label=_(u'Facility Information'),
        fields=['image', 'opening_hours', 'contact', 'infrastructure',
                'terms_of_use', 'notes']
    )


class FacilityDirectoryItem(item.DirectoryItem):
    pass


class ExtendedDirectoryItemFieldMap(grok.Adapter):
    """Adapter extending the import/export fieldmap of
    seantis.dir.facilty.item.

    """
    grok.context(IFacilityDirectory)
    grok.provides(IFieldMapExtender)

    def __init__(self, context):
        self.context = context

    def extend_import(self, itemmap):
        itemmap.typename = 'seantis.dir.facility.item'
        itemmap.interface = IFacilityDirectoryItem

        extended = ['opening_hours', 'contact', 'infrastructure',
                    'terms_of_use', 'notes']

        itemmap.add_fields(extended, len(itemmap))


class View(core.View):
    implements(IOverview)
    grok.context(IFacilityDirectoryItem)
    template = grok.PageTemplateFile('templates/item.pt')
    hide_search_viewlet = True

    def resources(self):
        return get_resources_in_context(self.context)

    @property
    def compare_link(self):
        return utils.compare_link(self.resources())

    @property
    def monthly_report_link(self):
        return utils.monthly_report_link(
            self.context,
            self.request,
            self.resources()
        )

    @property
    def is_itemview(self):
        return True

    def resource_map(self):
        return (r.UID for r in utils.portal_type_in_context(
            self.context, 'seantis.reservation.resource'
        ))


class DetailView(grok.Viewlet):
    grok.context(Interface)
    grok.name('seantis.dir.facility.detailview')
    grok.require('zope2.View')
    grok.viewletmanager(IAboveContentBody)

    _template = grok.PageTemplateFile('templates/itemdetail.pt')

    @property
    def show_viewlet(self):

        # TODO => all details, even the default ones, should be defined
        # through an item detail viewlet
        man = ItemDetailViewletManager(self.context, self.request, self)
        man.update()

        if man.viewlets:
            return True

        attributes = [
            'image',
            'opening_hours',
            'description',
            'contact',
            'infrastructure',
            'terms_of_use',
            'notes',
        ]

        for a in attributes:
            if not hasattr(self.context, a):
                return False

        for a in attributes:
            if getattr(self.context, a):
                return True

        return False

    @property
    def show_keywords(self):
        try:
            return bool(self.categories)
        except TypeError:
            return False

    @property
    def categories(self):
        return IDirectoryCategorized(self.context).categories()

    def render(self):
        if not self.show_viewlet:
            return u''

        return self._template.render(self)


class Mapviewlet(grok.Viewlet):
    grok.context(Interface)
    grok.name('seantis.dir.facility.mapviewlet')
    grok.require('zope2.View')
    grok.viewletmanager(OverviewletManager)

    grok.order(2)

    _template = grok.PageTemplateFile('templates/map.pt')

    def render(self):
        if IDirectoryPage.providedBy(self.view):
            return self._template.render(self)
        else:
            return u''


class ItemDetailViewletManager(grok.ViewletManager):
    grok.context(Interface)
    grok.name('seantis.dir.facility.item.detailviewletmanager')


# Provide the facility fields in a behavior which will then be activated for
# for seantis.reservation.resource. This allows resources to contain the
# fields of the facility. These fields will be filled with the values of the
# facility on creation. After that the values are independent.


class IFacilityFields(IFacilityDirectoryItem):
    """Provides the fields of Facility Directory Item to any Dexterity type"""
    form.omitted(*IDirectoryItemBase.names())


def default_value(data):
    """ Gets the default value of the context (facility) if the attribute
    is found.

    """
    if hasattr(data.context, data.field.__name__):
        return getattr(data.context, data.field.__name__)

# Setup the decorators
defaults = [None] * len(IFacilityDirectoryItem.names())
for ix, field in enumerate(IFacilityDirectoryItem.names()):
    defaults[ix] = form.default_value(
        field=IFacilityFields[field]
    )(default_value)

alsoProvides(IFacilityFields, IFormFieldProvider)
