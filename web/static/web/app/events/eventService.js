(function () {
    'use strict';

    angular
        .module('cm.event')
        .factory('eventService', eventService);

    eventService.$inject = ['eventData'];

    function eventService(eventData) {

        var service = {
            events: getEvents,
            upcoming: getUpcomingEvents
        };

        return service;

        function getEvents(year, month) {
            return eventData.events(year, month+1).then( function(data) {
                var calendar = new ClubManager.Calendar(month, year);
                data.forEach(function (event) {
                    calendar.addEvent(event);
                });
                return calendar;
            });
        }
        
        function getUpcomingEvents() {
            return eventData.upcoming();
        }
    }
})();