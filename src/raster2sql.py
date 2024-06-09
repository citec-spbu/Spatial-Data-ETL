import psycopg2
import subprocess 
import sys, os
from utils import *


database = DB_NAME
user = DB_USER
password = postgres
port = PORT

input_path = f"{BASE_DIR}/src/cache/R9_C19"

for raster in os.listdir(input_path):
    if raster.endswith(".tif"):
       name = raster.split(".tif")[0]   
       raster = os.path.join(input_path, raster)                    
       rastername = str(name)
       rasterlayer = rastername.lower()
       conn = psycopg2.connect(database=database, user=user, host=host, password=password, port=port)
       cursor = conn.cursor()
       cmds = 'raster2pgsql -s 3857 -t auto "' + raster + '" |psql'
       subprocess.call(cmds, shell=True)
       logger.info("Unpacking of ghsl data is complete")
