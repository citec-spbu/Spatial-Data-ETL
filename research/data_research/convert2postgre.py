from pydriosm.ios import PostgresOSM
from pydriosm.reader import GeofabrikReader

def load_data2postgres(regions: list, data_dir: str, host: str, port: int, username: str, password: str, database_name: str):
    """
    Load data from OSM PBF files into a PostgreSQL database.

    Args:
        regions (list): A list of region names to load data for.
        data_dir (str): The directory where the OSM PBF files are located.
        host (str): The hostname of the PostgreSQL server.
        port (int): The port number of the PostgreSQL server.
        username (str): The username for connecting to the PostgreSQL server.
        password (str): The password for connecting to the PostgreSQL server.
        database_name (str): The name of the PostgreSQL database.

    Raises:
        Exception: If there is an error connecting to the database or reading the data.

    Returns:
        None
    """
    try:
        osmdb = PostgresOSM(
            host=host, port=port, username=username, password=password,
            database_name=database_name, data_source='Geofabrik')
    except Exception as e:
        print(e, "can't connect to database")

    gfr = GeofabrikReader()


    for reg in regions:
        try:
            reg_data = gfr.read_osm_pbf(
                subregion_name=reg, data_dir=f'{data_dir}{reg}.pbf', expand=True, verbose=True)
        except Exception as e:
            print(e, "can't read data", reg)

        try:
            osmdb.import_osm_data(reg_data, table_name=reg)
        except Exception as e:
            print(e, "can't import data", reg)