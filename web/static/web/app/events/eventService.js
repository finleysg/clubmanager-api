angular
    .module('club-manager')
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
        var year = new Date().getFullYear();
        return eventData.events(year).then( function(data) {
            var filtered = data.filter(function (event) {
                return moment(event.start_date).year() === year &&
                    (event.event_state === 'registration' || event.event_state === 'pending');
            });
            return filtered;
        });
    }
}
