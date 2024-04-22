import os
import subprocess
from subprocess import Popen, PIPE
from dotenv import load_dotenv
import os

load_dotenv()
DB_PASS = os.getenv('DB_PASS')
DB_NAME = os.getenv('DB_NAME')


def checkPsqlVersion():
    commandPsqlCheck = [
        'which',
        'psql'
    ]
    resultCheck = subprocess.run(commandPsqlCheck, check=True, capture_output=True)
    if len(resultCheck.stdout.decode("utf-8")) == 0:
        commandPsqlInst = [
            'sudo',
            'apt',
            'install',
            'postgresql'
        ]
        try:
            subprocess.run(commandPsqlInst, check=True)
        except subprocess.CalledProccesError as e:
            print(f"Ошибка при установке psql: {e}")
        except Exception as e:
            print(f"Ошибка: {e}")
    commandWVersion = [
        'pg_config',
        '--version'
    ]
    try:
        result = subprocess.run(commandWVersion, check=True, capture_output=True)
        version = result.stdout.decode("utf-8")
        version = version.split(" ")[1]
        if version.find(".") != -1:
            version = version[:version.find(".")]
        return version
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении: {e}")
    except Exception as e:
        print(f"Ошибка: {e}")


def installPostGIS(psqlVersion: str, dbName: str, password: str):
    try:
        commandPsqlDB = [
            'createdb',
            '-U',
            'postgres',
            dbName
        ]
        p = Popen(commandPsqlDB, stdout=PIPE, stdin=PIPE, stderr=PIPE, text=True)
        p.stdin.write(password + "\n")
        p.stdin.flush()
        p.kill()
        line = 'postgresql-' + psqlVersion + '-postgis-3'
        commandPostGISInst = ['sudo', 'apt', 'install', 'postgis', line]
        result = subprocess.run(commandPostGISInst, check=True)
        commandPsqlEnter = [
            'psql',
            '-U',
            'postgres',
            dbName
        ]
        p = Popen(commandPsqlEnter, stdout=PIPE, stdin=PIPE, stderr=PIPE, text=True)
        p.stdin.write(password)
        p.stdin.flush()
        commandExt = "CREATE EXTENSION postgis;\n"
        p.stdin.write(commandExt)
        p.stdin.flush()
        p.kill()
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при установке postgis: {e}")
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    psqlVersion = checkPsqlVersion()
    installPostGIS(psqlVersion, DB_NAME, DB_PASS)
