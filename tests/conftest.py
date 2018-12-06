"""
Some fixture methods
"""
import os
import pytest

import django_palette


class FixturesSettingsTestMixin(object):
    """Mixin containing some basic settings"""
    def __init__(self):
        # Base fixture datas directory
        self.tests_dir = 'tests'
        self.tests_path = os.path.normpath(
            os.path.join(
                os.path.abspath(os.path.dirname(django_palette.__file__)),
                '..',
                self.tests_dir,
            )
        )
        self.fixtures_dir = 'data_fixtures'
        self.fixtures_path = os.path.join(
            self.tests_path,
            self.fixtures_dir
        )

        # Some sample libraries
        self.colors_dir = 'colors'
        self.colors_path = os.path.join(self.fixtures_path, self.colors_dir)


@pytest.fixture(scope="module")
def settings():
    """Initialize and return settings (mostly paths) for fixtures (scope at module level)"""
    return FixturesSettingsTestMixin()
