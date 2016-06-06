angular
    .module('club-manager')
    .factory('accountService', accountService);

accountService.$inject = ['$rootScope', '$q', 'accountData'];

function accountService($rootScope, $q, accountData) {

    var currentUser;

    var service = {
        login: login,
        logout: logout,
        changePassword: changePassword,
        resetPassword: resetPassword,
        user: user,
        updateProfile: updateProfile,
        verify: verify,
        confirmReset: confirmReset
    };

    return service;

    function login(username, password) {
        return accountData.login(username, password).then(function(data){
            $rootScope.$broadcast('auth.logged_in', data);
        });
    }

    function logout() {
        return accountData.logout().then(function() {
            currentUser = undefined;
            $rootScope.$broadcast('auth.logged_out');
        });
    }

    function changePassword(password1, password2) {
        return accountData.changePassword(password1, password2);
    }

    function resetPassword(email) {
        return accountData.resetPassword(email);

    }

    function user(role) {
        var promise = $q.defer();
        if (currentUser === undefined) {
            accountData.user().then(function (data) {
                currentUser = new ClubManager.User();
                angular.extend(currentUser, data);
                if (!currentUser.isInRole(role)) {
                    promise.reject('not authorized');
                }
                promise.resolve(currentUser);
            });
        }
        else {
            if (!currentUser.isInRole(role)) {
                promise.reject('not authorized');
            }
            promise.resolve(currentUser);
        }
        return promise.promise;
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
}