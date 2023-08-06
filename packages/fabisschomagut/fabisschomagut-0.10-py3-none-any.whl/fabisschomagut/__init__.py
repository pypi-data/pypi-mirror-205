import re
from typing import Union, List, Tuple

colormap = {
    # X11 colour table from https://drafts.csswg.org/css-color-4/, with
    # gray/grey spelling issues fixed.  This is a superset of HTML 4.0
    # colour names used in CSS 1.
    # from https://github.com/bunkahle/PILasOPENCV
    "aliceblue": "#f0f8ff",
    "antiquewhite": "#faebd7",
    "aqua": "#00ffff",
    "aquamarine": "#7fffd4",
    "azure": "#f0ffff",
    "beige": "#f5f5dc",
    "bisque": "#ffe4c4",
    "black": "#000000",
    "blanchedalmond": "#ffebcd",
    "blue": "#0000ff",
    "blueviolet": "#8a2be2",
    "brown": "#a52a2a",
    "burlywood": "#deb887",
    "cadetblue": "#5f9ea0",
    "chartreuse": "#7fff00",
    "chocolate": "#d2691e",
    "coral": "#ff7f50",
    "cornflowerblue": "#6495ed",
    "cornsilk": "#fff8dc",
    "crimson": "#dc143c",
    "cyan": "#00ffff",
    "darkblue": "#00008b",
    "darkcyan": "#008b8b",
    "darkgoldenrod": "#b8860b",
    "darkgray": "#a9a9a9",
    "darkgrey": "#a9a9a9",
    "darkgreen": "#006400",
    "darkkhaki": "#bdb76b",
    "darkmagenta": "#8b008b",
    "darkolivegreen": "#556b2f",
    "darkorange": "#ff8c00",
    "darkorchid": "#9932cc",
    "darkred": "#8b0000",
    "darksalmon": "#e9967a",
    "darkseagreen": "#8fbc8f",
    "darkslateblue": "#483d8b",
    "darkslategray": "#2f4f4f",
    "darkslategrey": "#2f4f4f",
    "darkturquoise": "#00ced1",
    "darkviolet": "#9400d3",
    "deeppink": "#ff1493",
    "deepskyblue": "#00bfff",
    "dimgray": "#696969",
    "dimgrey": "#696969",
    "dodgerblue": "#1e90ff",
    "firebrick": "#b22222",
    "floralwhite": "#fffaf0",
    "forestgreen": "#228b22",
    "fuchsia": "#ff00ff",
    "gainsboro": "#dcdcdc",
    "ghostwhite": "#f8f8ff",
    "gold": "#ffd700",
    "goldenrod": "#daa520",
    "gray": "#808080",
    "grey": "#808080",
    "green": "#008000",
    "greenyellow": "#adff2f",
    "honeydew": "#f0fff0",
    "hotpink": "#ff69b4",
    "indianred": "#cd5c5c",
    "indigo": "#4b0082",
    "ivory": "#fffff0",
    "khaki": "#f0e68c",
    "lavender": "#e6e6fa",
    "lavenderblush": "#fff0f5",
    "lawngreen": "#7cfc00",
    "lemonchiffon": "#fffacd",
    "lightblue": "#add8e6",
    "lightcoral": "#f08080",
    "lightcyan": "#e0ffff",
    "lightgoldenrodyellow": "#fafad2",
    "lightgreen": "#90ee90",
    "lightgray": "#d3d3d3",
    "lightgrey": "#d3d3d3",
    "lightpink": "#ffb6c1",
    "lightsalmon": "#ffa07a",
    "lightseagreen": "#20b2aa",
    "lightskyblue": "#87cefa",
    "lightslategray": "#778899",
    "lightslategrey": "#778899",
    "lightsteelblue": "#b0c4de",
    "lightyellow": "#ffffe0",
    "lime": "#00ff00",
    "limegreen": "#32cd32",
    "linen": "#faf0e6",
    "magenta": "#ff00ff",
    "maroon": "#800000",
    "mediumaquamarine": "#66cdaa",
    "mediumblue": "#0000cd",
    "mediumorchid": "#ba55d3",
    "mediumpurple": "#9370db",
    "mediumseagreen": "#3cb371",
    "mediumslateblue": "#7b68ee",
    "mediumspringgreen": "#00fa9a",
    "mediumturquoise": "#48d1cc",
    "mediumvioletred": "#c71585",
    "midnightblue": "#191970",
    "mintcream": "#f5fffa",
    "mistyrose": "#ffe4e1",
    "moccasin": "#ffe4b5",
    "navajowhite": "#ffdead",
    "navy": "#000080",
    "oldlace": "#fdf5e6",
    "olive": "#808000",
    "olivedrab": "#6b8e23",
    "orange": "#ffa500",
    "orangered": "#ff4500",
    "orchid": "#da70d6",
    "palegoldenrod": "#eee8aa",
    "palegreen": "#98fb98",
    "paleturquoise": "#afeeee",
    "palevioletred": "#db7093",
    "papayawhip": "#ffefd5",
    "peachpuff": "#ffdab9",
    "peru": "#cd853f",
    "pink": "#ffc0cb",
    "plum": "#dda0dd",
    "powderblue": "#b0e0e6",
    "purple": "#800080",
    "rebeccapurple": "#663399",
    "red": "#ff0000",
    "rosybrown": "#bc8f8f",
    "royalblue": "#4169e1",
    "saddlebrown": "#8b4513",
    "salmon": "#fa8072",
    "sandybrown": "#f4a460",
    "seagreen": "#2e8b57",
    "seashell": "#fff5ee",
    "sienna": "#a0522d",
    "silver": "#c0c0c0",
    "skyblue": "#87ceeb",
    "slateblue": "#6a5acd",
    "slategray": "#708090",
    "slategrey": "#708090",
    "snow": "#fffafa",
    "springgreen": "#00ff7f",
    "steelblue": "#4682b4",
    "tan": "#d2b48c",
    "teal": "#008080",
    "thistle": "#d8bfd8",
    "tomato": "#ff6347",
    "turquoise": "#40e0d0",
    "violet": "#ee82ee",
    "wheat": "#f5deb3",
    "white": "#ffffff",
    "whitesmoke": "#f5f5f5",
    "yellow": "#ffff00",
    "yellowgreen": "#9acd32",
}


