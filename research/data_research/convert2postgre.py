from pydriosm.ios import PostgresOSM
from pydriosm.reader import GeofabrikReader
from config import host, port, username, password, database_name, russian_regions, data_dir

osmdb = PostgresOSM(
    host=host, port=port, username=username, password=password,
    database_name=database_name, data_source='Geofabrik')

gfr = GeofabrikReader()


for reg in russian_regions:
    reg_data = gfr.read_osm_pbf(
        subregion_name=reg, data_dir=f'{data_dir}{reg}.pbf', expand=True, verbose=True)

    osmdb.import_osm_data(reg_data, table_name=reg)