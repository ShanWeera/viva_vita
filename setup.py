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

from viva_vdm.core.settings import ResourceConfig, AppConfig


class Setup(object):
    def __init__(self):
        self.settings = ResourceConfig()
        self.app_settings = AppConfig()
        self._con_retries = 0

        self.client = MongoClient(
            host=f'{self.settings.mongo_host}',
            port=27017,
            username=self.settings.mongo_root_username,
            password=self.settings.mongo_root_password,
        )

    def run(self):
        self._download_iedb_mhci_pred_tools()

    def _download_iedb_mhci_pred_tools(self):
        version = self.app_settings.iedb_mhci_version
        download_url = f'https://downloads.iedb.org/tools/mhci/{version}/IEDB_MHC_I-{version}.tar.gz'

        print(f'Downloading IEDB MHCI tools version: {version}')

        iedb_mhci_directory = self._create_resource_directory('iedb_mhci')
        archive_path = os.path.join(iedb_mhci_directory, 'mhci.tar.gz')
        extract_path = os.path.join(iedb_mhci_directory, 'mhci')

        urllib.request.urlretrieve(download_url, archive_path)

        print('Download completed..Extracting..')

        self._extract_tar(archive_path, extract_path)

        print('Extracting completed!. Cleaning up..')

        actual_path = os.path.join(extract_path, 'mhc_i')
        shutil.move(actual_path, iedb_mhci_directory)

        os.remove(archive_path)
        shutil.rmtree(extract_path)

    def _download_iedb_mhcii_pred_tools(self):
        version = self.app_settings.iedb_mhcii_version
        download_url = f'https://downloads.iedb.org/tools/mhcii/{version}/IEDB_MHC_II-{version}.tar.gz'

        iedb_mhci_directory = self._create_resource_directory('iedb_mhcii')
        archive_path = os.path.join(iedb_mhci_directory, 'mhcii.tar.gz')
        extract_path = os.path.join(iedb_mhci_directory, 'mhcii')

        urllib.request.urlretrieve(download_url, archive_path)

        self._extract_tar(archive_path, extract_path)

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

    def _create_resource_directory(self, resource: str):
        cwd = os.getcwd()

        directory = os.path.join(cwd, *('_resources', resource))

        self._create_directory(directory)

        return directory

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

        prosite_dir = self._create_resource_directory('prosite')
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
    def _create_directory(cls, directory: str) -> str:
        if os.path.exists(directory):
            shutil.rmtree(directory)

        os.makedirs(directory)


def main():
    Setup().run()


if __name__ == "__main__":
    main()
