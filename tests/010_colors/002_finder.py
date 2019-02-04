# -*- coding: utf-8 -*-
import os

from pathlib import Path

import pytest

from colour import Color

from django_palette.colors.finder import ColorFinder



@pytest.mark.parametrize("extensions,expected", [
    (
        None,
        [
            'sample-3.scss',
            'sample-2.scss',
            'sample-1.scss',
            'sub_1/subfile.scss',
            'sample-4.sass',
            'sample-5.css',
            'sub_1/sub_1-1/subsubfile.css',
        ]
    ),
    (
        ['scss'],
        [
            'sample-3.scss',
            'sample-2.scss',
            'sample-1.scss',
            'sub_1/subfile.scss',
        ]
    ),
    (
        ['sass'],
        [
            'sample-4.sass',
        ]
    ),
    (
        ['css'],
        [
            'sample-5.css',
            'sub_1/sub_1-1/subsubfile.css',
        ]
    ),
    (
        ['txt'],
        [
            'dummy.txt',
        ]
    ),
    (
        ['nope'],
        []
    ),
])
def test_get_files(testsettings, extensions, expected):
    """Search for colors in file"""
    basedir = testsettings.colors_path

    finder = ColorFinder(extensions=extensions)
    found = finder.get_files(basedir)

    relative_found = [str(item.relative_to(basedir)) for item in found]

    assert sorted(relative_found) == sorted(expected)


@pytest.mark.parametrize("source,expected", [
    (
        "nothing",
        []
    ),
    (
        ("// Not a color\n"
         "#maze"),
        []
    ),
    (
        ("// Invalid hexa\n"
         "color: ffffff;"),
        []
    ),
    (
        "#000",
        ["#000"]
    ),
    (
        "#FFF000",
        ["#fff000"]
    ),
    (
        "#fff000",
        ["#fff000"]
    ),
    (
        ("// Single comment\n"
         ".red{color: #ff0000}"),
        ["#ff0000"]
    ),
    (
        ("// Commented color\n"
         "// #ff0000"),
        ["#ff0000"]
    ),
    (
        ("color: rgba(#ff0000, 0.4);"),
        ["#ff0000"]
    ),
    (
        ("// Single comment\n"
         ".red{color: #ff0000}\n"
         ".blue{color: #0000ff;}"),
        ["#ff0000", "#0000ff"]
    ),
    (
        ("$var: #f0f0f0 #dedede #ff0000;"),
        ["#f0f0f0", "#dedede", "#ff0000"]
    ),
])
def test_find_hexacode(source, expected):
    """Hexadecimal codes finding"""
    finder = ColorFinder()
    found = finder.find_hexacode(source)

    assert sorted(found) == sorted(expected)


# rgb[a] is currently not supported
#@pytest.mark.parametrize("source,expected", [
    #(
        #"nothing",
        #[]
    #),
    #(
        #("color: rgba(255, 0, 0);"),
        #["255, 0, 0"]
    #),
    #(
        #("color: rgba(#255, 0, 0);"),
        #["#255, 0, 0"]
    #),
    #(
        #("color: rgba(#255, 0);"),
        #["#255"]
    #),
    #(
        #("color: rgba(#ff0000, 0.4);"),
        #["#ff0000"]
    #),
    #(
        #("color: rgb(255, 0, 0);"
         #"color: rgb(0, 255, 0);"),
        #["0, 255, 0", "255, 0, 0"]
    #),
#])
#def test_find_rgb(source, expected):
    #"""rgb[a] finding"""
    #finder = ColorFinder()
    #found = finder.find_rgb(source)

    #assert sorted(found) == sorted(expected)


@pytest.mark.parametrize("filepath,expected", [
    (
        "sample-1.scss",
        ['#4c4c92', '#6676a2', '#ff8702']
    ),
    (
        "sample-2.scss",
        []
    ),
    (
        "sample-3.scss",
        ['#253a79', '#1a2955', '#fafafa', '#ff8702']
    ),
    (
        "sample-4.sass",
        ['#00ff00']
    ),
    (
        "sample-5.css",
        ['#222']
    ),
])
def test_read_file(testsettings, filepath, expected):
    """Open and read file"""
    basedir = testsettings.colors_path

    path = basedir / Path(filepath)

    finder = ColorFinder()
    found = finder.read_file(path)

    assert sorted(found) == sorted(expected)


@pytest.mark.parametrize("dirpath,extensions,expected", [
    (
        ".",
        None,
        ['#222', '#b29e6b', '#253a79', '#fafafa', '#1a2955', '#6676a2',
         '#00ff00', '#8461a1', '#ff8702', '#4c4c92']
    ),
    (
        "empty",
        None,
        []
    ),
    (
        "sub_1",
        None,
        ['#b29e6b', '#8461a1']
    ),
    (
        ".",
        ['css', 'sass'],
        ['#222', '#8461a1', '#00ff00']
    ),
])
def test_search_recursive_dir(testsettings, dirpath, extensions, expected):
    """Search color through files from dir"""
    basedir = testsettings.colors_path

    path = basedir / Path(dirpath)

    finder = ColorFinder(extensions=extensions)
    found = finder.search(path)

    assert sorted(found) == sorted(expected)


@pytest.mark.parametrize("filepath,expected", [
    (
        "sample-1.scss",
        ['#ff8702', '#6676a2', '#4c4c92']
    ),
    (
        "dummy.txt",
        ["#ff0000"]
    ),
    (
        "empty/.keep",
        []
    ),
])
def test_search_from_file(testsettings, filepath, expected):
    """Search color through a single file"""
    basedir = testsettings.colors_path

    path = basedir / Path(filepath)

    finder = ColorFinder()
    found = finder.search(path)

    assert sorted(found) == sorted(expected)

