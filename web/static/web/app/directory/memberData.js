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
