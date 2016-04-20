(function () {
    'use strict';

    angular
        .module('cm.event')
        .factory('eventData', eventData);

    eventData.$inject = ['$http', 'host'];

    function eventData($http, host) {

        var service = {
            events: getEvents,
            upcoming: getUpcomingEvents
        };

        return service;

        function getEvents(year, month) {
            var url = host.api + 'events/';
            if (year) url = url + '?year=' + year;
            if (year && month) url = url + '&month=' + month;
            return $http.get(url, { cache: true })
                .then(getEventsComplete);
        }

        function getEventsComplete(response) {
            return response.data;
        }

        function getUpcomingEvents() {
            var url = host.api + 'upcoming-events/';
            return $http.get(url, { cache: true })
                .then(getUpcomingEventsComplete);
        }

        function getUpcomingEventsComplete(response) {
            return response.data;
        }
    }
})();