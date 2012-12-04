from zope.interface.verify import verifyObject

from seantis.dir.facility.directory import IFacilityDirectory
from seantis.dir.facility.tests import IntegrationTestCase


class TestFacilityDirectoryItem(IntegrationTestCase):

    def test_interface(self):
        directory = self.add_directory()
        self.assertTrue(verifyObject(IFacilityDirectory, directory))
