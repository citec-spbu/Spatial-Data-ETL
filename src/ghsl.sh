#!/bin/bash
PYTHON_VERSION="$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"

sudo pip install geopandas
my_var="Hello Again!"
echo $my_var

DIRECTORY="./cache"

# создает дирикторию, если не создана
if [ ! -d "$DIRECTORY" ]; then
    mkdir -p "$DIRECTORY"
fi

# скрипт для установки данных с Global Human Settlement Layer
sudo pip install rasterio
python3 get_ghsl.py


zipfile="./cache/ghsl_shapefile.zip"

extract_to="./cache/extract_data"

# проверка, установлена unzip
if ! [ -x "$(command -v unzip)" ]; then
  echo 'Ошибка: unzip не установлен.' >&2
  exit 1
fi

# существует ли zip-файл
if ! [ -e "$zipfile" ]; then
  echo "Ошибка: Файл $zipfile не найден." >&2
  exit 1
fi

source extract_raster_files.sh

unzip "$zipfile" -d "$extract_to"