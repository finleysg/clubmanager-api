var _calendarDay = function (date, currentMonth) {
    this.name = date.format('dddd');
    this.shortName = date.format('ddd');
    this.day = parseInt(date.format('D'), 10);
    this.isCurrentMonth = date.month() === currentMonth.month();
    this.isToday = date.isSame(new Date(), 'day');
    this.date = date;
    this.events = [];
};

_calendarDay.prototype = {
    constructor: _calendarDay,
    hasEvents: function() {
        return this.events && this.events.length > 0;
    }//,
    //addEvent: function (event) { addEvent(this, event); }
};

ClubManager.Day = _calendarDay;
