import logging
log = logging.getLogger('seantis.reservation')

from Products.CMFCore.utils import getToolByName
from zope.component.hooks import getSite

from StringIO import StringIO
from plone.namedfile.file import NamedImage
from seantis.reservation import utils as reservation_utils


def upgrade_to_1000(context):

    # 2 untangles the dependency hell that was default <- sunburst <- izug.
    # Now, sunburst and izug.basetheme both have their own profiles.

    # Since the default profile therefore has only the bare essential styles
    # it needs to be decided on upgrade which theme was used, the old css
    # files need to be removed and the theme profile needs to be applied.

    # acquire the current theme
    skins = getToolByName(context, 'portal_skins')
    theme = skins.getDefaultSkin()

    # find the right profile to use
    profilemap = {
        'iZug Base Theme': 'izug_basetheme',
        'Sunburst Theme': 'sunburst'
    }

    if theme not in profilemap:
        log.info("Theme %s is not supported by seantis.dir.facility" % theme)
        profile = 'default'
    else:
        profile = profilemap[theme]

    # remove all existing reservation stylesheets
    css_registry = getToolByName(context, 'portal_css')
    stylesheets = css_registry.getResourcesDict()
    ids = [i for i in stylesheets if 'resource++seantis.dir.facility.css' in i]

    map(css_registry.unregisterResource, ids)

    # reapply the chosen profile

    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile(
        'profile-seantis.dir.facility:%s' % profile
    )


def upgrade_1000_to_1001(context):
    """ Plone 4.3 uses plone.namedfile 2.0.1 which fails on all existing images
    of seantis.dir.facility. This function reapplies those images after which
    everything is fine again. This unfortunately makes Plone 4.2 incompatible.

    """

    site = getSite()

    brains = reservation_utils.portal_type_in_context(
        site, 'seantis.dir.facility.item', depth=100
    )
    brains += reservation_utils.portal_type_in_context(
        site, 'seantis.dir.facility.directory', depth=100
    )

    objects = [i.getObject() for i in brains]

    for obj in objects:
        if obj.image is None:
            continue

        obj.image = NamedImage(StringIO(obj.image.data), obj.image.contentType)


def upgrade_1001_to_1002(context):

    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(
        'profile-seantis.dir.facility:default', 'typeinfo'
    )
