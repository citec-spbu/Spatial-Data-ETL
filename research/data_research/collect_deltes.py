import schedule
import logging
import time
from config import REGIONS

def collect_delta(region: str):
    logging.info(f"Collecting delta REGION: {region}; TIME: {time.time()}")

def collect_delta_regions(regions: list):
    for region in regions:
        collect_delta(region)

# regions = ["russia/central-fed-district", "central-fed-district", "crimean-fed-district", "far-eastern-fed-district", "kaliningrad", "north-caucasus-fed-district", "northwestern-fed-district", "siberian-fed-district", "south-fed-district", "ural-fed-district", "volga-fed-district"]
schedule.every().day.at("08:00").do(collect_delta_regions, REGIONS)

logging.basicConfig(level=logging.INFO, filename='app.log', format='%(asctime)s - %(levelname)s - %(message)s')


while True:
    schedule.run_pending()
    time.sleep(1)