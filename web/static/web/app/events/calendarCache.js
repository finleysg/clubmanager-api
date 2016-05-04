angular
    .module('club-manager')
    .factory('calendarCache', calendarCache);

calendarCache.$inject = ['$cookies'];

function calendarCache($cookies) {

    console.log('calendarCache');

    var service = {
        get currentDay() { 
            var today = $cookies.get('currentDay');
            if (!today) {
                today = moment();
            }
            return moment(today);
        },
        set currentDay(value) {
            $cookies.put('currentDay', value.toString());
        }
    };

    return service;
}
