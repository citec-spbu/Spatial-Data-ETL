import datetime
from utils import check_num, retry
import os

def download_state_file() -> tuple[int, datetime.datetime]:
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
        retry("https://planet.openstreetmap.org/replication/day/state.txt",
                                "data/state.txt")
    except Exception as e:
        print(e, "Error in downloading state file")

    with open("data/state.txt") as f:
        s = f.readlines()
    sequenceNumber = int(s[1].split("=")[1])
    timestamp = s[2].split("=")[1]
    timestamp = timestamp.strip()
    timestamp = timestamp.replace("\\:", ":")
    timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")

    return sequenceNumber, timestamp


def download_delta_file(sequenceNumber: int, timestamp: str):
    """
    A function to download the delta file based on the sequence number and timestamp.

    Args:
        sequenceNumber (int): The sequence number used to calculate AAA, BBB, and CCC. N = AAA*1000000 + BBB*1000 + CCC
        timestamp (str): The timestamp to be used in the file name.

    Returns:
        None
    """
    AAA = sequenceNumber // 1000000
    BBB = sequenceNumber // 1000 - AAA * 1000
    CCC = sequenceNumber - AAA * 1000000 - BBB * 1000

    url = f"https://planet.openstreetmap.org/replication/day/{check_num(AAA)}/{check_num(BBB)}/{check_num(CCC)}.osc.gz"

    save_path = os.path.join('data', 'delta')

    if not os.path.exists(save_path):
        os.makedirs(save_path)
    try:
        retry(url, os.path.join(save_path, f"{timestamp}.osc.gz"))
    except Exception as e:
        print(e, "Error in downloading delta file")
        