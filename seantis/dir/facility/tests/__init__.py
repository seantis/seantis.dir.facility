from Products.PloneTestCase.ptc import PloneTestCase
from seantis.dir.facility.tests.layer import Layer


class IntegrationTestCase(PloneTestCase):
    layer = Layer

    def add_directory(self, name='Directory'):
        self.folder.invokeFactory('seantis.dir.facility.directory', name)
        return self.folder[name]

    def add_item(self, directory, name='DirectoryItem'):
        directory.invokeFactory('seantis.dir.facility.item', name)
        return directory[name]

    def add_resource(self, item, name='Resource'):
        item.invokeFactory('seantis.reservation.resource', name)
        return item[name]
