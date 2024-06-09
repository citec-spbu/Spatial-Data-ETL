import logging
import sys, os


def get_logger(name):
    logger = logging.Logger(name)
    handler = logging.StreamHandler(sys.stdout)
    log_format = logging.Formatter("[%(asctime)s][%(levelname)s] %(message)s")
    handler.setFormatter(log_format)
    logger.addHandler(handler)
    return logger

logger = get_logger(__name__)
CASHE_DIR = "cache"
cache_dir = CASHE_DIR
shapefile_zip_path = os.path.join(cache_dir, "ghsl_shapefile.zip")
shapefile_dir_path = os.path.join(cache_dir, "ghsl_shapefile")
ghsl_shape_url = "https://ghsl.jrc.ec.europa.eu/download/GHSL_data_54009_shapefile.zip"
ghsl_tile_url_template = "https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_POP_GLOBE_R2022A/GHS_POP_E2020_GLOBE_R2022A_54009_100/V1-0/tiles/GHS_POP_E2020_GLOBE_R2022A_54009_100_V1_0_{tile_id}.zip"
rus_pop_url = "https://rosstat.gov.ru/storage/mediabank/Tom8_tab2_VPN-2020.xlsx"
nhts_url = "https://nhts.ornl.gov/assets/2016/download/csv.zip"
BASE_DIR = '/Users/igorkopylov/Spatial-Data-ETL'

DB_NAME="geotest"
DB_USER="postgres"
DB_PSWD="postgres"
HOST="localhost"
PORT=5432


top = 81.8574
bottom = 41.1857
left = 19.6430
right = 169.05