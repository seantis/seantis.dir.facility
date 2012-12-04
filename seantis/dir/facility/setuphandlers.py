from seantis.dir.base.setuphandlers import get_fti, add_behavior


def install_behavior(context):
    fti = get_fti('seantis.reservation.resource')
    add_behavior(fti, 'seantis.dir.facility.item.IFacilityFields')
