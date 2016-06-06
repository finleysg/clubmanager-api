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
        user: user,
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
    
    function user() {
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