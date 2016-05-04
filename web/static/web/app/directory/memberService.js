angular
    .module('club-manager')
    .factory('memberService', memberService);

memberService.$inject = ['memberData'];

function memberService(memberData) {

    var service = {
        members: getMembers,
        alphabet: getAlphabet
    };

    return service;

    function getAlphabet() {
        return ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]; 
    }
    
    function getMembers(initial) {
        return memberData.members().then( function(data) {
            var members = [];
            data.forEach(function (member) {
                if (member.last_name[0].toLowerCase() === initial.toLowerCase()) {
                    members.push(member);
                }
            });
            return members;
        });
    }
}
