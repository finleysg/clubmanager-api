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
