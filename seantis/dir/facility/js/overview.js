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

        var highlight_group = function(elements, highlight) {
            elements.toggleClass('groupSelection', highlight);
        }

        seantis.overview.mouseover = function(event) {
            var ids = '#' + seantis.overview.items(event.uuids).join(', #');
            highlight_group($(ids), true);
            highlight_group($(this), true);
        };

        seantis.overview.mouseout = function(event) {
            var ids = '#' + seantis.overview.items(event.uuids).join(', #');
            highlight_group($(ids), false);
            highlight_group($(this), false);
        };

        seantis.overview.resultmouseover = function() {
            var element = $('.' + $(this).attr('id'));
            highlight_group(element, true);
        };

        seantis.overview.resultmouseout = function() {
            var element = $('.' + $(this).attr('id'));
            highlight_group(element, false);
        }

        $('.directoryResult').mouseenter(seantis.overview.resultmouseover);
        $('.directoryResult').mouseleave(seantis.overview.resultmouseout);
        
        var options = {
            firstDay: 1,
            timeFormat: 'HH:mm{ - HH:mm}',
            axisFormat: 'HH:mm{ - HH:mm}',
            columnFormat: 'ddd d.M',
            eventAfterRender: seantis.overview.render,
            eventMouseover: seantis.overview.mouseover,
            eventMouseout: seantis.overview.mouseout
        };

        $.extend(options, seantis.overview.options);
        seantis.overview.element.fullCalendar(options);
    });
})( jQuery );