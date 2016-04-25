(function () {
    'use strict';

    angular
        .module('cm.event')
        .directive('eventCalendar', eventCalendar);

    function eventCalendar() {
        var directive = {
            restrict: 'AE',
            templateUrl: 'events/event-calendar.html',
            replace: true,
            controller: EventCalendarController,
            controllerAs: 'vm',
            bindToController: true
        };

        return directive;
    }

    EventCalendarController.$inject = ['eventService', 'calendarCache'];

    function EventCalendarController(eventService, calendarCache) {

        var vm = this;

        //data
        vm.calendar = null;
        vm.currentDay = calendarCache.currentDay.clone();

        //methods
        vm.changeMonth = changeMonth;

        loadCalendar();

        function loadCalendar() {
            calendarCache.currentDay = vm.currentDay;
            vm.monthName = vm.currentDay.format('MMMM');
            vm.year = vm.currentDay.year();
            eventService.events(vm.currentDay.year(), vm.currentDay.month()).then(function (calendar) {
                vm.calendar = calendar;
            });
        }

        function changeMonth(amount) {
            if (amount > 0) {
                vm.currentDay.add(amount, 'months');
            } else {
                vm.currentDay.subtract(Math.abs(amount), 'months');
            }
            loadCalendar();
        }
    }
})();