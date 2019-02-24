import pytest
import json

from django.forms import formset_factory

from tests.utils import assert_and_parse_html

from django_palette.forms.palette import (formset_data_helper,
                                          PaletteItemFormSet,
                                          PaletteItemForm)


@pytest.mark.parametrize("data,options,expected", [
    # single item with single choice, no fields
    (
        {
            "#f0f0f0": [("gray94", "#f0f0f0")],
        },
        {"fields": False, "initials": False},
        {
            "form-TOTAL_FORMS": 1,
            "form-INITIAL_FORMS": 1,
            "form-MAX_NUM_FORMS": "",
        },
    ),
    # single item with single choice, no initials
    (
        {
            "#f0f0f0": [("gray94", "#f0f0f0")],
        },
        {"fields": True, "initials": False},
        {
            "form-TOTAL_FORMS": 1,
            "form-INITIAL_FORMS": 1,
            "form-MAX_NUM_FORMS": "",
            "form-0-color": "",
            "form-0-name": "",
        },
    ),
    # single item with single choice
    (
        {
            "#f0f0f0": [("gray94", "#f0f0f0")],
        },
        {"fields": True, "initials": True},
        {
            "form-TOTAL_FORMS": 1,
            "form-INITIAL_FORMS": 1,
            "form-MAX_NUM_FORMS": "",
            "form-0-color": "#f0f0f0",
            "form-0-name": "gray94",
        },
    ),
    # multiple item with single choice
    (
        {
            "#000000": [("black", "#000000")],
            "#f0f0f0": [("gray94", "#f0f0f0")],
            "#ff0000": [("red1", "#ff0000")],
        },
        {"fields": True, "initials": True},
        {
            "form-TOTAL_FORMS": 3,
            "form-INITIAL_FORMS": 3,
            "form-MAX_NUM_FORMS": "",
            "form-0-color": "#000000",
            "form-0-name": "black",
            "form-1-color": "#f0f0f0",
            "form-1-name": "gray94",
            "form-2-color": "#ff0000",
            "form-2-name": "red1",
        },
    ),
    # multiple item with multiple choice
    (
        {
            "#000000": [("black", "#000000")],
            "#f0f0f0": [
                ("gray94", "#f0f0f0"),
                ("grey2", "#f0f0f0"),
            ],
            "#ff0000": [
                ("red1", "#ff0000"),
                ("firebrick0", "#ff0000"),
            ],
        },
        {"fields": True, "initials": True},
        {
            "form-TOTAL_FORMS": 3,
            "form-INITIAL_FORMS": 3,
            "form-MAX_NUM_FORMS": "",
            "form-0-color": "#000000",
            "form-0-name": "black",
            "form-1-color": "#f0f0f0",
            "form-1-name": "gray94",
            "form-2-color": "#ff0000",
            "form-2-name": "red1",
        },
    ),
])
def test_formset_data_helper(data, options, expected):
    assert formset_data_helper(data, **options) == expected


def test_formset_build():
    """
    Build formset with some initial and check returned HTML is ok
    """
    # Initial data to add forms
    initial = [
        {
            "color": "#000000",
            "name": "black",
        },
        {
            "color": "#ffffff",
            "name": "white",
        },
    ]

    # Order of expected form HTML must follow the "initial" items order to
    # correctly be checked against the right form
    # Expected HTML include some indentation to be more human readable but
    # are not mandatory
    expected_forms = [
        (
            """<p>"""
            """  <label for="id_form-0-color">Color:</label>"""
            """  <input type="text" name="form-0-color" value="#000000" id="id_form-0-color" />"""
            """</p>"""
            """<p>"""
            """  <label for="id_form-0-name">Name:</label>"""
            """  <input type="text" name="form-0-name" value="black" maxlength="50" id="id_form-0-name" minlength="3" />"""
            """</p>"""
        ),
        (
            """<p>"""
            """  <label for="id_form-1-color">Color:</label>"""
            """  <input type="text" name="form-1-color" value="#ffffff" id="id_form-1-color" />"""
            """</p>"""
            """<p>"""
            """  <label for="id_form-1-name">Name:</label>"""
            """  <input type="text" name="form-1-name" value="white" maxlength="50" id="id_form-1-name" minlength="3" />"""
            """</p>"""
        ),
    ]

    # Create formset factory without extra form
    factory = formset_factory(
        PaletteItemForm,
        extra=0,
    )

    # Build formset according to given initial data and dynamic choices
    formset = factory(initial=initial)

    for i, form in enumerate(formset):
        expected_html = expected_forms[i]
        assert assert_and_parse_html(form.as_p()) == assert_and_parse_html(expected_html)


