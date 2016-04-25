/* jshint ignore:start */
var gulp          = require('gulp');
var minifyHtml    = require('gulp-minify-html');
var templateCache = require('gulp-angular-templatecache');
var jshint        = require('gulp-jshint');
//var concat        = require('gulp-concat');
//var uglify        = require('gulp-uglify');
//var rename        = require('gulp-rename');
//var sh            = require('shelljs');
//var replace       = require('gulp-replace');
//var fs            = require('fs');
//var inject        = require('gulp-inject');
//var seq           = require('run-sequence');


gulp.task('html', function () {
    return gulp.src('web/static/web/app/**/*.html')
        .pipe(minifyHtml({ empty: true }))
        .pipe(templateCache('templates.js', { module: 'club-manager', standalone: false }))
        .pipe(gulp.dest('web/static/web/app'));
});

gulp.task('lint', function () {
    return gulp.src([
        'web/static/web/app/**/*.js',
        '!web/static/web/app/templates.js'
    ]).pipe(jshint()).pipe(jshint.reporter('jshint-stylish'));
});

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
        'bower_components/angular-cookies/angular-cookies.js',
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

// gulp.task('bundle', function() {
//     return gulp.src(['www/src/**/*.js','!www/src/app.js'])
//         .pipe(concat('statracker.js'))
//         .pipe(header('\'use strict\';\n'))
//         .pipe(gulp.dest('www/dist'))
//         .pipe(rename({ extname: '.min.js' }))
//         .pipe(uglify())
//         .pipe(gulp.dest('www/dist'));
// });
//
// gulp.task('inject-src', function () {
//     var target = gulp.src('./www/index.html');
//     var sources = gulp.src([
//         './www/src/account/**/*.js',
//         './www/src/clubs/**/*.js',
//         './www/src/components/**/*.js',
//         './www/src/courses/**/*.js',
//         './www/src/data/**/*.js',
//         './www/src/config/**/*.js',
//         './www/src/rounds/**/*.js',
//         './www/src/stats/**/*.js'], {read: false, cwd: __dirname});
//     //sources.pipe(print());
//     return target.pipe(inject(sources, {relative: true, addRootSlash: false})).pipe(gulp.dest('./www'));
// });
/* jshint ignore:end */