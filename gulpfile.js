var gulp          = require('gulp');
//var concat        = require('gulp-concat');
//var uglify        = require('gulp-uglify');
//var rename        = require('gulp-rename');
//var sh            = require('shelljs');
//var replace       = require('gulp-replace');
//var fs            = require('fs');
//var inject        = require('gulp-inject');
//var seq           = require('run-sequence');


gulp.task('update-styles', function () {
    return gulp.src('bower_components/bootstrap/less/bootstrap.less')
        .pipe(less())
        .pipe(gulp.dest('bower_components/bootstrap/dist/css/'));
});

gulp.task('stage-css', function () {
    var sources = [
        'bower_components/animate.css/animate.css',
        'bower_components/material-design-iconic-font/dist/css/material-design-iconic-font.css',
        'bower_components/malihu-custom-scrollbar-plugin/jquery.mCustomScrollbar.css'
    ];
    return gulp.src(sources).pipe(gulp.dest('web/static/web/css'));
});

gulp.task('stage-js-lib', function () {
    var sources = [
        'bower_components/jquery/dist/jquery.js',
        'bower_components/angular/angular.js',
        'bower_components/lodash/dist/lodash.js',
        'bower_components/moment/moment.js',
        'bower_components/bootstrap/dist/js/bootstrap.js',
        'bower_components/malihu-custom-scrollbar-plugin/jquery.mCustomScrollbar.js'
    ];
    return gulp.src(sources).pipe(gulp.dest('web/static/web/lib'));
});

gulp.task('stage-fonts', function () {
    var sources = [
        'bower_components/bootstrap/dist/fonts/*.*',
        'bower_components/material-design-iconic-font/dist/fonts/*.*'
    ];
    return gulp.src(sources).pipe(gulp.dest('web/static/web/fonts'));
});

gulp.task('stage', ['stage-fonts', 'stage-css', 'stage-js-lib']);
