def rgbint2rgbfloat(i):
    """
    Convert a rgb integer value (0-255) to a rgb float value (0.0-1.0).

    Args:
        i (int): Integer value from 0 to 255

    Returns:
        float: Float value from 0.0 to 1.0
    """
    return i / 255


def rgbfloat2rgbint(i):
    """
    Convert a rgb float value (0.0-1.0) to a rgb integer value (0-255).

    Args:
        i (int): Float value from 0.0 to 1.0

    Returns:
        int: Integer values from 0 to 255
    """
    return int(255 * i)


def toColourRGB(rgb):
    """
    Convert a tuple rgb integer values to rgb float values suitable
    with colour.Color usage.

    Args:
        rgb (tuple): Tuple of integer values.

    Returns:
        tuple: Tuple of float values.
    """
    return tuple([rgbint2rgbfloat(i) for i in rgb])


def toCssRGB(rgb):
    """
    Convert a tuple of rgb float values to rgb integer values suitable within
    a ``rgb()`` css value.

    Args:
        rgb (tuple): Tuple of float values.

    Returns:
        tuple: Tuple of integer values.
    """
    return tuple([rgbfloat2rgbint(i) for i in rgb])