def get_all_colors_in_range(start, end):
    start = color_converter(start)
    end = color_converter(end)
    allrgbvals = []
    for s, e in zip(start, end):
        allrgbvals.append(tuple(range(s, e + 1)))
    for r in allrgbvals[0]:
        for g in allrgbvals[1]:
            for b in allrgbvals[2]:
                yield r, g, b


def color_converter(color: Union[int, str, List[int], Tuple[int]]) -> tuple:
    # adapted from https://github.com/bunkahle/PILasOPENCV
    """
    Converts a color string or integer to a tuple of RGB values.

    Args:
        color (Union[int, str, List[int], Tuple[int]]): The color to convert.

    Returns:
        Tuple[int, int, int] or Tuple[int, int, int, int]: The RGB or RGBA values as a tuple.

    Raises:
        ValueError: If the color specifier is unknown.

    """
    if isinstance(color, int):
        color = "#" + "{0:06X}".format(color)
        print(color)

    if isinstance(color, str):
        color = color.strip().lower()
        try:
            int(color, base=16)
            color = re.sub(r"^0x0*", "", color, flags=re.I)
            color = "000000" + color
            color = "#" + color[-6:]
        except Exception:
            pass

    if isinstance(color, list):
        color = tuple(color)
    if isinstance(color, tuple):
        return color
    if color in colormap:
        color = colormap[color]

        # check for known string formats
    if re.match(r"^#?[a-f0-9]{3}$", color, flags=re.IGNORECASE):
        if "#" in color:
            return (
                int(color[1] * 2, 16),
                int(color[2] * 2, 16),
                int(color[3] * 2, 16),
            )
        return (
            int(color[0] * 2, 16),
            int(color[1] * 2, 16),
            int(color[2] * 2, 16),
        )

    if re.match(r"^#?[a-f0-9]{4}$", color, flags=re.IGNORECASE):
        if "#" in color:
            return (
                int(color[1] * 2, 16),
                int(color[2] * 2, 16),
                int(color[3] * 2, 16),
                int(color[4] * 2, 16),
            )
        return (
            int(color[0] * 2, 16),
            int(color[1] * 2, 16),
            int(color[2] * 2, 16),
            int(color[3] * 2, 16),
        )

    if re.match(r"^#?[a-f0-9]{6}$", color, flags=re.IGNORECASE):
        if "#" in color:
            return (
                int(color[1:3], 16),
                int(color[3:5], 16),
                int(color[5:7], 16),
            )
        return (
            int(color[0:2], 16),
            int(color[2:4], 16),
            int(color[4:6], 16),
        )

    if re.match(r"^#?[a-f0-9]{8}$", color, flags=re.IGNORECASE):
        if "#" in color:
            return (
                int(color[1:3], 16),
                int(color[3:5], 16),
                int(color[5:7], 16),
                int(color[7:9], 16),
            )
        return (
            int(color[0:2], 16),
            int(color[2:4], 16),
            int(color[4:6], 16),
            int(color[6:8], 16),
        )

    m = re.match(
        r"rgb\(\s*(?:\d+)\s*,\s*(?:\d+)\s*,\s*(?:\d+)\s*\)$", color, flags=re.IGNORECASE
    )
    if m:
        return (int(m.group(1)), int(m.group(2)), int(m.group(3)))

    m = re.match(
        r"rgb\(\s*(?:\d+)%\s*,\s*(?:\d+)%\s*,\s*(?:\d+)%\s*\)$",
        color,
        flags=re.IGNORECASE,
    )
    if m:
        return (
            int((int(m.group(1)) * 255) / 100.0 + 0.5),
            int((int(m.group(2)) * 255) / 100.0 + 0.5),
            int((int(m.group(3)) * 255) / 100.0 + 0.5),
        )

    m = re.match(
        r"hsl\(\s*(?:\d+\.?\d*)\s*,\s*(?:\d+\.?\d*)%\s*,\s*(?:\d+\.?\d*)%\s*\)$",
        color,
        flags=re.IGNORECASE,
    )
    if m:
        from colorsys import hls_to_rgb

        rgb = hls_to_rgb(
            float(m.group(1)) / 360.0,
            float(m.group(3)) / 100.0,
            float(m.group(2)) / 100.0,
        )
        return (
            int(rgb[0] * 255 + 0.5),
            int(rgb[1] * 255 + 0.5),
            int(rgb[2] * 255 + 0.5),
        )

    m = re.match(
        r"hs[bv]\(\s*(?:\d+\.?\d*)\s*,\s*(?:\d+\.?\d*)%\s*,\s*(?:\d+\.?\d*)%\s*\)$",
        color,
        flags=re.IGNORECASE,
    )
    if m:
        from colorsys import hsv_to_rgb

        rgb = hsv_to_rgb(
            float(m.group(1)) / 360.0,
            float(m.group(2)) / 100.0,
            float(m.group(3)) / 100.0,
        )
        return (
            int(rgb[0] * 255 + 0.5),
            int(rgb[1] * 255 + 0.5),
            int(rgb[2] * 255 + 0.5),
        )

    m = re.match(
        r"rgba\(\s*(?:\d+)\s*,\s*(?:\d+)\s*,\s*(?:\d+)\s*,\s*(?:\d+)\s*\)$",
        color,
        flags=re.IGNORECASE,
    )
    if m:
        return (int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)))
    raise ValueError("unknown color specifier: %r" % color)


