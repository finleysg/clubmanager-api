var _user = function () {
    this.username = '';
    this.first_name = '';
    this.last_name = '';
    this.email = '';
    this.is_authenticated = false;
    this.is_staff = false;
    this.is_admin = false;
};

_user.prototype = {
    constructor: _user,
    get name() {
        if (!this.is_authenticated) {
            return 'Anonymous';
        }
        return this.first_name + ' ' + this.last_name;
    },
    isInRole: function(role) {
        var result = true;
        if (!role || role === '') {
            //no-op: allow
        }
        else if (role === 'member' && !currentUser.is_authenticated) {
            result = false;
        } else if (role === 'staff' && !currentUser.is_staff) {
            result = false;
        } else if (role === 'admin' && !currentUser.is_admin) {
            result = false;
        } else {
            //TODO: log 'unknown role ' + role;
            result = false;
        }
        return result;
    }
};

ClubManager.User = _user;