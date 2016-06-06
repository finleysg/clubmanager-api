(function() { 
"use strict";
var ClubManager = ClubManager || {};
angular.module('club-manager', [
    'ngAnimate',
    'ngCookies',
    'ui.router',
    'ui.bootstrap',
    'angular-loading-bar'
]);
angular
    .module('club-manager')
    .controller('AppController', AppController);

AppController.$inject = ['$state'];

function AppController($state) {

    var vm = this;

    // Detect Mobile Browser
    if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
        angular.element('html').addClass('ismobile');
    }

    // By default Sidebars are hidden in boxed layout and in wide layout only the right sidebar is hidden.
    vm.sidebarToggle = {
        left: false,
        right: false
    }
    // By default template has a boxed layout
    vm.layoutType = localStorage.getItem('ma-layout-status');
    // For Mainmenu Active Class
    vm.$state = $state;
    //Listview Search (Check listview pages)
    vm.listviewSearchStat = false;
    //Listview menu toggle in small screens
    vm.lvMenuStat = false;
    //Skin Switch
    vm.currentSkin = 'blue';
    vm.skinList = [
        'lightblue',
        'bluegray',
        'cyan',
        'teal',
        'green',
        'orange',
        'blue',
        'purple'
    ];

    vm.sidebarStat = sidebarStat;
    vm.lvSearch = lvSearch;
    vm.skinSwitch = skinSwitch;
    vm.clearLocalStorage = clearLocalStorage;
    vm.fullScreen = fullScreen;
    
    //Close sidebar on click
    function sidebarStat(event) {
        if (!angular.element(event.target).parent().hasClass('active')) {
            vm.sidebarToggle.left = false;
        }
    }

    function lvSearch() {
        vm.listviewSearchStat = true;
    }

    function skinSwitch(color) {
        vm.currentSkin = color;
    }

    // Clear Local Storage
    function clearLocalStorage() {

        //Get confirmation, if confirmed clear the localStorage
        swal({
            title: "Are you sure?",
            text: "All your saved localStorage values will be removed",
            type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#F44336",
            confirmButtonText: "Yes, delete it!",
            closeOnConfirm: false
        }, function(){
            localStorage.clear();
            swal("Done!", "localStorage is cleared", "success");
        });
    }

    //Fullscreen View
    function fullScreen() {
        //Launch
        function launchIntoFullscreen(element) {
            if(element.requestFullscreen) {
                element.requestFullscreen();
            } else if(element.mozRequestFullScreen) {
                element.mozRequestFullScreen();
            } else if(element.webkitRequestFullscreen) {
                element.webkitRequestFullscreen();
            } else if(element.msRequestFullscreen) {
                element.msRequestFullscreen();
            }
        }

        //Exit
        function exitFullscreen() {
            if(document.exitFullscreen) {
                document.exitFullscreen();
            } else if(document.mozCancelFullScreen) {
                document.mozCancelFullScreen();
            } else if(document.webkitExitFullscreen) {
                document.webkitExitFullscreen();
            }
        }

        if (exitFullscreen()) {
            launchIntoFullscreen(document.documentElement);
        }
        else {
            launchIntoFullscreen(document.documentElement);
        }
    }
}

angular.module("club-manager").run(["$templateCache", function($templateCache) {$templateCache.put("directory/member-directory.html","<div class=row><div class=col-xs-1><p ng-click=vm.loadMembers(letter) class=member-menu ng-repeat=\"letter in vm.alphabet\">{{ letter }}</p></div><div class=col-xs-11><p class=member-list ng-repeat=\"member in vm.members\"><a href=\"/profile/{{ member.user_id }}/\">{{ member.first_name }} {{ member.last_name }}</a> <a href=\"mailto:{{ member.email }}\" ng-show=member.show_email>{{ member.email }}</a> <span ng-show=member.show_phone>{{ member.phone_number }}</span></p></div></div>");
$templateCache.put("events/event-calendar.html","<div id=calendar-wrap><header><div class=month-title><span ng-click=vm.changeMonth(-1)>&lt;</span>{{vm.monthName}} {{vm.year}}<span ng-click=vm.changeMonth(1)>&gt;</span></div></header><div id=calendar><ul class=weekdays><li>Sunday</li><li>Monday</li><li>Tuesday</li><li>Wednesday</li><li>Thursday</li><li>Friday</li><li>Saturday</li></ul><ul ng-repeat=\"week in vm.calendar.weeks\" class=days><li ng-repeat=\"d in week.days\" class=day ng-class=\"{\'other-month\': !d.isCurrentMonth}\"><div class=date>{{d.day}}</div><div ng-repeat=\"e in d.events\" class=event><div class=event-desc><a href=\"/event/{{ e.id }}/\">{{e.name}}</a></div></div></li></ul></div></div>");
$templateCache.put("events/upcoming-events.html","<li class=\"dropdown hidden-xs\"><a href data-toggle=dropdown class=hi-events><i class=\"zmdi zmdi-calendar\"></i></a><div class=\"dropdown-menu hi-dropdown\"><div class=\"dropdown-header bg-blue m-b-15\">UPCOMING EVENTS</div><div ng-show=\"vm.events.length === 0\" class=\"list-group lg-alt\">No events are available for registration at this time.</div><div ng-show=\"vm.events.length > 0\" ng-repeat=\"e in vm.events\" class=\"list-group lg-alt\"><a class=\"list-group-item media\" href=\"/event/{{ e.id }}/register/\"><div class=pull-left><div class=\"event-time bg-green\"><h2>{{ e.start_date }}</h2><small>{{ e.start_time }}</small></div></div><div class=media-body><div class=list-group-item-heading>{{ e.name }}</div><small class=\"list-group-item-text c-gray f-11\">{{ e.time_left }}</small></div></a></div><a class=view-more href=\"/calendar/\">View all</a></div></li>");
$templateCache.put("views/home.html","<div>home</div>");
$templateCache.put("views/login.html","<div class=login-content ng-controller=\"LoginController as vm\"><form role=form name=loginForm novalidate><div class=lc-block id=l-login><div class=\"input-group m-b-30\"><div class=fg-line><input type=text class=form-control ng-model=vm.username placeholder=Username required></div></div><div class=\"input-group m-b-30\"><div class=fg-line><input type=password class=form-control ng-model=vm.password placeholder=Password required></div></div><div class=clearfix></div><div class=checkbox><label><input type=checkbox value> <i class=input-helper></i> Keep me signed in</label></div><a ng-click=vm.login(loginForm) class=\"btn btn-login btn-danger btn-float\"><i class=\"zmdi zmdi-arrow-forward\"></i></a><div class=text-danger ng-repeat=\"error in vm.errors.password\">{{error}}</div><div class=text-danger ng-repeat=\"error in vm.errors.non_field_errors\">{{error}}</div><div class=text-danger ng-if=error>{{error}}</div><div><a ui-sref=forgot-password>Forgot Password</a></div></div></form></div>");}]);
angular
    .module('club-manager')
    .factory('validationService', validationService);

validationService.$inject = [];

function validationService() {

    var _messages = {
        'minlength': 'This value is not long enough.',
        'maxlength': 'This value is too long.',
        'email': 'A properly formatted email address is required.',
        'required': 'This field is required.'
    };

    var service = {
        validate: form_validation
    };

    return service;
    

    function validation_messages(field, form, error_bin) {
        var messages = [];
        for (var e in form[field].$error) {
            if (form[field].$error[e]) {
                if (_messages[e]) {
                    messages.push(this.message[e]);
                } else {
                    messages.push('Error: ' + e)
                }
            }
        }
        var deduped_messages = [];
        angular.forEach(messages, function(el){
            if (deduped_messages.indexOf(el) === -1) deduped_messages.push(el);
        });
        if (error_bin) {
            error_bin[field] = deduped_messages;
        }
    }

    function form_validation(form, error_bin) {
        for (var field in form) {
            if (field.substr(0,1) != '$') {
                validation_messages(field, form, error_bin);
            }
        }
    }
}
angular
    .module('club-manager')
    .factory('accountData', accountData);

accountData.$inject = ['$http', '$q', '$cookies', 'host'];

function accountData($http, $q, $cookies, host) {
    
    var service = {
        login: login,
        logout: logout,
        changePassword: changePassword,
        resetPassword: resetPassword,
        profile: profile,
        updateProfile: updateProfile,
        verify: verify,
        confirmReset: confirmReset
    };

    return service;
    

    function login(username, password) {
        return request({
            'method': 'POST',
            'url': '/login/',
            'data': {
                'username': username,
                'password': password
            }
        }).then(function (data) {
            if (!host.use_session) {
                $http.defaults.headers.common.Authorization = 'Token ' + data.key;
                $cookies.put('token', data.key); //TODO: expires for remember me
            }
        });
    }
    
    function logout() {
        return request({
            'method': 'POST',
            'url': '/logout/'
        }).then(function() {
            delete $http.defaults.headers.common.Authorization;
            delete $cookies.remove('token');
        });
    }
    
    function changePassword(password1, password2) {
        return request({
            'method': 'POST',
            'url': '/password/change/',
            'data':{
                'new_password1': password1,
                'new_password2': password2
            }
        });
    }
    
    function resetPassword(email) {
        return request({
            'method': 'POST',
            'url': '/password/reset/',
            'data':{
                'email': email
            }
        });
    }
    
    function profile() {
        return request({
            'method': 'GET',
            'url': '/user/'
        });
    }
    
    function updateProfile(data) {
        return request({
            'method': 'PATCH',
            'url': '/user/',
            'data': data
        });
    }
    
    function verify(key) {
        return request({
            'method': 'POST',
            'url': '/registration/verify-email/',
            'data': {'key': key}
        });
    }
    
    function confirmReset(uid, token, password1, password2) {
        return request({
            'method': 'POST',
            'url': '/password/reset/confirm/',
            'data':{
                'uid': uid,
                'token': token,
                'new_password1':password1,
                'new_password2':password2
            }
        });
    }

    function request(args) {
        
        // Retrieve the token from the cookie, if available
        var t = $cookies.get('token');
        if (t){
            $http.defaults.headers.common.Authorization = 'Token ' + t;
        }

        args = args || {};
        
        var deferred = $q.defer(),
            url = host.rest_auth + args.url,
            method = args.method || 'GET',
            params = args.params || {},
            data = args.data || {};
        
        // Fire the request, as configured.
        var csrf = $cookies.get('csrftoken');
        $http({
            url: url,
            withCredentials: host.use_session,
            method: method.toUpperCase(),
            headers: {'X-CSRFToken': csrf},
            params: params,
            data: data
        })
            .success(angular.bind(this, function(data, status) {
                deferred.resolve(data, status);
            }))
            .error(angular.bind(this, function(data, status, headers, config) {
                console.log('error syncing with: ' + url);
                // Set request status
                if(data){
                    data.status = status;
                }
                if(status == 0) {
                    if(data == "") {
                        data = {};
                        data['status'] = 0;
                        data['non_field_errors'] = ['Could not connect. Please try again.'];
                    }
                    // or if the data is null, then there was a timeout.
                    if(data == null){
                        // Inject a non field error alerting the user
                        // that there's been a timeout error.
                        data = {};
                        data['status'] = 0;
                        data['non_field_errors'] = ['Server timed out. Please try again.'];
                    }
                }
                deferred.reject(data, status, headers, config);
            }));
        
        return deferred.promise;
    }
}
angular
    .module('club-manager')
    .factory('accountService', accountService);

accountService.$inject = ['$rootScope', 'accountData'];

function accountService($rootScope, accountData) {

    var authenticated = false;

    var service = {
        login: login,
        logout: logout,
        changePassword: changePassword,
        resetPassword: resetPassword,
        profile: profile,
        updateProfile: updateProfile,
        verify: verify,
        confirmReset: confirmReset,
        status: authenticationStatus
    };

    return service;

    function login(username, password) {
        return accountData.login(username, password).then(function(data){
            authenticated = true;
            $rootScope.$broadcast('auth.logged_in', data);
        });
    }

    function logout() {
        return accountData.logout().then(function() {
            authenticated = false;
            $rootScope.$broadcast('auth.logged_out');
        });
    }

    function changePassword(password1, password2) {
        return accountData.changePassword(password1, password2);
    }

    function resetPassword(email) {
        return accountData.resetPassword(email);

    }

    function profile() {
        return accountData.profile();
    }

    function updateProfile(data) {
        return accountData.updateProfile(data);
    }

    function verify(key) {
        return accountData.verify(key);
    }

    function confirmReset(uid, token, password1, password2) {
        return accountData.confirmReset(uid, token, password1, password2);
    }

    function authenticationStatus(restrict, force) {
        // Set restrict to true to reject the promise if not logged in
        // Set to false or omit to resolve when status is known
        // Set force to true to ignore stored value and query API
        restrict = restrict || false;
        force = force || false;
        
        if(this.authPromise == null || force){
            this.authPromise = accountData.profile();
        }
        var da = this;
        var getAuthStatus = $q.defer();
        if(this.authenticated != null && !force){
            // We have a stored value which means we can pass it back right away.
            if (this.authenticated == false && restrict){
                getAuthStatus.reject('User is not logged in.');
            } else {
                getAuthStatus.resolve();
            }
        } else {
            // There isn't a stored value, or we're forcing a request back to
            // the API to get the authentication status.
            this.authPromise.then(function(){
                da.authenticated = true;
                getAuthStatus.resolve();
            }, function() {
                da.authenticated = false;
                if(restrict){
                    getAuthStatus.reject('User is not logged in.');
                }else{
                    getAuthStatus.resolve();
                }
            });
        }
        return getAuthStatus.promise;
    }
}
angular
    .module('club-manager')
    .controller('LoginController', LoginController);

LoginController.$inject = ['$state', 'accountService', 'validationService'];

function LoginController($state, accountService, validationService) {

    var vm = this;

    vm.username = '';
    vm.password = '';
    vm.complete = false;
    vm.errors = [];
    
    vm.login = login;

    function login(formData){
        vm.errors = [];
        validationService.validate(formData, vm.errors);
        if (!formData.$invalid) {
            accountService.login(vm.username, vm.password)
                .then(function() {
                    $state.go('home');
                    //$location.path("/");
                }, function(data) {
                    vm.errors = data;
                });
        }
    }
}
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
        get rest_auth() { return root + 'rest-auth'; },
        get admin() { return root + 'admin/'; },
        get use_session() { return false; }
    };

    return service;
}

