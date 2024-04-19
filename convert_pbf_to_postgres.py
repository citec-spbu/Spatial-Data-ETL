import subprocess

PASSWORD = 'postgres'


def run_osm2pgsql(
        username: str,
        db_title: str,
        host: str,
        pbf_file_name: str,
):
    # Определяем команду и параметры
    command = [
        'osm2pgsql',
        '-U', username,
        '-W',
        '-l',
        '-d', db_title,
        '-H', host,
        pbf_file_name,
    ]

    # Запускаем процесс
    try:
        result = subprocess.run(command, check=True, text=True, input=PASSWORD)
        print("osm2pgsql выполнен успешно.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении osm2pgsql: {e}")
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    _username = 'postgres'
    _db_title = 'leningrad'
    _host = 'localhost'
    _pbf_file_name = 'leningrad.osm.pbf'
    run_osm2pgsql(
        username=_username,
        db_title=_db_title,
        host=_host,
        pbf_file_name=_pbf_file_name,
    )
