Plan
====

1. Django is used for backend (the forms for validation and computations and
   dump process) and serve frontend (build base page from template and serve
   assets);
2. VueJS is used for interactive frontend to build forms and send data to
   backend;

Workflow
========

1. SourceForm accept a text source to search for colors;
2. SourceForm.save() returns a dict of finded colors with their computed names;
3. SourceForm view response is JSON data of return previous dict from save();
4. Frontend use given JSON to build Palette formset;
5. Palette formset purpose is to select available color names or type a custom
   one for each colors;
6. On submit frontend compute form data to build dynamic choice to inject as a
   JSON string in an hidden field
7. Then send POST request with data from frontend formset;
8. Backend formset view receive POST request with data, read the hidden field
   to pass dynamic choice to formset form;
9. Backend formset form validate data;
10. When valid, backend formset compute data to return a dict of colors (as
    key) with select/custom name (as value);
11. Output various dump type to display (JSON, Sass, Python, etc..). It will
    probably be a JSON of output types with type as key and output as value
    (escaped) to directly include in page. Or output may be also directly
    builded from frontend.
