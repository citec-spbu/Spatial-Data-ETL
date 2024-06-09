PYTHON_VERSION="$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"

sudo pip install subprocess-pipe psycopg2

python3 raster2sql.py
