from pydriosm.downloader import GeofabrikDownloader
from config import russian_regions, file_format, data_dir

gfd = GeofabrikDownloader()

for reg in russian_regions:
    gfd.download_subregion_data(reg, file_format, data_dir, confirmation_required=False)