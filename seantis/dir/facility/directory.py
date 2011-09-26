from zope.interface import alsoProvides
from plone.namedfile.field import NamedImage
from plone.autoform.interfaces import IFormFieldProvider
from plone.app.dexterity.behaviors.metadata import MetadataBase
from plone.app.dexterity.behaviors.metadata import DCFieldProperty
from plone.directives import form

from seantis.dir.facility import _

class IFacilityDirectory(form.Schema):
    """Extends the seantis.dir.base.directory.IDirectory"""

    image = NamedImage(
            title=_(u'Image'),
            required=False,
            default=None
        )

alsoProvides(IFacilityDirectory, IFormFieldProvider)

class FacilityDirectory(MetadataBase):
    image = DCFieldProperty(IFacilityDirectory['image'])