angular
    .module('club-manager')
    .directive('upcomingEvents', upcomingEvents);

function upcomingEvents() {
    var directive = {
        restrict: 'AE',
        templateUrl: 'events/upcoming-events.html',
        replace: true,
        controller: UpcomingEventsController,
        controllerAs: 'vm',
        bindToController: true
    };

    return directive;
}

UpcomingEventsController.$inject = ['eventService'];

function UpcomingEventsController(eventService) {

    var vm = this;

    //data
    vm.events = [];
    
    activate();

    function activate() {
        eventService.upcoming().then(function (events) {
            vm.events = events.map(function (e) {
                var start_date = moment(e.start_date).format('MMM D');
                var start_time = moment(e.start_time, 'hh:mm').format('h:mm A');
                var time_left = timeLeft(e);
                return {
                    'id': e.id,
                    'url': e.url,
                    'name': e.name,
                    'start_date': start_date,
                    'start_time': start_time,
                    'time_left': time_left
                };
            });
        });
    }

    function timeLeft(event) {
        var today = moment();
        var end_date = moment(event.signup_end);
        var days = end_date.diff(today, 'days');
        if (days > 0) {
            return days + ' days left to sign up';
        } 
        var hours = end_date.diff(today, 'hours');
        if (hours > 0) {
            return hours + ' hours left to sign up';
        }
        return 'Signup window closed at ' + end_date.format('h:mm A');
    }
}
