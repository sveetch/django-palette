Introduction
============

The goal is to develop "Django Palette" an application to help naming colors
from a given text source.

Given source is parsed to extract every colors and find them a name using an
algorithm which search through a manifest of named colors. An option is
available to use custom name (manual input) if needed.

Once named colors have been validated from user, dump them into many various
formats (Python list, JSON list, Sass variables, etc..);

Repository will contain a sandbox which is a Django project used to launch tests
but also ready to be used to serve Django Palette as a one page site.

Requirements
============

* Django is used to distribute everything (JSON, assets, HTML, CSS, etc..);
* Pip to install Python package in virtualenv and 'setup.cfg' to config
  (almost) everything on the Python side;
* Vue.js+VueX for frontend application;
* ES6 for frontend development;
* Never NodeJS will be used to serve anything, only building;
* .. but possibly we can use it in local development for hot reload;
* npm to install nodejs libs, webpack to build and manage assets;
* Sass to write CSS sources, no CSS per frontend component;

Strategy
========

1. Django is used for backend (the forms for validation and computations and
   dump process) and serve frontend (build base page from template and serve
   assets);
2. VueJS is used for interactive frontend to build forms, send data to
   backend and display responses;

Workflow
========

1. SourceForm accept a text source to search for colors;
2. ``SourceForm.save()`` returns a dict of finded colors with their computed
   names;
3. SourceForm view response returns JSON data from ``SourceForm.save()``;
4. Frontend use returned JSON to build Palette formset;
5. Palette formset purpose is to select available color names or type a custom
   one for each colors;
6. Then send POST request with data from frontend formset;
7. Backend formset view receive POST request with data to validate;
9. When valid, backend formset compute data to return a dict of colors (as
   key) with selected/customized name (as value);
10. Output various dump type to display (JSON, Sass, Python, etc..). It will
    probably be a JSON of output types with type as key and output as value
    (escaped) to directly include in page. Or output may be also directly
    builded from frontend.
