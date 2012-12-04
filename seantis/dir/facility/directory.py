from five import grok
from zope.interface import implements

from Products.CMFPlone.PloneBatch import Batch
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

    @utils.memoize
    def resources(self):
        catalog = getToolByName(self, 'portal_catalog')
        path = '/'.join(self.getPhysicalPath())

        results = catalog(
            path={'query': path, 'depth': 2},
            portal_type='seantis.reservation.resource'
        )

        return [r.getObject() for r in results]


class ExtendedDirectoryViewlet(grok.Viewlet):
    grok.context(IDirectory)
    grok.name('seantis.dir.facility.directory.detail')
    grok.require('zope2.View')
    grok.viewletmanager(IBelowContentTitle)

    template = grok.PageTemplateFile('templates/directorydetail.pt')


class View(directory.View):
    implements(IOverview)
    grok.context(IFacilityDirectory)
    grok.require('zope2.View')
    template = grok.PageTemplateFile('templates/directory.pt')

    @property
    def compare_link(self):
        resources = self.context.resources()
        return utils.compare_link(resources)

    @property
    def monthly_report_link(self):
        resources = self.context.resources()
        return utils.monthly_report_link(self.context, self.request, resources)

    @property
    def batch(self):
        start = int(self.request.get('b_start') or 0)
        return Batch(self.items, 5, start, orphan=1)
