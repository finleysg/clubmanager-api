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

    EventCalendarController.$inject = ['eventService'];

    function EventCalendarController(eventService) {

        var vm = this;

        //data
        vm.calendar = null;
        vm.today = moment();
        vm.month = vm.today.clone();

        //methods
        vm.changeMonth = changeMonth;

        loadCalendar();

        function loadCalendar() {
            //initialize
            vm.monthName = vm.month.format('MMMM');
            vm.year = vm.month.year();
            eventService.events(vm.month.year(), vm.month.month()).then(function (calendar) {
                vm.calendar = calendar;
            });
        }

        function changeMonth(amount) {
            if (amount > 0) {
                vm.month.add(amount, 'months');
            } else {
                vm.month.subtract(Math.abs(amount), 'months');
            }
            loadCalendar();
        }
    }
})();