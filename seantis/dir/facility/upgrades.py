import logging
log = logging.getLogger('seantis.dir.facility')

from Products.CMFCore.utils import getToolByName

from seantis.dir.facility.directory import IFacilityDirectory
from seantis.dir.facility.item import IFacilityDirectoryItem
from seantis.dir.base.upgrades import add_behavior_to_item, reset_images

profilemap = {
    'iZug Base Theme': 'izug_basetheme',
    'Sunburst Theme': 'sunburst'
}


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

    reset_images(context, (IFacilityDirectory, IFacilityDirectoryItem))


def upgrade_1001_to_1002(context):

    add_behavior_to_item(
        context, 'seantis.dir.facility', IFacilityDirectoryItem
    )


def upgrade_1002_to_1003(context):

    setup = getToolByName(context, 'portal_setup')

    # upgrade the css registry of the installed profiles
    available_profiles = [
        'profile-seantis.dir.facility:sunburst',
        'profile-seantis.dir.facility:izug_basetheme'
    ]

    upgraded = 0

    for profile in available_profiles:
        installed = setup.getProfileImportDate(profile)

        if installed:
            setup.runImportStepFromProfile(profile, 'cssregistry')
            upgraded += 1

    # if no profile was found, try to upgrade by theme
    if not upgraded:
        skins = getToolByName(context, 'portal_skins')
        theme = skins.getDefaultSkin()

        profile = profilemap.get(theme, None)

        if profile:
            profile = 'profile-seantis.dir.facility:{}'.format(profile)
            setup.runImportStepFromProfile(profile, 'cssregistry')


def upgrade_1003_to_1004(context):

    # update actions
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(
        'profile-seantis.dir.facility:default', 'typeinfo'
    )


def upgrade_1004_to_1005(context):

    # add collective.geo.behaviour
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile(
        'profile-collective.geo.behaviour:default'
    )

    add_behavior_to_item(
        context, 'seantis.dir.facility', IFacilityDirectoryItem
    )

    # update css and js
    getToolByName(context, 'portal_css').cookResources()
    getToolByName(context, 'portal_javascripts').cookResources()