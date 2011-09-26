def get_fti(context, typename):
    types = context.getSite().portal_types

    if typename in types:
        return types[typename]
    else:
        return None

def add_behavior(fti, behavior):
    if fti:
        behaviors = list(fti.behaviors)
        if not behavior in behaviors:
            behaviors.append(behavior)
            fti.behaviors = tuple(behaviors)

def installBehavior(context):
    """Registers behaviors for seantis.dir.base.item."""

    fti = get_fti(context, 'seantis.dir.base.item')
    add_behavior(fti, 'seantis.dir.facility.item.IFacilityDirectoryItem')

    fti = get_fti(context, 'seantis.dir.base.directory')
    add_behavior(fti, 'seantis.dir.facility.directory.IFacilityDirectory')