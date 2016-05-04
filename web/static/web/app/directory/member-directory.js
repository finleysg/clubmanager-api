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