@pytest.mark.parametrize("data,is_valid,errors", [
    # no errors, everything is fine, note we use color name instead of hex
    # code, this is fine also
    (
        {
            "form-TOTAL_FORMS": "2",
            "form-INITIAL_FORMS": "2",
            "form-MAX_NUM_FORMS": "",
            "form-0-color": "white",
            "form-0-name": "dummy",
            "form-1-color": "black",
            "form-1-name": "foo",
        },
        True,
        [
            {},
            {}
        ],
    ),
    # no errors, everything is fine
    (
        {
            "form-TOTAL_FORMS": "2",
            "form-INITIAL_FORMS": "2",
            "form-MAX_NUM_FORMS": "",
            "form-0-color": "#FFFFFF",
            "form-0-name": "white",
            "form-1-color": "#000",
            "form-1-name": "black",
        },
        True,
        [
            {},
            {}
        ],
    ),
    # second form fields are empty
    (
        {
            "form-TOTAL_FORMS": "2",
            "form-INITIAL_FORMS": "2",
            "form-MAX_NUM_FORMS": "",
            "form-0-color": "dummy",
            "form-0-name": "fake",
            "form-1-color": "",
            "form-1-name": "",
        },
        False,
        [
            {},
            {
                "name": ["This field is required."],
                "color": ["This field is required."],
            }
        ],
    ),
    # rgb(a) notation is not supported
    (
        {
            "form-TOTAL_FORMS": "2",
            "form-INITIAL_FORMS": "2",
            "form-MAX_NUM_FORMS": "",
            "form-0-color": "#FFFFFF",
            "form-0-name": "white",
            "form-1-color": "rgb(0, 0, 0)",
            "form-1-name": "black",
        },
        False,
        [
            {},
            {
                "color": ["RGB(A) values are not supported"],
            }
        ],
    ),
    # Wrong hex color codes
    (
        {
            "form-TOTAL_FORMS": "3",
            "form-INITIAL_FORMS": "3",
            "form-MAX_NUM_FORMS": "",
            "form-0-color": "#ff",
            "form-0-name": "foo",
            "form-1-color": "##000000",
            "form-1-name": "bar",
            "form-2-color": "#f0f0z0",
            "form-2-name": "ping",
        },
        False,
        [
            {
                "color": ["Invalid Hexadecimal code"],
            },
            {
                "color": ["Invalid Hexadecimal code"],
            },
            {
                "color": ["Invalid Hexadecimal code"],
            },
        ],
    ),
    # Both valid and invalid names
    (
        {
            "form-TOTAL_FORMS": "4",
            "form-INITIAL_FORMS": "4",
            "form-MAX_NUM_FORMS": "",
            "form-0-color": "#ffffff",
            "form-0-name": "foo bar",
            "form-1-color": "#000000",
            "form-1-name": "foo-bar",
            "form-2-color": "#f0f0f0",
            "form-2-name": "-foobar",
            "form-3-color": "#f0f0f0",
            "form-3-name": "_foobar",
        },
        False,
        [
            {
                "name": ["Invalid name"],
            },
            {},
            {
                "name": ["Invalid name"],
            },
            {
                "name": ["Invalid name"],
            },
        ],
    ),
])
def test_formset_field_errors(data, is_valid, errors):
    """
    Check against various errors on formset form fields
    """
    factory = formset_factory(
        PaletteItemForm,
        extra=0,
        formset=PaletteItemFormSet,
    )

    formset = factory(data)

    assert formset.is_valid() == is_valid
    assert formset.errors == errors


@pytest.mark.parametrize("data,expected_palette", [
    (
        {
            "form-TOTAL_FORMS": "3",
            "form-INITIAL_FORMS": "3",
            "form-MAX_NUM_FORMS": "",
            "form-0-color": "#FFF",
            "form-0-name": "white",
            "form-1-color": "Yellow",
            "form-1-name": "Yellow",
            "form-2-color": "#404040",
            "form-2-name": "gray25",
        },
        [
            {
                "color": "#fff",
                "name": "white"
            },
            {
                "color": "yellow",
                "name": "yellow"
            },
            {
                "color": "#404040",
                "name": "gray25"
            },
        ],
    ),
])
def test_results(data, expected_palette):
    factory = formset_factory(
        PaletteItemForm,
        extra=0,
        formset=PaletteItemFormSet,
    )

    formset = factory(data)

    assert formset.is_valid() == True

    results = formset.save()

    assert (len(results["dump_formats"]) > 0) == True
    assert expected_palette == results["palette"]
