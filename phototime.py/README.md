# `phototime.py`

`phototime.py` renames all photo files in a given directory to filenames that reflect the date and time when the photo was taken. It uses [`exiftool`](https://exiftool.org/) to determine the relevant metadata of the photo files, so make sure it is installed and accessible on your system.

## Requirements

* [Python](https://www.python.org/)
* [ExifTool](https://exiftool.org/)
* [PyExifTool](https://pypi.org/project/PyExifTool/)

## Usage

`python phototime.py --help` prints the usage as follows.

```console
$ python phototime.py --help
usage: phototime.py [-h] [directory]

positional arguments:
  directory   directory with photos to rename

options:
  -h, --help  show this help message and exit
```

`python phototime.py .` renames all photo files in the current directory.

```console
$ python phototime.py .
IMG_1010.JPG
 → 20240726_103000+0900.jpg
IMG_2020.PNG
 → 20240726_113021+0900.png
IMG_2025.PNG
 → FAILED: 'NoneType' object has no attribute 'group'
IMG_3030.HEIC
 → 20240726_120430+0900.heic
```

## Limitations

* Only supports `.heic`, `.jpeg`, `.jpg`, and `.png`.
* Relies on the presence of valid date and time metadata in the photo files. Files without this metadata might not be renamed correctly or at all.
* Does not handle potential file name collisions (i.e. if two photo files have the same capture time).