def to_rgb_tuple(
    color: (Union[int, str, List[int], Tuple[int]]), invert: bool = False
) -> Tuple[int, int, int]:
    """
    Converts a color value to an RGB tuple.

    Args:
        color: A color value that can be an integer, string, list or tuple of integers.
        invert: A boolean value indicating whether to invert the RGB tuple.

    Returns:
        A tuple of three integers representing the RGB values of the color.

    Raises:
        ValueError: If the color value is not valid.

    Example:

        >>> to_rgb_tuple('#FF0000')
        (255, 0, 0)
        >>> to_rgb_tuple([255, 0, 0], invert=True)
        (0, 0, 255)
    """
    cof = color_converter(color=color)[:3]
    if not invert:
        return cof
    return cof[::-1]


def to_rgba_tuple(
    color: (Union[int, str, List[int], Tuple[int]]), invert: bool = False
) -> Tuple[int, int, int, int]:
    """
    Converts a color value to a tuple of RGBA values.

    Args:
        color: A color value that can be an integer, string, list or tuple of integers.
        invert: A boolean value indicating whether to invert the RGB values.

    Returns:
        A tuple of four integers representing the RGBA values of the input color.

    Raises:
        TypeError: If the input color is not of the expected type.

    Example:
        >>> to_rgba_tuple((255, 0, 0))
        (255, 0, 0, 255)
        >>> to_rgba_tuple('#00FF00', invert=True)
        (0, 0, 255, 255)
    """
    tu = color_converter(color=color)
    if len(tu) == 3:
        tu = tu + (255,)
    if invert:
        tu = tu[:3][::-1] + (tu[-1],)
    return tu


def to_rgb_hex(
    color: (Union[int, str, List[int], Tuple[int]]),
    prefix: str = "0x",
    invert: bool = False,
) -> str:
    """
    Converts a color value to its hexadecimal representation in RGB format.

    Args:
        color: A color value that can be an integer, string, list or tuple of integers representing
            the RGB values of the color.
        prefix: A string prefix to be added to the hexadecimal representation of the color.
            Default is "0x".
        invert: A boolean flag indicating whether to invert the RGB values before converting
            to hexadecimal. Default is False.

    Returns:
        A string representing the hexadecimal representation of the color in RGB format.

    Raises:
        TypeError: If the color value is not of the expected type.

    Examples:
        >>> to_rgb_hex(255, prefix="0x")
        '0xff0000'
        >>> to_rgb_hex([0, 255, 0])
        '0x00ff00'
        >>> to_rgb_hex((0, 255, 0), prefix="#")
        '#00ff00'
    """
    co = to_rgb_tuple(color, invert=invert)
    co2 = prefix + "".join([hex(x)[2:].zfill(2) for x in co])
    return co2


