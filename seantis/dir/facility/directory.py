from five import grok
from zope.interface import alsoProvides
from zope.interface import implements
from plone.namedfile.field import NamedImage
from plone.autoform.interfaces import IFormFieldProvider
from plone.directives import form

from seantis.dir.base import directory
from seantis.dir.base import core

from seantis.dir.facility import _

from seantis.reservation.overview import IOverview

class IFacilityDirectory(form.Schema):
    """Extends the seantis.dir.base.directory.IDirectory"""

    image = NamedImage(
            title=_(u'Image'),
            required=False
        )

alsoProvides(IFacilityDirectory, IFormFieldProvider)

@core.ExtendedDirectory
class FacilityDirectory(core.DirectoryMetadataBase):
    interface = IFacilityDirectory

class View(directory.View):
    implements(IOverview)
    grok.context(directory.IDirectory)
    grok.require('zope2.View')
    template = grok.PageTemplateFile('templates/directory.pt')