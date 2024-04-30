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
        pbf_file_name: str,
):
    # Определяем команду и параметры
    command = [
        'osm2pgsql',
        '-U', username,
        '-W',
        '-l',
        '-d', db_name,
        '-H', host,
        pbf_file_name,
    ]

    # Запускаем процесс
    try:
        result = subprocess.run(command, check=True, text=True, input=PASSWORD)
        logger.info("osm2pgsql выполнен успешно.")
    except subprocess.CalledProcessError as e:
        logger.info(f"Ошибка при выполнении osm2pgsql: {e}")
    except Exception as e:
        logger.info(f"Ошибка: {e}")


def download_raw_file_with_url(url: str, name: str):
    urllib.request.urlretrieve(url, name)


if __name__ == "__main__":
    _username = config.DB_USER
    _db_name = config.DB_NAME
    _host = config.DB_HOST
    _pbf_file_name = 'raw.osm.pbf'

    _download_url = f"https://download.geofabrik.de/{config.REGIONS[0]}/crimean-fed-district-latest.osm.pbf"

    download_raw_file_with_url(_download_url, _pbf_file_name)

    run_osm2pgsql(
        username=_username,
        db_name=_db_name,
        host=_host,
        pbf_file_name=_pbf_file_name,
    )
