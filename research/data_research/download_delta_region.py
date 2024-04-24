import datetime
from utils import check_num, retry
import os

def get_last_info_state(region: str) -> tuple[int, datetime.datetime]:
    with open(f"data/{region}/state.txt") as f:
        s = f.readlines()
    sequenceNumber = int(s[2].split("=")[1])
    timestamp = s[1].split("=")[1]
    timestamp = timestamp.strip().replace("\\:", ":")
    timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    return sequenceNumber, timestamp


def download_state_file_by_region_on_geofabric(region: str) -> tuple[int, datetime.datetime]:
    """
    Downloads the state file from the OpenStreetMap replication server and retrieves the sequence number and timestamp.

    Args:
        region (str): The region to be downloaded.

    Returns:
        tuple: A tuple containing the sequence number and timestamp extracted from the state file.
    """

    """
    Russia
    russia/central-fed-district
    central-fed-district
    crimean-fed-district
    far-eastern-fed-district
    kaliningrad
    north-caucasus-fed-district
    northwestern-fed-district
    siberian-fed-district
    south-fed-district
    ural-fed-district
    volga-fed-district
    """
    '''https://download.geofabrik.de/russia/volga-fed-district-updates/state.txt'''
    reg = region.split("/")[1]

    save_path = os.path.join('data', reg)

    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    try:
        retry(f"https://download.geofabrik.de/{region}-updates/state.txt", os.path.join(save_path, 'state.txt'))
    except Exception as e:
        print(e, "Error in downloading state file")
    
    with open(f"data/{reg}/state.txt") as f:
        s = f.readlines()
    sequenceNumber = int(s[2].split("=")[1])
    timestamp = s[1].split("=")[1]
    timestamp = timestamp.strip().replace("\\:", ":")
    timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")

    return sequenceNumber, timestamp

def download_delta_file_by_region_on_geofabric(region: str, sequenceNumber: int, timestamp: str):
    """
    A function to download the delta file based on the sequence number and timestamp.

    Args:
        region (str): The region to be downloaded.
        sequenceNumber (int): The sequence number used to calculate AAA, BBB, and CCC. N = AAA*1000000 + BBB*1000 + CCC
        timestamp (str): The timestamp to be used in the file name.

    Returns:
        None
    """
    AAA = sequenceNumber // 1000000
    BBB = sequenceNumber // 1000 - AAA * 1000
    CCC = sequenceNumber - AAA * 1000000 - BBB * 1000

    formatted_timestamp = timestamp.strftime("%Y%m%d_%H%M%S")

    save_path = os.path.join('data', 'delta', region)

    url = f"https://download.geofabrik.de/{region}-updates/{check_num(AAA)}/{check_num(BBB)}/{check_num(CCC)}.osc.gz"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    try:
        retry(url, os.path.join(save_path, f"{formatted_timestamp}.osc.gz"))
    except Exception as e:
        print(e, "Error in downloading delta file", url)