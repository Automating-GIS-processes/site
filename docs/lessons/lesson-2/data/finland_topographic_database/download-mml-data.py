#!/usr/bin/env python3

"""Download one topographic database grid cell from Maanmittauslaitos"""

import io
import pathlib
import zipfile

import requests


TOPOGRAPHIC_DATABASE_DOWNLOAD_URL = (
    "http://www.nic.funet.fi/"
    "index/geodata/mml/maastotietokanta/"
    "2020/shp/L4/L41/L4132R.shp.zip"
)
TOPOGRAPHIC_DATABASE_DIRECTORY = pathlib.Path().resolve()

with requests.get(TOPOGRAPHIC_DATABASE_DOWNLOAD_URL) as response:
    zipfile.ZipFile(
        io.BytesIO(response.content)
    ).extractall(TOPOGRAPHIC_DATABASE_DIRECTORY)

# Remove a few of the largest files (not used in the course)
large_files = [
    "r_L4132R_v.*",
    "r_L4132R_p.*",
    "l_L4132R_v.*",
    "m_L4132R_v.*",
    "k_L4132R_v.*",
]
for file in TOPOGRAPHIC_DATABASE_DIRECTORY.iterdir():
    for large_file_pattern in large_files:
        if file.match(large_file_pattern):
            file.unlink()
            break
