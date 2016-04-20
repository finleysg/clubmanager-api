(function () {
    'use strict';

    describe('calendar service', function () {

        var service; //our service under test

        //noinspection JSUnresolvedFunction
        beforeEach(module('cm.event'));

        //get a reference to our service
        beforeEach(inject(function ($injector) {
            service = $injector.get('calendarService');
        }));

        describe('month', function () {

            it('should return a month object', function () {
                var result = service.month(3, 2016);
                expect(result).toBeDefined();
            });
        });
    });
})();