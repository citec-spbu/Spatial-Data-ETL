import datetime
from utils import check_num, retry, get_sequence_number_and_timestamp_from_state_file, convert_sequence_number
import os

def download_state_file_country(country: str) -> tuple[int, datetime.datetime]:
    """
    Downloads the state file from the OpenStreetMap replication server and retrieves the sequence number and timestamp.

    Args:
        None

    Returns:
        tuple: A tuple containing the sequence number and timestamp extracted from the state file.
    """
    if not os.path.exists("data"):
        os.makedirs("data")

    try:
        retry(f"https://download.geofabrik.de/{country}-updates/",
                                f"data/{country}/state.txt")
    except Exception as e:
        print(e, "Error in downloading state file")

    return get_sequence_number_and_timestamp_from_state_file(f"data/{country}/state.txt")


def download_delta_file_country(country: str, sequenceNumber: int, timestamp: str):
    """
    A function to download the delta file based on the sequence number and timestamp.

    Args:
        sequenceNumber (int): The sequence number used to calculate AAA, BBB, and CCC. N = AAA*1000000 + BBB*1000 + CCC
        timestamp (str): The timestamp to be used in the file name.

    Returns:
        None
    """
    AAA, BBB, CCC = convert_sequence_number(sequenceNumber)

    url = f"https://download.geofabrik.de/{country}-updates/{check_num(AAA)}/{check_num(BBB)}/{check_num(CCC)}.osc.gz"

    save_path = os.path.join('data', country, 'delta')

    if not os.path.exists(save_path):
        os.makedirs(save_path)
    try:
        retry(url, os.path.join(save_path, f"{timestamp}.osc.gz"))
    except Exception as e:
        print(e, "Error in downloading delta file")
        