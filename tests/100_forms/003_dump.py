import pytest

from django_palette.forms.dump import DumpForm


@pytest.mark.parametrize("data,is_valid", [
    # valid single element
    (
        [
            {"color":"#ffffff", "name": "white"},
        ],
        [],
    ),
    # valid multiple elements
    (
        [
            {"color":"#ffffff", "name": "white"},
            {"color":"#000000", "name": "black"},
        ],
        [],
    ),
    # missing "color" field in single element
    (
        [
            {"foo":"#ffffff", "name": "white"},
        ],
        [
            "Item #0 has no 'color' field",
        ],
    ),
    # missing "color" field in single element
    (
        [
            {"color":"#ffffff", "foo": "white"},
        ],
        [
            "Item #0 has no 'name' field",
        ],
    ),
    # invalid multiple elements
    (
        [
            {"foo":"#ffffff", "name": "white"},
            {"color":"#000000", "foo": "black"},
        ],
        [
            "Item #0 has no 'color' field",
            "Item #1 has no 'name' field",
        ],
    ),
    # multiple elements with mixed error and valid fields
    (
        [
            {"foo":"#ffffff", "name": "white"},
            {"color":"#ff0000", "name": "red"},
            {"color":"#000000", "foo": "black"},
            {"color":"#00ff00", "name": "green"},
            {"foo":"#0000ff", "bar": "blue"},
        ],
        [
            "Item #0 has no 'color' field",
            "Item #2 has no 'name' field",
            "Item #4 has no 'color' field",
            "Item #4 has no 'name' field",
        ],
    ),
])
def test_palette_structure_validation(data, is_valid):
    """
    test structure validation
    """
    f = DumpForm()
    assert f.validate_palette_structure(data) == is_valid


@pytest.mark.parametrize("data,errors", [
    # unknow fields
    (
        {"foo": "bar"},
        {
            "formats": ["This field is required."],
            "palette": ["This field is required."]
        },
    ),
    # formats is empty
    (
        {
            "palette": """[{"color":"#ffffff", "name": "white"}]""",
            "formats": [],
        },
        {
            "formats": ["This field is required."],
        },
    ),
    # both are empty
    (
        {
            "palette": "",
            "formats": [],
        },
        {
            "formats": ["This field is required."],
            "palette": ["This field is required."]
        },
    ),
    # palette is invalid JSON
    (
        {
            "palette": "nope",
            "formats": ["json"],
        },
        {
            "palette": ["Invalid JSON data."]
        },
    ),
    # given palette is empty JSON data
    (
        {
            "palette": "[]",
            "formats": ["json"],
        },
        {
            "palette": ["This field is required."]
        },
    ),
    # given palette is not a JSON list
    (
        {
            "palette": """{"yop": "glop"}""",
            "formats": ["json"],
        },
        {
            "palette": ["Palette data structure is invalid."]
        },
    ),
    # palette is given and valid JSON data but invalid expected structure
    (
        {
            "palette": """[{"foo":"#ffffff", "name": "white"}]""",
            "formats": ["json"],
        },
        {
            "palette": ["Palette data structure is invalid."]
        },
    ),
    # all given format are not valid choices
    (
        {
            "palette": """[{"color":"#ffffff", "name": "white"}]""",
            "formats": ["foo", "bar"],
        },
        {
            "formats": ["Select a valid choice. foo is not one of the available choices."],
        },
    ),
    # one of given formats is not a valid choice
    (
        {
            "palette": """[{"color":"#ffffff", "name": "white"}]""",
            "formats": ["json", "bar"],
        },
        {
            "formats": ["Select a valid choice. bar is not one of the available choices."],
        },
    ),
])
def test_validation_errors(data, errors):
    """
    check errors from validation
    """
    f = DumpForm(data)
    assert f.is_valid() == False
    assert f.errors == errors


@pytest.mark.parametrize("data", [
    # valid single element
    {
        "palette": """[{"color":"#ffffff", "name": "white"}]""",
        "formats": ["json"],
    },
    # multiple valid elements
    {
        "palette": ("""[{"color":"#ffffff", "name": "white"},"""
                    """{"color":"#000000", "name": "black"}]"""),
        "formats": ["json", "python-dict"],
    },
])
def test_validation_success(data):
    """
    validation success on valid datas
    """
    f = DumpForm(data)
    assert f.is_valid() == True


#@pytest.mark.parametrize("data", [
    ## valid single element
    #{
        #"palette": ("""[{"color":"#ffffff", "name": "white"},"""
                    #"""{"color":"#000000", "name": "black"}]"""),
        #"formats": ["json"],
    #},
#])
#def test_save(data):
    #"""
    #test validation
    #"""
    #f = DumpForm(data)
    #assert f.is_valid() == True
    #assert f.save() == None
