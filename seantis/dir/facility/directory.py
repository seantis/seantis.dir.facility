import json
from datetime import timedelta

from five import grok
from zope.interface import alsoProvides
from plone.namedfile.field import NamedImage
from plone.autoform.interfaces import IFormFieldProvider
from plone.directives import form
from plone.uuid.interfaces import IUUID

from seantis.dir.base import directory
from seantis.dir.base import core

from seantis.dir.facility import _

from seantis.reservation import utils
from seantis.reservation import resource

class IFacilityDirectory(form.Schema):
    """Extends the seantis.dir.base.directory.IDirectory"""

    image = NamedImage(
            title=_(u'Image'),
            required=False
        )

alsoProvides(IFacilityDirectory, IFormFieldProvider)

@core.ExtendedDirectory
class FacilityDirectory(core.DirectoryMetadataBase):
    interface = IFacilityDirectory

class View(directory.View):
    grok.context(directory.IDirectory)
    grok.require('zope2.View')
    template = grok.PageTemplateFile('templates/directory.pt')

    overview_id = "seantis-overview-calendar"

    def uuidmap(self):
        """ Returns the uuids of the current items as well as the item.id that
        belongs to each uuid. 

        """
        uuids = {}
        for item in self.items:
            for resource in item.resources():
                uuid = IUUID(resource)
                uuids[uuid] = item.id
            
        return uuids

    def javascript(self):
        template = """
        <script type="text/javascript">
            if (!this.seantis) this.seantis = {};
            if (!this.seantis.overview) this.seantis.overview = {};

            this.seantis.overview.id = '#%s';
            this.seantis.overview.options = %s;
        </script>"""

        return template % (self.overview_id, self.calendar_options())

    def calendar_options(self):

        # Put the uuidmap in the json so it can be used by overview.js
        uuidmap = self.uuidmap()

        options = {}
        options['events'] = {
            'url': self.overview_url,
            'type': 'POST',
            'data': {
                'uuid': uuidmap.keys()
            },
            'className': 'seantis-overview-event'
        }
        options['uuidmap'] = uuidmap

        return json.dumps(options)

    @property
    def overview_url(self):
        return self.context.absolute_url_path() + '/overview'


class Overview(grok.View, resource.CalendarRequest):
    grok.context(directory.IDirectory)
    grok.require('zope2.View')
    grok.name('overview')

    def uuids(self):
        # The uuids are transmitted by the fullcalendar call, which seems to
        # mangle the the uuid options as follows:
        uuids = self.request.get('uuid[]', [])

        if not hasattr(uuids, '__iter__'):
            uuids = [uuids]

        return uuids

    def render(self):
        return resource.CalendarRequest.render(self)

    def events(self):
        """ Returns the events for the overview. """

        start, end = self.range
        if not all((start, end)):
            return []

        brains = [utils.get_resource_by_uuid(self.context, uid) for uid in self.uuids()]
        resources = [b.getObject() for b in brains]
        schedulers = [r.scheduler() for r in resources]

        if not schedulers:
            return []

        events = []

        # iterate through all days and aggregate the availability for each day
        for day in xrange(0, (end - start).days):

            # create an event which spans over an entire day
            event_start = start + timedelta(days=day)
            event_end = start + timedelta(days=day+1, microseconds=-1)

            uuids = []
            totalcount, totalavailability = 0, 0.0

            for sc in schedulers:
                count, availability = sc.availability(event_start, event_end)
                totalcount += count
                totalavailability += availability

                # add every resource that belongs the the current event
                if count > 0:
                    uuids.append(str(sc.uuid))

            if not totalcount:
                continue

            average = int(totalavailability / totalcount)
            title = u''
            events.append(dict(
                start=event_start.isoformat(),
                end=event_end.isoformat(),
                title=title,
                uuids=uuids,
                className=utils.event_class(average)
            ))

        return events