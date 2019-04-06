A Django app to create a palette of named colors from given source.

Requires
********

* Python >= 3.4;
* Django>=2.0,<2.1;
* colour==0.1.5;
* whitenoise>=4.0,<5.0 (for sandbox);
* NodeJS (to customize and build frontend);


Install
*******

As a package
------------

Install package ::

    pip install django-palette

Add it to your installed Django apps in settings like this : ::

    INSTALLED_APPS = (
        ...
        'django_palette',
    )

Then load its settings from your settings file: ::

    from django_palette.settings import *

Sandbox
-------

Ensure you got recent Makefile, Python and NodeJS install, clone the repository
and go in its directory to type: ::

    make install

Once everything is done you can simply launch local server: ::

    make run

About
*****

Sandbox
-------

This is the demonstration project which you can easily install to quickly try
application. This is also the recommended way to find how to include
application into your project.

It contains some additional applications used for development so you should
focus on sandbox settings and templates.

Frontend
--------

It is cutted in two parts, the most important is the VueJS application that is
shipped in application ``static`` directory, so you can easily load it from
your templates.

Also there is the CSS part that is highly paired to the sandbox layout but you
can find its sources in the ``sass`` directory and copy what you need to start
your own layout.

Color name finding
------------------

Naming stands on color registries that contain many named color references.
Because there is a lot of possibility to name a colour and to add some
vocabulary diversity many different registries can be available to search for.

Each finded color from given source is compared to every color from registry
to calculate the nearest color (with the lowest difference between colours)
which is used for its name as a proposal. This is repeated for each available
registry.

Before performing name selection base on difference calculation, the finder
will search for an exact match on searched color against registry color.

During difference calculation there is some bonus/malus depending if searched
color is a grey shade (when every RGB values are equal).

It is worth to notice than a same name can not be used twice in a registry, so
exact match will avoid to be "stealed" from a nearest color.

