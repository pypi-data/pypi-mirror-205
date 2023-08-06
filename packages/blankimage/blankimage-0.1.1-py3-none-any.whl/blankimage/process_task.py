from ril import Image
from .format_options import get_about, get_example, get_version, format_cli_options



def generate_image(options):
    try:
        Image.new(
            width=options['width'],
            height=options['height'],
            fill=options['pixel'],
        ).save(
            path=options['filename'],
            encoding=options['image_format'],
        )
    except ValueError as val_err:
        print("**** ValueError **** " + str(val_err))
    except RuntimeError as run_err:
        print("**** RuntimeError ****" + str(run_err))
    except:
        print("**** Exception ****")
    else:
        print("Image " + options['filename'] + "Generated Successfully")


def process_options(options):
    # Format Options

    display_info = []
    if options['version']:
        display_info.append(get_version())
    elif options['about']:
        display_info.append(get_version())
        display_info.append(get_about())
    elif options['example']:
        display_info.append(get_example())

    if display_info:
        for text in display_info:
            print(text)
        exit(0)


    # Validate Info
    formatted_options = format_cli_options(options)

    # Generate Image
    generate_image(formatted_options)
