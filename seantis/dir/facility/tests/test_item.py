from zope.interface.verify import verifyObject

from seantis.dir.facility.item import IFacilityDirectoryItem
from seantis.dir.facility.tests import IntegrationTestCase
from seantis.dir.facility.utils import get_resources_in_context


class TestFacilityDirectoryItem(IntegrationTestCase):

    def test_interface(self):
        directory = self.add_directory()
        item = self.add_item(directory)
        self.assertTrue(verifyObject(IFacilityDirectoryItem, item))

    def test_resources(self):
        directory = self.add_directory()
        item = self.add_item(directory)
        self.assertEqual([], get_resources_in_context(item))

        resource = self.add_resource(item)
        self.assertEqual([resource], get_resources_in_context(item))
