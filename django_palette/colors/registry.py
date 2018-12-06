# -*- coding: utf-8 -*-
import io, json

from pathlib import Path


class ColorRegistry:
    """
    Open, read and store color names maps

    Default shipped color registry is used on loading if no specific path is
    given to ``load`` method.
    """
    def __init__(self):
        datas_dirpath = Path(__file__).parent / "datas"

        self.map_path = datas_dirpath / "names.json"

        self.name_map, self.hexa_map = {}, {}

    def load(self, path=None):
        """
        Load registry and set maps

        Keyword args:
            path (pathlib.Path): Optionnal path object to open instead of
                default of from ``ColorRegistry.map_path``.
        """
        names = self.get_registry_file(path or self.map_path)

        self.name_map, self.hexa_map = self.get_registry_maps(names)

    def get_registry_file(self, path):
        """
        Open registry file from given path

        Args:
            path (pathlib.Path): Path object to open.

        Returns:
            list: List of map items from registry.
        """
        with io.open(str(path), 'r') as fp:
            registry_map = json.load(fp)

        return registry_map

    def get_registry_maps(self, items):
        """
        From registry items build maps, one indexed on name, another
        one indexed on color.

        Args:
            items (list): Registry items

        Returns:
            tuple: First item is the names map, second item is the colors map.
                Both are list object.
        """
        name_map = items
        # Reverse keys/values so map is indexed on hexa
        hexa_map = list(zip([v for k,v in items], [k for k,v in items]))

        return name_map, hexa_map
