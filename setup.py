"""
This script is used to set up the environment, and resources on first run.
"""
import platform
import shutil
import time
import urllib.request
import os
import zipfile
import tarfile

import dotenv

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure, CollectionInvalid

from viva_vdm.settings import ResourceConfig


class Setup(object):
    def __init__(self):
        self.settings = ResourceConfig()
        self._con_retries = 0

        self.client = MongoClient(
            host=f'{self.settings.mongo_host}',
            port=27017,
            username=self.settings.mongo_root_username,
            password=self.settings.mongo_root_password,
        )

    def run(self):
        self._check_if_connected()
        self._create_db()
        self._create_user()
        self._download_prosite()

    def _check_if_connected(self):
        try:
            print(self.client.server_info())
        except ServerSelectionTimeoutError as e:
            if self._con_retries > 10:
                print(e)
                exit(1)

            time.sleep(5)
            self._con_retries += 1

            print(f'Retrying Database Connection x{self._con_retries}/10')

            self._check_if_connected()

    def _create_db(self):
        dbs = self.client.list_database_names()
        ddm_db = self.settings.mongo_ddm_database

        if ddm_db in dbs:
            print(f'Database {ddm_db} already present')
            return

        db = self.client[ddm_db]

        try:
            result = db.create_collection('delete_me')
            print(result)
        except CollectionInvalid as e:
            print(e)
            exit(2)

    def _create_user(self):
        ddm_db = self.settings.mongo_ddm_database

        db = self.client[ddm_db]

        try:
            result = db.command(
                'createUser',
                self.settings.mongo_ddm_username,
                pwd=self.settings.mongo_ddm_password,
                roles=[{'role': 'readWrite', 'db': ddm_db}],
            )

            print(result)
        except OperationFailure as e:
            print(e.details)

    def _download_prosite(self):
        print("Creating Prosite directory..")
        prosite_dir = self._create_prosite_dir()
        prosite_db = os.path.join(prosite_dir, 'prosite.dat')

        dotenv_file = dotenv.find_dotenv()
        dotenv.load_dotenv(dotenv_file)
        dotenv.set_key(dotenv_file, "PROSITE_DB_PATH", prosite_db)

        print("Downloading Prosite database..")
        urllib.request.urlretrieve('https://ftp.expasy.org/databases/prosite/prosite.dat', prosite_db)

        print("Downloading Prosite binaries..")
        if platform.system() == "Linux":
            prosite_archive = os.path.join(prosite_dir, 'ps_scan_linux_x86_elf.tar.gz')
            urllib.request.urlretrieve(
                'https://ftp.expasy.org/databases/prosite/ps_scan/ps_scan_linux_x86_elf.tar.gz', prosite_archive
            )

            self._extract_tar(prosite_archive, prosite_dir)
            dotenv.set_key(dotenv_file, "PROSITE_INSTALL_PATH", os.path.join(prosite_dir, 'ps_scan', 'pfscan'))
        elif platform.system() == "Windows":
            prosite_archive = os.path.join(prosite_dir, 'ps_scan_win32.zip')

            urllib.request.urlretrieve(
                'https://ftp.expasy.org/databases/prosite/ps_scan/ps_scan_win32.zip', prosite_archive
            )

            with zipfile.ZipFile(prosite_archive, 'r') as zip_ref:
                zip_ref.extractall(prosite_dir)

            dotenv.set_key(dotenv_file, "PROSITE_INSTALL_PATH", os.path.join(prosite_dir, 'ps_scan', 'pfscan.exe'))
        elif platform.system() == "Darwin":
            prosite_archive = os.path.join(prosite_dir, 'ps_scan_macosx.tar.gz')
            urllib.request.urlretrieve(
                'https://ftp.expasy.org/databases/prosite/ps_scan/ps_scan_macosx.tar.gz', prosite_archive
            )

            self._extract_tar(prosite_archive, prosite_dir)
            dotenv.set_key(dotenv_file, "PROSITE_INSTALL_PATH", os.path.join(prosite_dir, 'ps_scan', 'pfscan'))

        print("Prosite setup completed.")

    @classmethod
    def _extract_tar(cls, tar_path: str, extract_path: str):
        tar = tarfile.open(tar_path, "r:gz")
        tar.extractall(path=extract_path)
        tar.close()

    @classmethod
    def _create_prosite_dir(cls) -> str:
        cwd = os.getcwd()
        prosite_dir = os.path.join(cwd, 'prosite')

        if os.path.exists(prosite_dir):
            shutil.rmtree(prosite_dir)

        os.mkdir(prosite_dir)

        return prosite_dir


def main():
    Setup().run()


if __name__ == "__main__":
    main()