def to_rgba_hex(
    color: (Union[int, str, List[int], Tuple[int]]),
    prefix: str = "0x",
    invert: bool = False,
) -> str:
    """
    Converts a color value to its hexadecimal representation in RGBA format.

    Args:
        color: A color value that can be an integer, string, list or tuple of integers representing
            the red, green, blue and alpha values of the color. If a string is provided, it must be
            in the format "#RRGGBB" or "#RRGGBBAA".
        prefix: A string that will be added as a prefix to the hexadecimal representation of the color.
            Default is "0x".
        invert: A boolean value indicating whether the color should be inverted before converting it
            to its hexadecimal representation. Default is False.

    Returns:
        A string representing the hexadecimal representation of the color in RGBA format, with the
        prefix specified in the `prefix` argument.

    Raises:
        ValueError: If the `color` argument is not a valid color value.

    Examples:
        >>> to_rgba_hex((255, 0, 0, 255))
        '0xff0000ff'
        >>> to_rgba_hex("#00FF00")
        '0x00ff00ff'

    """
    co = to_rgba_tuple(color, invert=invert)
    co2 = "".join([hex(x)[2:].zfill(2) for x in co])

    return prefix + co2


def _sub_add_colors(
    color1: (Union[int, str, List[int], Tuple[int]]),
    color2: (Union[int, str, List[int], Tuple[int]]),
    invert: bool = False,
    operation: str = "+",
) -> Tuple[int, int, int]:
    """
    This function takes two colors as input and performs addition or subtraction operation on them based on the
    'operation' parameter. The colors can be provided as integers, strings, lists or tuples. If the 'invert' parameter
    is set to True, the colors will be inverted before the operation is performed (RGB - BGR). The resulting color is returned as
    a tuple.

    :param color1: The first color to be used in the operation. Can be an integer, string, list or tuple.
    :param color2: The second color to be used in the operation. Can be an integer, string, list or tuple.
    :param invert: A boolean parameter indicating whether the colors should be inverted before the operation is performed.
    :param operation: A string parameter indicating the operation to be performed. Can be either '+' or '-'.
    :return: A tuple representing the resulting color after the operation is performed.
    """
    c1 = to_rgb_tuple(color1, invert=invert)
    c2 = to_rgb_tuple(color2, invert=invert)
    newcolor = []
    for co1, co2 in zip(c1, c2):
        if operation == "+":
            noa = co1 + co2
        else:
            noa = co1 - co2
        if noa > 255:
            newcolor.append(255)
        elif noa < 0:
            newcolor.append(0)
        else:
            newcolor.append(noa)
    return tuple(newcolor)


def add_color(
    color1: (Union[int, str, List[int], Tuple[int]]),
    color2: (Union[int, str, List[int], Tuple[int]]),
    invert: bool = False,
) -> Tuple[int, int, int]:
    """
    Adds two colors together and returns the result.

    Args:
        color1: The first color to add. This can be an integer, string, tuple, or list of integers.
        color2: The second color to add. This can be an integer, string, tuple, or list of integers.
        invert: If True, the result will be inverted. Default is False.

    Returns:
        The result of adding the two colors together - tuple

    Raises:
        TypeError: If color1 or color2 is not an integer, string, tuple, or list of integers.

    Example:
        >>> add_color((255, 0, 0), (0, 255, 0))
        (255, 255, 0)
        >>> add_color("#FF0000", "#00FF00")
        [255, 255, 0]

    """
    return _sub_add_colors(color1, color2, invert=invert, operation="+")


def subtract_color(
    color1: (Union[int, str, List[int], Tuple[int]]),
    color2: (Union[int, str, List[int], Tuple[int]]),
    invert: bool = False,
) -> Tuple[int, int, int]:
    """
    Subtract two colors and return the result.

    Args:
        color1: The first color to subtract. This can be an integer, string, tuple or list of integers representing
            the RGB values of the color.
        color2: The second color to subtract. This can be an integer, string, tuple or list of integers representing
            the RGB values of the color.
        invert: If True, the result will be inverted. Default is False.

    Returns:
        The result of subtracting the two colors as a tuple

    Raises:
        TypeError: If either color1 or color2 is not an integer, string, tuple or list of integers.
        ValueError: If either color1 or color2 does not have exactly three values representing the RGB values.
    """
    return _sub_add_colors(color1, color2, invert=invert, operation="-")


