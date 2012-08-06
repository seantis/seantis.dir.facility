from seantis.dir.base.setuphandlers import get_fti, add_behavior

def installBehavior(context):
    """Registers behaviors for seantis.dir.base.item."""

    fti = get_fti('seantis.dir.base.item')
    add_behavior(fti, 'seantis.dir.facility.item.IFacilityDirectoryItem')

    fti = get_fti('seantis.dir.base.directory')
    add_behavior(fti, 'seantis.dir.facility.directory.IFacilityDirectory')

    fti = get_fti('seantis.reservation.resource')
    add_behavior(fti, 'seantis.dir.facility.item.IFacilityFields')