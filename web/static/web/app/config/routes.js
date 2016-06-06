angular
    .module('club-manager')
    .run(appRun);

/* @ngInject */
function appRun(routerHelper) {
    routerHelper.configureStates(getStates());
}

function getStates() {
    return [
        {
            state: 'home',
            config: {
                templateUrl: 'views/home.html',
                url: '/home'
            }
        },
        {
            state: 'login',
            config: {
                templateUrl: 'account/login.html',
                controller: 'LoginController as vm',
                url: '/login'
            }
        },
        {
            state: 'password-reset',
            config: {
                templateUrl: 'account/password-reset.html',
                controller: 'PasswordResetController as vm',
                url: '/password-reset'
            }
        },
        {
            state: 'password-reset-confirm',
            config: {
                templateUrl: 'account/password-reset-confirm.html',
                controller: 'PasswordResetConfirmController as vm',
                url: '/password-reset/:token/:reset-token'
            }
        },
        {
            state: 'account',
            role: 'member',
            config: {
                templateUrl: 'account/account-detail.html',
                controller: 'AccountController as vm',
                url: '/account'
            }
        },
        {
            state: 'account.password-change',
            role: 'member',
            config: {
                templateUrl: 'account/password-change.html',
                controller: 'PasswordChangeController as vm',
                url: '/password-change'
            }
        }
    ];
}