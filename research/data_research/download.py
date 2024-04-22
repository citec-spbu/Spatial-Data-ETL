from pydriosm.downloader import GeofabrikDownloader

"""
Example for downloading data for the regions:

russian_regions = ['Central Federal District', 'Crimean Federal District', 'Far Eastern Federal District', 'North Caucasus Federal District', 'Northwestern Federal District',
                   'Siberian Federal District', 'South Federal District', 'Ural Federal District', 'Volga Federal District']
"""

def download_pbf_regions(regions: list, file_format: str, data_dir: str):
    """
    Downloads PBF regions from Geofabrik.

    Args:
        regions (list): A list of region names to download data for.
        file_format (str): The file format of the data to download.
        data_dir (str): The directory where the downloaded data will be stored.

    Returns:
        None
    """
    gfd = GeofabrikDownloader()

    for reg in regions:
        try:
            gfd.download_subregion_data(reg, file_format, data_dir, confirmation_required=False)
        except Exception as e:
            print(e, "Error in downloading", reg)