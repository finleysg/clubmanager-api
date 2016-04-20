(function () {
    'use strict';

    angular
        .module('cm.event')
        .factory('calendarService', calendarService);

    calendarService.$inject = [];

    function calendarService() {

        var service = {
            month: getMonth
        };

        return service;

        function getMonth(month, year) {
            var start = findSunday(month, year);
            return buildMonth(start);
        }

        function findSunday(month, year) {
            var start = moment([year, month, 1]),
                dow = start.day();
            while (dow > 0) {
                start.add(-1, 'd');
                dow = start.day();
            }
            return start;
        }

        function buildMonth(start) {
            var weeks = [];
            var currentMonth = moment();
            var done = false, date = start.clone(), monthIndex = date.month(), count = 0;
            while (!done) {
                weeks.push({ days: buildWeek(date.clone(), currentMonth) });
                date.add(1, 'w');
                done = count++ > 2 && monthIndex !== date.month();
                monthIndex = date.month();
            }
            return weeks;
        }

        function buildWeek(date, month) {
            var days = [];
            for (var i = 0; i < 7; i++) {
                days.push(new ClubManager.Day(date, month));
                date = date.clone();
                date.add(1, 'd');
            }
            return days;
        }
    }
})();