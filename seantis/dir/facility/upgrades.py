import logging
log = logging.getLogger('seantis.reservation')
from Products.CMFCore.utils import getToolByName


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