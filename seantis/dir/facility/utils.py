from Products.CMFCore.utils import getToolByName


def get_resources_in_context(context):
    catalog = getToolByName(context, 'portal_catalog')
    path = '/'.join(context.getPhysicalPath())

    results = catalog(
        path={'query': path, 'depth': 1},
        portal_type='seantis.reservation.resource',
        sort_on='sortable_title'
    )

    return [r.getObject() for r in results]
