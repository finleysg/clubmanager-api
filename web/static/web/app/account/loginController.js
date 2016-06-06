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