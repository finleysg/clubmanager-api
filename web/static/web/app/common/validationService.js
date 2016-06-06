angular
    .module('club-manager')
    .factory('validationService', validationService);

validationService.$inject = [];

function validationService() {

    var _messages = {
        'minlength': 'This value is not long enough.',
        'maxlength': 'This value is too long.',
        'email': 'A properly formatted email address is required.',
        'required': 'This field is required.'
    };

    var service = {
        validate: form_validation
    };

    return service;
    

    function validation_messages(field, form, error_bin) {
        var messages = [];
        for (var e in form[field].$error) {
            if (form[field].$error[e]) {
                if (_messages[e]) {
                    messages.push(this.message[e]);
                } else {
                    messages.push('Error: ' + e)
                }
            }
        }
        var deduped_messages = [];
        angular.forEach(messages, function(el){
            if (deduped_messages.indexOf(el) === -1) deduped_messages.push(el);
        });
        if (error_bin) {
            error_bin[field] = deduped_messages;
        }
    }

    function form_validation(form, error_bin) {
        for (var field in form) {
            if (field.substr(0,1) != '$') {
                validation_messages(field, form, error_bin);
            }
        }
    }
}