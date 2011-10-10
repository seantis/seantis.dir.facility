if (!this.seantis) this.seantis = {};
if (!this.seantis.overview) this.seantis.overview = {};

(function($) {
    $(document).ready(function() {
        if (! seantis.overview.id)
            return;

        seantis.overview.element = $(seantis.overview.id);

        seantis.overview.items = function(resources) {
            var resourcemap = seantis.overview.options.resourcemap;

            if (!resources.length || !resourcemap) {
                return [];
            }
 
            var item_ids = [];
            var duplicate = function(id) {
                for (var i=0; i<item_ids.length; i++) {
                    if (item_ids[i] === id) {
                        return true;
                    }
                }
                return false;
            };

            for (var i=0; i<resources.length; i++) {
                var resource = resources[i];
                var item_id = resourcemap[resource];
                if (item_id && !duplicate(item_id)) {
                    item_ids.push(resourcemap[resource]);       
                }
            }

            return item_ids;
        };

        seantis.overview.mouseover = function(event) {
            var ids = seantis.overview.items(event.resources);
            for (var i=0; i<ids.length; i++) {
                $('#' + ids[i]).toggleClass('groupSelection');
            }
            $(this).toggleClass('groupSelection');
        };

        var options = {
            timeFormat: 'HH:mm{ - HH:mm}',
            axisFormat: 'HH:mm{ - HH:mm}',
            columnFormat: 'dddd d.M',
            eventAfterRender: seantis.overview.render,
            eventMouseover: seantis.overview.mouseover,
            eventMouseout: seantis.overview.mouseover
        };

        $.extend(options, seantis.overview.options);
        seantis.overview.element.fullCalendar(options);
    });
})( jQuery );