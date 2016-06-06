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
