A Django app to build a palette with named color from given source.

It's a mixin of Django for backend and Vue.js for frontend.

Explanations
============

Backend
*******

Not so much to write, Django is a robust and stable solution to build and
serve web applications.

Frontend
********

Frontend is build from webpack+babel so it can be writed with all last
Ecmascript (ES6) features and turned to compatible script for recent browsers.

Since NodeJs world is largely fragmented into many libraries there is a lot of
involved packages, see below.

About packages
--------------

vue
    The core library for Vue.js
vue-axios
    A simple tiny wrapper around Axios so it is available from a Vue
    application instance.
vue-cookie
    A library to manage cookies available from a Vue application instance.
vue-loader
    A Webpack loader for common Vue.js stuff.
vue-template-compiler
    Library to support ``*.vue`` component template, required by ``vue-loader``
    which does not install it itself.
axios
    Library for a HTTP client to perform requests with *Promise* support.
qs
    Library to stringifying data, required to send form POST with content type
    ``application/x-www-form-urlencoded``.
webpack
    Common tool to manage assets and build scripts.
@babel/core
    Core library for Babel.
@babel/cli
    Babel command line tool.
@babel/preset-env
    Preset of Babel configuration for every common options and features so we
    can start to code without to configure everything manually.
@babel/polyfill
    A set of polyfill for last Ecmascript features so we can safely use them in
    our frontend sources and still be compatible with browsers that does not
    include them yet.
babel-loader
    A Webpack loader for common Babel stuff.

