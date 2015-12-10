from five import grok
from zope.interface import implements

from Products.CMFCore.utils import getToolByName
from plone.namedfile.field import NamedImage
from plone.app.layout.viewlets.interfaces import IBelowContentTitle

from seantis.dir.base import directory
from seantis.dir.base.interfaces import IDirectory

from seantis.dir.facility import _

from seantis.reservation.interfaces import IOverview
from seantis.reservation import utils


class IFacilityDirectory(IDirectory):
    """Extends the seantis.dir.base.directory.IDirectory"""

    image = NamedImage(
        title=_(u'Image'),
        required=False
    )


class FacilityDirectory(directory.Directory):

    def resources(self):
        catalog = getToolByName(utils.getSite(), 'portal_catalog')
        path = '/'.join(self.getPhysicalPath())

        return catalog(
            path={'query': path, 'depth': 2},
            portal_type='seantis.reservation.resource'
        )


class ExtendedDirectoryViewlet(grok.Viewlet):
    grok.context(IFacilityDirectory)
    grok.name('seantis.dir.facility.directory.detail')
    grok.require('zope2.View')
    grok.viewletmanager(IBelowContentTitle)

    template = grok.PageTemplateFile('templates/directorydetail.pt')


class View(directory.View):
    implements(IOverview)
    grok.context(IFacilityDirectory)
    grok.require('zope2.View')

    template = grok.PageTemplateFile('templates/directory.pt')

    itemsperpage = 5

    @property
    def compare_link(self):
        resources = self.context.resources()
        return utils.compare_link(resources)

    @property
    def monthly_report_link(self):
        resources = self.context.resources()
        return utils.monthly_report_link(self.context, self.request, resources)

    def resource_map(self):
        rmap = {}
        for item in utils.maybe_call(self.items):
            # if the item itself is a resource it won't be found by
            # portal_type_in_context since that method searches 'inside'
            if item.portal_type == 'seantis.reservation.resource':
                rmap[item.id] = [item.UID]
            else:
                rmap[item.id] = [r.UID for r in utils.portal_type_in_context(
                    item, 'seantis.reservation.resource'
                )]

        return rmap
