if (!this.seantis) this.seantis = {};
if (!this.seantis.overview) this.seantis.overview = {};

(function($) {
    $(document).ready(function() {
        if (_.isUndefined(seantis.overview.id))
            return;

        seantis.overview.element = $(seantis.overview.id);

        seantis.overview.items = function(uuids) {
            var uuidmap = seantis.overview.options.uuidmap;
            if (_.isEmpty(uuids) || _.isEmpty(uuidmap))
                return [];

            return _.unique(_.map(uuids, function(uuid) {
               return uuidmap[uuid]; 
            }));
        };

        seantis.overview.render = function(event, element) {
            // rendering will be a tad faster if the classes are setup later
            _.defer( function() {
                _.each(event.uuids, function(uuid) {
                    element.addClass(
                        seantis.overview.items(event.uuids).join(' ')
                    )
                });
            });
        };

        seantis.overview.mouseover = function(event) {
            var ids = '#' + seantis.overview.items(event.uuids).join(', #');
            $(ids).toggleClass('groupSelection');
            $(this).toggleClass('groupSelection');
        };

        seantis.overview.resultmouseover = function() {
            var id = $(this).attr('id');
            $('.'+id, seantis.overview.element).toggleClass('groupSelection');
        };

        $('.directoryResult').mouseenter(seantis.overview.resultmouseover);
        $('.directoryResult').mouseleave(seantis.overview.resultmouseover);
        
        var options = {
            firstDay: 1,
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