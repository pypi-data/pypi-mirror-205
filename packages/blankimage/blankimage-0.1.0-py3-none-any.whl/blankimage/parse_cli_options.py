import argparse
from datetime import datetime
from .process_task import process_options


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "filename",
        nargs='?',
        type=str,
        default=f"IMG_{datetime.now().strftime('%Y_%m_%d_T_%H_%M_%S_%f')}",
        help="File name of the generated file. File extension is used to infer the image file type.",
    )

    parser.add_argument(
        "-s",
        "--size",
        nargs=2,
        type=int,
        default=[1080, 1080],
        help="Image dimensions",
        metavar=("HEIGHT", "WIDTH"),
    )

    parser.add_argument(
        "-c",
        "--color",
        default="#008080",
        help="Image Color in Hex format",
    )

    parser.add_argument(
        "-i",
        "--image-format",
        default="png",
        choices=['png', 'jpeg', 'gif', 'webp'],
        help="Image file format.",
    )

    # Misc

    parser.add_argument(
        "-v",
        "--version",
        action='store_true',
        help="Displays the current version",
    )

    parser.add_argument(
        "-a",
        "--about",
        action='store_true',
        help="Displays information about project",
    )

    parser.add_argument(
        "-e",
        "--example",
        action='store_true',
        help="Sample examples to get you stared",
    )

    options = parser.parse_args()
    process_options(vars(options))

    # Display generated Image Info.
    # Infer File format from extension.



