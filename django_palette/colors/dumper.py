# -*- coding: utf-8 -*-
import json


class ColorDump:
    """
    Provide some method to dump ``colors.naming.ColorNames`` results as JSON
    or Sass.
    """
    def as_json(self, datas, fp=None):
        """
        Dump given datas as JSON in a file or as a string

        Args:
            datas (object): Any object suitable to be encoded to JSON.

        Keyword args:
            fp (file object): Optionnal fileobject where to write JSON.

        Returns:
            string: Either JSON data as a string if no fileobject was given
                or fileobject filename.
        """
        if fp:
            json.dump(datas, fp=fp, indent=4)
            return fp.name
        else:
            return json.dumps(datas, indent=4)
