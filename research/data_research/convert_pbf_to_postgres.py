import subprocess
import logging
import urllib.request
import config

PASSWORD = config.DB_PASS
logger = logging.getLogger("osm2pgsql")


def run_osm2pgsql(
        username: str,
        db_name: str,
        host: str,
        pbf_file_path: str,
):
    # Определяем команду и параметры
    command = [
        'osm2pgsql',
        '-U', username,
        '-W',
        '-l',
        '-d', db_name,
        '-H', host,
        pbf_file_path,
    ]

    # Запускаем процесс
    try:
        result = subprocess.run(command, check=True, text=True, input=PASSWORD)
        logger.info("osm2pgsql выполнен успешно.")
    except subprocess.CalledProcessError as e:
        logger.info(f"Ошибка при выполнении osm2pgsql: {e}")
    except Exception as e:
        logger.info(f"Ошибка: {e}")


def download_raw_file_with_url(url: str, path: str):
    urllib.request.urlretrieve(url, path)


if __name__ == "__main__":
    _username = config.DB_USER
    _db_name = config.DB_NAME
    _host = config.DB_HOST

    pbf_file_name = "raw.osm.pbf"
    data_dir_path = "data"

    raw_pbf_file_path = f"{data_dir_path}/{pbf_file_name}"

    _download_url = f"https://download.geofabrik.de/{config.REGIONS[0]}/{config.FILE_TO_DOWNLOAD}"

    download_raw_file_with_url(_download_url, raw_pbf_file_path)

    run_osm2pgsql(
        username=_username,
        db_name=_db_name,
        host=_host,
        pbf_file_path=raw_pbf_file_path,
    )
