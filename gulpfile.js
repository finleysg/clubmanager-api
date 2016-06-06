/* jshint ignore:start */
var gulp          = require('gulp');
var minifyHtml    = require('gulp-minify-html');
var templateCache = require('gulp-angular-templatecache');
var jshint        = require('gulp-jshint');
var concat        = require('gulp-concat');
var wrapper       = require('gulp-wrapper');
var uglify        = require('gulp-uglify');
var rename        = require('gulp-rename');
var inject        = require('gulp-inject');
var seq           = require('gulp-sequence');
var rev           = require('gulp-rev');
var revReplace    = require('gulp-rev-replace');
var revDel        = require('rev-del');
var less          = require('gulp-less');
var path          = require('path');

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

gulp.task('less', function () {
    return gulp.src('web/static/web/less/app.less')
        // .pipe(less({
        //     paths: [ path.join(__dirname, 'less', 'includes') ]
        // }))
        .pipe(less())
        .pipe(gulp.dest('web/static/web/css'));
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
        'bower_components/jquery/dist/jquery.min.js',
        'bower_components/angular/angular.min.js',
        'bower_components/angular/angular.js',
        'bower_components/angular-ui-router/release/angular-ui-router.min.js',
        'bower_components/angular-animate/angular-animate.min.js',
        'bower_components/angular-bootstrap/ui-bootstrap.min.js',
        'bower_components/angular-bootstrap/ui-bootstrap-tpls.min.js',
        'bower_components/angular-loading-bar/build/loading-bar.min.js',
        'bower_components/angular-cookies/angular-cookies.min.js',
        'bower_components/lodash/dist/lodash.min.js',
        'bower_components/moment/min/moment.min.js',
        'bower_components/bootstrap/dist/js/bootstrap.min.js',
        'bower_components/malihu-custom-scrollbar-plugin/jquery.mCustomScrollbar.concat.min.js',
        'bower_components/bootstrap-filestyle/src/bootstrap-filestyle.min.js'
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

gulp.task('bundle-js', function() {
  return gulp.src(['web/static/web/app/app.js', 'web/static/web/app/**/*.js'])
      .pipe(concat('club-manager.js'))
      .pipe(wrapper({
          header: '(function() { \n"use strict";\nvar ClubManager = ClubManager || {};\n',
          footer: '})();\n'
      }))
      .pipe(gulp.dest('web/static/web/dist'))
      .pipe(rev())
      .pipe(gulp.dest('web/static/web/dist'))
      .pipe(rev.manifest('js-manifest.json'))
      .pipe(revDel({ dest: 'web/static/web/dist' }))
      .pipe(gulp.dest('web/static/web/dist'));
});

gulp.task('bundle-css', function() {
    return gulp.src(
        [
            'web/static/web/css/animate.css',
            'web/static/web/css/jquery.mCustomScrollbar.css',
            'web/static/web/css/material-design-iconic-font.css',
            'web/static/web/css/app.css',
            'web/static/web/css/calendar.css',
            'web/static/web/css/overrides.css'
        ])
        .pipe(concat('club-manager.css'))
        .pipe(gulp.dest('web/static/web/dist'))
        .pipe(rev())
        .pipe(gulp.dest('web/static/web/dist'))
        .pipe(rev.manifest('css-manifest.json'))
        .pipe(revDel({ dest: 'web/static/web/dist' }))
        .pipe(gulp.dest('web/static/web/dist'));
});

gulp.task('mangle', function() {
  return gulp.src(['web/static/web/dist/club-manager.js'])
      .pipe(rename({ extname: '.min.js' }))
      .pipe(uglify())
      .pipe(gulp.dest('web/static/web/dist'));
});

gulp.task('inject-js', function () {
    var options = {
        transform: function (filepath) {
            // remove /web/static/
            return '<script src="{% static \'' + filepath.substring(12) + '\' %}"></script>';
        }
    };
    var sources = gulp.src(['web/static/web/dist/club-manager.js'], {read: false, cwd: __dirname});
    return gulp
        .src('web/templates/web/base.html')
        .pipe(inject(sources, options))
        .pipe(gulp.dest('web/templates/web'));
});

gulp.task('inject-css', function () {
    var options = {
        transform: function (filepath) {
            // remove /web/static/
            return '<link rel="stylesheet" type="text/css" href="{% static \'' + filepath.substring(12) + '\' %}"/>';
        }
    };
    var sources = gulp.src(['web/static/web/dist/club-manager.css'], {read: false, cwd: __dirname});
    return gulp
        .src('web/templates/web/base.html')
        .pipe(inject(sources, options))
        .pipe(gulp.dest('web/templates/web'));
});

gulp.task('update-base', ['inject-js', 'inject-css'], function(){
    var css_manifest = gulp.src('web/static/web/dist/css-manifest.json');
    var js_manifest = gulp.src('web/static/web/dist/js-manifest.json');
    return gulp.src('web/templates/web/base.html')
        .pipe(revReplace({manifest: css_manifest}))
        .pipe(revReplace({manifest: js_manifest}))
        .pipe(gulp.dest('web/templates/web'));
});

gulp.task('build', seq('html', 'bundle-js', 'bundle-css', 'update-base'));

gulp.task('inject-dist', function () {
    var options = {
        transform: function (filepath) {
            // remove /web/static/
            return '<script src="{% static \'' + filepath.substring(12) + '\' %}"></script>';
        }
    };
    var sources = gulp.src(['web/static/web/dist/club-manager.min.js'], {read: false, cwd: __dirname});
    return gulp
        .src('web/templates/web/base.html')
        .pipe(inject(sources, options))
        .pipe(gulp.dest('web/templates/web'));
});

gulp.task('release', seq('html', 'bundle', 'mangle', 'inject-dist'));
/* jshint ignore:end */