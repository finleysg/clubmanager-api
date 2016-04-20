(function (cm) {
    'use strict';

    function findSunday(month, year) {
        var start = moment([year, month, 1]),
            dow = start.day();
        while (dow > 0) {
            start.add(-1, 'd');
            dow = start.day();
        }
        return start;
    }

    function buildMonth(start, currentMonth) {
        var weeks = [];
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
            days.push(new cm.Day(date, month));
            date = date.clone();
            date.add(1, 'd');
        }
        return days;
    }
    
    var calendar = function (month, year) {
        var sunday = findSunday(month, year);
        this.weeks = buildMonth(sunday, moment([year, month, 1]));
    };

    var updateEvent = function (event) {
        var signup_start = moment(event.signup_start);
        var signup_end = moment(event.signup_end);
        event.canRegister = moment().isBetween(signup_start, signup_end);
        event.hasResults = moment().isAfter(event.start_date);
        return event;
    };

    var addEvent = function (self, event) {
        var start = moment(event.start_date);
        self.weeks.forEach(function (week) {
            week.days.forEach(function (day) {
               if (day.date.isSame(start, 'day')) {
                   day.events.push(updateEvent(event));
               }
            });
        });
    };
    
    calendar.prototype = {
        constructor: calendar,
        addEvent: function (event) { addEvent(this, event); } 
    };
    
    cm.Calendar = calendar;
    
})(ClubManager);
