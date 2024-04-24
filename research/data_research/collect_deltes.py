import schedule
import logging
import time
from config import REGIONS
from config import DAY_DELTA

from download_delta_region import download_state_file_by_region_on_geofabric, download_delta_file_by_region_on_geofabric, get_last_info_state

def collect_delta(region: str):
    logging.info(f"Collecting delta REGION: {region}; TIME: {time.time()}")

    sequenceNumber_last, timestamp_last = get_last_info_state(region)

    sequenceNumber, timestamp = download_state_file_by_region_on_geofabric(region)

    for i in range(sequenceNumber_last + 1, sequenceNumber + 1):
        download_delta_file_by_region_on_geofabric(region, i, timestamp)


def collect_delta_regions(regions: list):
    for region in regions:
        collect_delta(region)

# regions = ["russia/central-fed-district", "central-fed-district", "crimean-fed-district", "far-eastern-fed-district", "kaliningrad", "north-caucasus-fed-district", "northwestern-fed-district", "siberian-fed-district", "south-fed-district", "ural-fed-district", "volga-fed-district"]
schedule.every(DAY_DELTA).days.at("08:00").do(collect_delta_regions, REGIONS)

logging.basicConfig(level=logging.INFO, filename='app.log', format='%(asctime)s - %(levelname)s - %(message)s')


while True:
    schedule.run_pending()
    time.sleep(1)