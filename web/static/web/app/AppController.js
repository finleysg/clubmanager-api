(function() {
    'use strict';

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
            if (active > 0) {
                return true;
            }
            return false;
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
})();