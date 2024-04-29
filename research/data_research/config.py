from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DATA_DIR = os.environ.get("DATA_DIR")
FILE_FORMAT = os.environ.get("FILE_FORMAT")
REGIONS = os.environ.get("REGIONS").split(",")
DAY_DELTA = os.environ.get("DAY_DELTA")