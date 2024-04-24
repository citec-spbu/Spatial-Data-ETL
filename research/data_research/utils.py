import time
import urllib.error
import urllib.request
import datetime


def check_num(num: int) -> str:
    if num == 0:
        return "000"
    if 10 <= num < 100:
        return "0" + str(num)
    if num < 10:
        return "00" + str(num)
    return str(num)

def retry(url, save_way, max_attempts=3, delay=1):
    for attempt in range(max_attempts):
        try:
            urllib.request.urlretrieve(url, save_way)
        except urllib.error.URLError:
            if attempt < max_attempts - 1:
                time.sleep(delay)
                continue
            else:
                raise

def get_sequence_number_and_timestamp_from_state_file(save_path: str) -> tuple[int, datetime.datetime]:
    with open(save_path) as f:
        s = f.readlines()
    sequence_number = int(s[1].split("=")[1])
    timestamp = s[2].split("=")[1]
    timestamp = timestamp.strip()
    timestamp = timestamp.replace("\\:", ":")
    timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    return sequence_number, timestamp

def convert_sequence_number(sequence_number: int) -> tuple[int, int, int]:
    AAA = sequence_number // 1000000
    BBB = sequence_number // 1000 - AAA * 1000
    CCC = sequence_number - AAA * 1000000 - BBB * 1000
    return AAA, BBB, CCC