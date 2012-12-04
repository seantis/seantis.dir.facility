from plone.testing import z2
from zope.configuration import xmlconfig
from plone.app.testing import IntegrationTesting
from plone.app.testing import applyProfile
from plone.app.testing import quickInstallProduct

from seantis.reservation.testing import SqlLayer
from seantis.reservation.testing import SQL_FIXTURE


class IntegrationTestLayer(SqlLayer):
    default_bases = (SQL_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        SqlLayer.setUpZope(self, app, configurationContext)

        import seantis.dir.facility
        xmlconfig.file(
            'configure.zcml',
            seantis.dir.facility,
            context=configurationContext
        )
        z2.installProduct(app, 'seantis.dir.facility')

    def tearDownZope(self, app):
        SqlLayer.tearDownZope(self, app)
        z2.uninstallProduct(app, 'seantis.dir.facility')

    def setUpPloneSite(self, portal):
        SqlLayer.setUpPloneSite(self, portal)
        quickInstallProduct(portal, 'seantis.dir.facility')
        applyProfile(portal, 'seantis.dir.facility:default')

FIXTURE = IntegrationTestLayer()

Layer = IntegrationTesting(
    bases=(FIXTURE,),
    name="seantis.dir.facility:Integration"
)
