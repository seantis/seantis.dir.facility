from zope.interface.verify import verifyObject

from seantis.dir.facility.item import IFacilityDirectoryItem
from seantis.dir.facility.tests import IntegrationTestCase


class TestFacilityDirectoryItem(IntegrationTestCase):

    def test_interface(self):
        directory = self.add_directory()
        item = self.add_item(directory)
        self.assertTrue(verifyObject(IFacilityDirectoryItem, item))

    def test_resources(self):
        directory = self.add_directory()
        item = self.add_item(directory)
        self.assertEqual([], item.resources())

        resource = self.add_resource(item)
        self.assertEqual([resource], item.resources())
