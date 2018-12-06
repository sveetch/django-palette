# -*- coding: utf-8 -*-
"""
Try to find all used colors through all given scss/css files or source

Require:

    pip install colorutils

"""
import os, re

from pathlib import Path

from colour import Color


class ColorFinder:
    """
    Color patterns finding in files matching some extensions.
    """
    _DEFAULT_EXTENSIONS = ['scss', 'sass', 'css']
    _REG_HEXACODE = re.compile(r'#(?:[a-fA-F0-9]{1,6})\b')
    _REG_RGB = re.compile(r'rgb[a]{0,1}\(([^)]*)\)')

    def __init__(self, extensions=None):
        self.extensions = extensions or self._DEFAULT_EXTENSIONS

    def get_files(self, path):
        """
        Recursively search for files matching enabled extension from given base
        directory.

        Args:
            path (str): A directory path where to perform recursive search.

        Returns:
            list: List of ``pathlib.Path`` objects for each finded files.
        """
        found_for_extension = []

        for ext in self.extensions:
            found = Path(path).resolve().glob('**/*.{}'.format(ext))
            found_for_extension.extend(found)

        return found_for_extension

    def find_hexacode(self, source):
        """
        Find hexadecimal codes from given source.

        Args:
            source (str): Source string where to search for codes.

        Returns:
            list: List of found codes. Every code are return in lowercase
                with doubles. Codes are in arbitrary order.
        """
        found = [item.lower() for item in self._REG_HEXACODE.findall(source)]
        return list(set(found))

    def find_rgb(self, source):
        """
        Find rgb colors from given source.

        Note:
            Currently not supported until i find how to convert 255 notation to
            float notation (required from 'colour').

            Also there is flaw since rgba can contain hexadecimal code, we should
            ensure this does not lead to duplication find with find_hexacode()
            method, basically they should be ignored since they would be
            allready finded.

        Args:
            source (str): Source string where to search for rgb[a] occurences.

        Returns:
            list: List of found values.
        """
        found = self._REG_RGB.findall(source)

        values = set([])
        for item in found:
            # Rgb with alpha, ignore alpha
            segments = [v.strip() for v in item.split(',')]

            if item.startswith('#'):
                Color(segments[0])
                values.add(segments[0])
            elif len(item) > 3:
                Color(rgb=segments[0:3])
                values.add(",".join(segments[0:3]))
            # Rgb
            elif len(item) > 2:
                Color(rgb=segments[0:3])
                values.add(",".join(segments[0:3]))
            # Hexa with alpha, ignore alpha
            elif len(item) > 1 and item.startswith('#'):
                Color(segments[0])
                values.add(segments[0])
            # Hexa
            # Everything else is assumed to be invalid

        return list(values)

    def find(self, source):
        """
        Find color values from given source.

        It is a unique wrapper around every color type finders like
        hexadecimal, rgb, etc..

        TODO:
            include find_rgb() usage when it's done

        Args:
            source (str): Source string where to search for codes.

        Returns:
            list: List of found codes. Every code are return in lowercase
                with doubles. Codes are in arbitrary order.
        """
        found = self.find_hexacode(source)

        return found

    def read_file(self, path):
        """
        Read given file to find all color occurences.

        Args:
            path (pathlib.Path): Path object to open.

        Returns:
            list: List of finded colors.
        """
        return self.find_hexacode(path.read_text())

    def search(self, path):
        """
        Search through file(s) for every colors

        Args:
            path (pathlib.Path): Path object where to search colors. Either:

                * A directory to recursively search for files ending with one
                  of ``ColorFinder.extensions``.
                * A single file (with any or no extension).

        Returns:
            list: List of finded colors.
        """
        found = set([])

        if path.is_dir():
            for pathobject in self.get_files(path):
                found.update(self.read_file(pathobject))
        elif path.is_file():
            found = set(self.read_file(path))

        return list(found)
