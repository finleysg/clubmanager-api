// Karma configuration
// Generated on Sun Apr 17 2016 13:24:57 GMT-0500 (CDT)

module.exports = function(config) {
    'use strict';

    config.set({

    // base path that will be used to resolve all patterns (eg. files, exclude)
    basePath: '',

    // frameworks to use
    // available frameworks: https://npmjs.org/browse/keyword/karma-adapter
    frameworks: ['jasmine'],

    plugins: [
        'karma-jasmine',
        'karma-firefox-launcher'
    ],

    // list of files / patterns to load in the browser
    files: [
        'web/static/web/lib/jquery.js',
        'web/static/web/lib/angular.js',
        'web/static/web/lib/moment.js',
        'bower_components/angular-mocks/angular-mocks.js',
        'web/static/web/app/events/event.js',
        'web/static/web/app/events/**/*.js',
        'web/static/web/app/app.js',
        'web/static/web/app/config/**/*.js'
    ],

    // list of files to exclude
    exclude: [
    ],

    // preprocess matching files before serving them to the browser
    // available preprocessors: https://npmjs.org/browse/keyword/karma-preprocessor
    preprocessors: {
    },

    // test results reporter to use
    // possible values: 'dots', 'progress'
    // available reporters: https://npmjs.org/browse/keyword/karma-reporter
    reporters: ['progress'],

    // web server port
    port: 9876,

    // enable / disable colors in the output (reporters and logs)
    colors: true,

    // level of logging
    // possible values: config.LOG_DISABLE || config.LOG_ERROR || config.LOG_WARN || config.LOG_INFO || config.LOG_DEBUG
    logLevel: config.LOG_INFO,

    // enable / disable watching file and executing tests whenever any file changes
    autoWatch: false,

    // start these browsers
    // available browser launchers: https://npmjs.org/browse/keyword/karma-launcher
    browsers: ['Firefox'],

    // Continuous Integration mode
    // if true, Karma captures browsers, runs the tests and exits
    singleRun: true,

    // Concurrency level
    // how many browser should be started simultaneous
    concurrency: Infinity
    });
}