import datetime
from utils import check_num, retry, get_sequence_number_and_timestamp_from_state_file, convert_sequence_number
import os
from collect_deltes import logger

def get_last_info_state(region: str) -> tuple[int, datetime.datetime] | tuple[None, None]:
    """
    Retrieves the last information state for a given region.

    Args:
        region (str): The name of the region.

    Returns:
        tuple[int, datetime.datetime] | tuple[None, None]: A tuple containing the sequence number and timestamp
        of the last information state for the region. If the state file does not exist, returns (None, None).
    """
    save_path = os.path.join('data', region, 'state.txt')

    if not os.path.exists(save_path):
        return None, None
    
    return get_sequence_number_and_timestamp_from_state_file(save_path)


def download_state_file_by_region_on_geofabric(region: str) -> tuple[int, datetime.datetime]:
    """
    Downloads the state file from the OpenStreetMap replication server and retrieves the sequence number and timestamp.

    Args:
        region (str): The region to be downloaded.

    Returns:
        tuple: A tuple containing the sequence number and timestamp extracted from the state file.
    """
    reg = region.split("/")[1]

    save_path = os.path.join('data', reg)

    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    try:
        retry(f"https://download.geofabrik.de/{region}-updates/state.txt", os.path.join(save_path, 'state.txt'))
    except Exception as e:
        logger.error(f"{e} Error in downloading state file")

    return get_sequence_number_and_timestamp_from_state_file(os.path.join(save_path, 'state.txt'))

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
    AAA, BBB, CCC = convert_sequence_number(sequenceNumber)

    formatted_timestamp = timestamp.strftime("%Y%m%d_%H%M%S")

    save_path = os.path.join('data', 'delta', region)

    url = f"https://download.geofabrik.de/{region}-updates/{check_num(AAA)}/{check_num(BBB)}/{check_num(CCC)}.osc.gz"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    try:
        retry(url, os.path.join(save_path, f"{formatted_timestamp}.osc.gz"))
    except Exception as e:
        logger.error(f"{e} Error in downloading delta file {url}")