from pathlib import Path
from ril import Pixel
from .__init__ import __version__


def add_extension_to_file_name(file_name, image_format):
    current_file_extension = Path(file_name).suffix.strip().strip(".").strip()
    if len(current_file_extension) == 0:
        file_name = file_name + "." + image_format
    return file_name


def convert_hex_to_rgba(hex_color_code):
    raw_hex = hex_color_code.strip().lstrip("#")

    color_value = []
    color_mode = None

    if len(raw_hex) == 1:
        color_value = [int(raw_hex * 2, 16)] * 3
        color_mode = "RGB"
    elif len(raw_hex) == 3:
        color_value = [int(_hex * 2, 16) for _hex in raw_hex]
        color_mode = "RGB"
    elif len(raw_hex) == 4:
        color_value = [int(_hex * 2, 16) for _hex in raw_hex]
        color_mode = "RGBA"
    elif len(raw_hex) == 6:
        rgb_list = [
            raw_hex[0:2],
            raw_hex[2:4],
            raw_hex[4:6],
        ]
        color_value = [int(_hex, 16) for _hex in rgb_list]
        color_mode = "RGB"
    elif len(raw_hex) == 8:
        rgba_list = [
            raw_hex[0:2],
            raw_hex[2:4],
            raw_hex[4:6],
            raw_hex[6:8],
        ]
        color_value = [int(_hex, 16) for _hex in rgba_list]
        color_mode = "RGBA"

    return color_mode, color_value


def convert_color_to_pixel(options):
    options['color_mode'], options['color_value'] = convert_hex_to_rgba(options['color'])
    if options['color_mode'] == "RGB":
        return Pixel.from_rgb(*options['color_value'])
    elif options['color_mode'] == "RGBA":
        return Pixel.from_rgba(*options['color_value'])
    else:
        options['error'] = "Invalid Color Code"


def format_cli_options(options):

    options['filename'] = add_extension_to_file_name(options['filename'], options['image_format'])
    options['pixel'] = convert_color_to_pixel(options)
    options['height'], options['width'] = options['size']


    if options.get('error'):
        print(options['error'])
        exit(1)

    return options








# Misc Functions


def get_version():
    return """\
    blankimage version v""" + __version__



def get_about():
    return """\
    Generate Blank Image of any dimension and color with the power of rust.

    pypi            = "https://pypi.org/project/blankimage/"
    repository      = "https://github.com/insumanth/blankimage"
    documentation   = "https://insumanth.github.io/blankimage"
    """


def get_example():
    return """\

    Create Image with default options:

    $ blankimage

    # Creates a image in current directory.

    """










