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