angular
    .module('club-manager')
    .config(function ($stateProvider, $urlRouterProvider, $locationProvider) {

        $locationProvider.html5Mode(true);
        $urlRouterProvider.otherwise("/home");

        $stateProvider

            .state('home', {
                url: '/home',
                templateUrl: 'views/home.html'
            })
            .state('login', {
                url: '/login',
                templateUrl: 'views/login.html'
            })
});
angular
    .module('club-manager')
    .factory('userData', userData);

userData.$inject = ['$http', 'host'];

function userData($http, host) {

    var service = {
        user: getUser
    };

    return service;

    function getUser() {
        var url = host.api + 'events/';
        if (year) url = url + '?year=' + year;
        if (year && month) url = url + '&month=' + month;
        return $http.get(url, { cache: true })
            .then(getUserComplete);
    }

    function getUserComplete(response) {
        return response.data;
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

    // =========================================================================
    // MALIHU SCROLL
    // =========================================================================
    
    //On Custom Class
    .directive('cOverflow', ['scrollService', function(scrollService){
        return {
            restrict: 'C',
            link: function(scope, element) {

                if (!$('html').hasClass('ismobile')) {
                    scrollService.malihuScroll(element, 'minimal-dark', 'y');
                }
            }
        }
    }]);

angular
    .module('club-manager')
    .directive('changeLayout', function(){

        return {
            restrict: 'A',
            scope: {
                changeLayout: '='
            },

            link: function(scope, element) {

                //Default State
                if(scope.changeLayout === '1') {
                    element.prop('checked', true);
                }

                //Change State
                element.on('change', function(){
                    if(element.is(':checked')) {
                        localStorage.setItem('ma-layout-status', 1);
                        scope.$apply(function(){
                            scope.changeLayout = '1';
                        })
                    }
                    else {
                        localStorage.setItem('ma-layout-status', 0);
                        scope.$apply(function(){
                            scope.changeLayout = '0';
                        })
                    }
                })
            }
        }
    });
angular
    .module('club-manager')
    
    // =========================================================================
    // Malihu Scroll - Custom Scroll bars
    // =========================================================================
    .service('scrollService', function() {
        var ss = {};
        ss.malihuScroll = function scrollBar(selector, theme, mousewheelaxis) {
            $(selector).mCustomScrollbar({
                theme: theme,
                scrollInertia: 100,
                axis:'yx',
                mouseWheel: {
                    enable: true,
                    axis: mousewheelaxis,
                    preventDefault: true
                }
            });
        }
    
        return ss;
    });
angular
    .module('club-manager')
        
    // =========================================================================
    // MAINMENU COLLAPSE
    // =========================================================================

    .directive('toggleSidebar', function(){

        return {
            restrict: 'A',
            scope: {
                modelLeft: '=',
                modelRight: '='
            },

            link: function(scope, element, attr) {
                element.on('click', function(){

                    if (element.data('target') === 'mainmenu') {
                        if (scope.modelLeft === false) {
                            scope.$apply(function(){
                                scope.modelLeft = true;
                            })
                        }
                        else {
                            scope.$apply(function(){
                                scope.modelLeft = false;
                            })
                        }
                    }

                    if (element.data('target') === 'chat') {
                        if (scope.modelRight === false) {
                            scope.$apply(function(){
                                scope.modelRight = true;
                            })
                        }
                        else {
                            scope.$apply(function(){
                                scope.modelRight = false;
                            })
                        }

                    }
                })
            }
        }

    })

    // =========================================================================
    // SUBMENU TOGGLE
    // =========================================================================

    .directive('toggleSubmenu', function(){

        return {
            restrict: 'A',
            link: function(scope, element, attrs) {
                element.click(function(){
                    element.next().slideToggle(200);
                    element.parent().toggleClass('toggled');
                });
            }
        }
    })
        
    // =========================================================================
    // STOP PROPAGATION
    // =========================================================================

    .directive('stopPropagate', function(){
        return {
            restrict: 'C',
            link: function(scope, element) {
                element.on('click', function(event){
                    event.stopPropagation();
                });
            }
        }
    })

    .directive('aPrevent', function(){
        return {
            restrict: 'C',
            link: function(scope, element) {
                element.on('click', function(event){
                    event.preventDefault();
                });
            }
        }
    });})();
