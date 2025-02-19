from exiftool import ExifToolHelper

import argparse
import datetime
import os
import re
import sys


# The list of allowed photo extensions.
PHOTO_EXTENSIONS = [".heic", ".jpeg", ".jpg", ".png"]

# The regular expression pattern for the offset time.
OFFSET_TIME_PATTERN = r"[+\-]\d{2}:\d{2}"

# The normalization input formats for the photo time.
NORMALIZATION_INPUT_FORMATS = ["%Y:%m:%d %H:%M:%S%z"]

# The normalization output format for the photo time.
NORMALIZATION_OUTPUT_FORMAT = "%Y%m%d_%H%M%S%z"


def argument_parser():
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument(
        "directory",
        default=os.getcwd(),
        help="directory with photos to rename",
        nargs="?",
    )
    return argument_parser


def lowercase_extension(file_path):
    return os.path.splitext(file_path)[-1].lower()


def is_photo(file_path):
    return lowercase_extension(file_path) in PHOTO_EXTENSIONS


def date_time(exif):
    # The date and time the image was taken: e.g. 2022:05:08 12:00:26
    if "EXIF:DateTimeOriginal" in exif:
        return exif["EXIF:DateTimeOriginal"]

    # The date and time the file was written to the file system: e.g. 2024:09:03 15:15:57+09:00
    if "File:FileModifyDate" in exif:
        return exif["File:FileModifyDate"]

    return None


def offset_time(exif):
    # The offset time the image was taken: e.g. +09:00 or -03:00
    if "EXIF:OffsetTimeOriginal" in exif:
        return exif["EXIF:OffsetTimeOriginal"]

    # The value of `File:FileModifyDate` returned by `exiftool` always contains the offset time.
    # So we can extract it from the value as a last resort.
    if "File:FileModifyDate" in exif:
        return re.search(OFFSET_TIME_PATTERN, exif["File:FileModifyDate"]).group()

    return None


def has_offset_time(time):
    return re.search(OFFSET_TIME_PATTERN, time) is not None


def normalize(time):
    # Try to normalize `time` in various candidate formats to the designated format:
    # e.g. 2022:05:08 12:00:26+09:00 → 20220508_120026+0900
    for format in NORMALIZATION_INPUT_FORMATS:
        try:
            return datetime.datetime.strptime(time, format).strftime(
                NORMALIZATION_OUTPUT_FORMAT
            )
        except Exception:
            return None


def photo_time(file_path):
    exif = ExifToolHelper().get_metadata(file_path)[0]
    time = date_time(exif)
    if not has_offset_time(time):
        time += offset_time(exif)
    return normalize(time)


def photo_time_file_path(file_path):
    time = photo_time(file_path)
    extension = lowercase_extension(file_path)
    if time and extension:
        return os.path.join(os.path.dirname(file_path), f"{time}{extension}")
    return None


def main():
    arguments = argument_parser().parse_args()
    for file_path in os.listdir(arguments.directory):
        if is_photo(file_path):
            try:
                new_file_path = photo_time_file_path(file_path)
                os.rename(file_path, new_file_path)
                print(
                    os.path.basename(file_path),
                    "\n",
                    "→",
                    os.path.basename(new_file_path),
                )
            except Exception as e:
                print(os.path.basename(file_path), "\n", "→", f"FAILED: {e}")


if __name__ == "__main__":
    sys.exit(main())
