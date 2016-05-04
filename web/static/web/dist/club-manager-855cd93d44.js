(function() { 
"use strict";
var ClubManager = ClubManager || {};
angular.module('club-manager', ['ngCookies']);

angular
    .module('club-manager')
    .controller('AppController', AppController);

AppController.$inject = ['$location'];

function AppController($location) {

    var vm = this;

    vm.isActive = isActive;
    vm.isOpen = isOpen;

    function isActive(path) {
        var url = $location.absUrl();
        var active = url.indexOf(path);
        return active > 0;
    }

    function isOpen(paths) {
        var url = $location.absUrl();
        var open = false;
        paths.forEach(function (path) {
            if (url.indexOf(path) > 0) {
                open = true;
            }
        });
        return open;
    }
}

angular.module("club-manager").run(["$templateCache", function($templateCache) {$templateCache.put("directory/member-directory.html","<div class=row><div class=col-xs-1><p ng-click=vm.loadMembers(letter) class=member-menu ng-repeat=\"letter in vm.alphabet\">{{ letter }}</p></div><div class=col-xs-11><p class=member-list ng-repeat=\"member in vm.members\"><a href=\"/profile/{{ member.user_id }}/\">{{ member.first_name }} {{ member.last_name }}</a> <a href=\"mailto:{{ member.email }}\" ng-show=member.show_email>{{ member.email }}</a> <span ng-show=member.show_phone>{{ member.phone_number }}</span></p></div></div>");
$templateCache.put("events/event-calendar.html","<div id=calendar-wrap><header><div class=month-title><span ng-click=vm.changeMonth(-1)>&lt;</span>{{vm.monthName}} {{vm.year}}<span ng-click=vm.changeMonth(1)>&gt;</span></div></header><div id=calendar><ul class=weekdays><li>Sunday</li><li>Monday</li><li>Tuesday</li><li>Wednesday</li><li>Thursday</li><li>Friday</li><li>Saturday</li></ul><ul ng-repeat=\"week in vm.calendar.weeks\" class=days><li ng-repeat=\"d in week.days\" class=day ng-class=\"{\'other-month\': !d.isCurrentMonth}\"><div class=date>{{d.day}}</div><div ng-repeat=\"e in d.events\" class=event><div class=event-desc><a href=\"/event/{{ e.id }}/\">{{e.name}}</a></div></div></li></ul></div></div>");
$templateCache.put("events/upcoming-events.html","<li class=\"dropdown hidden-xs\"><a href data-toggle=dropdown class=hi-events><i class=\"zmdi zmdi-calendar\"></i></a><div class=\"dropdown-menu hi-dropdown\"><div class=\"dropdown-header bg-blue m-b-15\">UPCOMING EVENTS</div><div ng-show=\"vm.events.length === 0\" class=\"list-group lg-alt\">No events are available for registration at this time.</div><div ng-show=\"vm.events.length > 0\" ng-repeat=\"e in vm.events\" class=\"list-group lg-alt\"><a class=\"list-group-item media\" href=\"/event/{{ e.id }}/register/\"><div class=pull-left><div class=\"event-time bg-green\"><h2>{{ e.start_date }}</h2><small>{{ e.start_time }}</small></div></div><div class=media-body><div class=list-group-item-heading>{{ e.name }}</div><small class=\"list-group-item-text c-gray f-11\">{{ e.time_left }}</small></div></a></div><a class=view-more href=\"/calendar/\">View all</a></div></li>");}]);
angular
    .module('club-manager')
    .factory('host', host);

host.$inject = ['$window'];

function host($window) {

    //http://localhost/Leaderboard...
    var root = '/';
    if ($window.location.host.toLowerCase() === 'localhost') {
        root = '/';
    }

    var service = {
        get root() { return root; },
        get api() { return root + 'api/'; },
        get admin() { return root + 'admin/'; }
    };

    return service;
}

function _findSunday(month, year) {
    var start = moment([year, month, 1]),
        dow = start.day();
    while (dow > 0) {
        start.add(-1, 'd');
        dow = start.day();
    }
    return start;
}

function _buildMonth(start, currentMonth) {
    var weeks = [];
    var done = false, date = start.clone(), monthIndex = date.month(), count = 0;
    while (!done) {
        weeks.push({ days: _buildWeek(date.clone(), currentMonth) });
        date.add(1, 'w');
        done = count++ > 2 && monthIndex !== date.month();
        monthIndex = date.month();
    }
    return weeks;
}

function _buildWeek(date, month) {
    var days = [];
    for (var i = 0; i < 7; i++) {
        days.push(new ClubManager.Day(date, month));
        date = date.clone();
        date.add(1, 'd');
    }
    return days;
}

var _calendar = function (month, year) {
    var sunday = _findSunday(month, year);
    this.weeks = _buildMonth(sunday, moment([year, month, 1]));
};

var _updateEvent = function (event) {
    var signup_start = moment(event.signup_start);
    var signup_end = moment(event.signup_end);
    event.canRegister = moment().isBetween(signup_start, signup_end);
    event.hasResults = moment().isAfter(event.start_date);
    return event;
};

var _addEvent = function (self, event) {
    var start = moment(event.start_date);
    self.weeks.forEach(function (week) {
        week.days.forEach(function (day) {
           if (day.date.isSame(start, 'day')) {
               day.events.push(_updateEvent(event));
           }
        });
    });
};

_calendar.prototype = {
    constructor: _calendar,
    addEvent: function (event) { _addEvent(this, event); } 
};

ClubManager.Calendar = _calendar;

var _calendarDay = function (date, currentMonth) {
    this.name = date.format('dddd');
    this.shortName = date.format('ddd');
    this.day = parseInt(date.format('D'), 10);
    this.isCurrentMonth = date.month() === currentMonth.month();
    this.isToday = date.isSame(new Date(), 'day');
    this.date = date;
    this.events = [];
};

_calendarDay.prototype = {
    constructor: _calendarDay,
    hasEvents: function() {
        return this.events && this.events.length > 0;
    }//,
    //addEvent: function (event) { addEvent(this, event); }
};

ClubManager.Day = _calendarDay;

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

angular
    .module('club-manager')
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

    //data foo
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

angular
    .module('club-manager')
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

angular
    .module('club-manager')
    .directive('memberDirectory', memberDirectory);

function memberDirectory() {
    var directive = {
        restrict: 'AE',
        templateUrl: 'directory/member-directory.html',
        replace: true,
        controller: MemberDirectoryController,
        controllerAs: 'vm',
        bindToController: true
    };

    return directive;
}

MemberDirectoryController.$inject = ['memberService'];

function MemberDirectoryController(memberService) {

    var vm = this;

    //data
    vm.alphabet = memberService.alphabet();
    vm.members = [];

    //methods
    vm.loadMembers = loadMembers;

    function loadMembers(letter) {
        memberService.members(letter).then(function (members) {
            vm.members = members
        });
    }
}
angular
    .module('club-manager')
    .factory('memberData', memberData);

memberData.$inject = ['$http', 'host'];

function memberData($http, host) {

    var service = {
        members: getMembers
    };

    return service;

    function getMembers() {
        var url = host.api + 'members/';
        return $http.get(url, { cache: true })
            .then(getMembersComplete);
    }

    function getMembersComplete(response) {
        return response.data;
    }
}

angular
    .module('club-manager')
    .factory('memberService', memberService);

memberService.$inject = ['memberData'];

function memberService(memberData) {

    var service = {
        members: getMembers,
        alphabet: getAlphabet
    };

    return service;

    function getAlphabet() {
        return ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]; 
    }
    
    function getMembers(initial) {
        return memberData.members().then( function(data) {
            var members = [];
            data.forEach(function (member) {
                if (member.last_name[0].toLowerCase() === initial.toLowerCase()) {
                    members.push(member);
                }
            });
            return members;
        });
    }
}
})();
