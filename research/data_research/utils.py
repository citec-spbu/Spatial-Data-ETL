import time
import urllib.error
import urllib.request


def check_num(num):
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