from pydantic import BaseSettings


class ResourceConfig(BaseSettings):
    """
    All constants and settings will be here.
    For more info: https://pydantic-docs.helpmanual.io/usage/settings/
    """

    mongo_host: str
    mongo_root_username: str
    mongo_root_password: str

    mongo_ddm_username: str
    mongo_ddm_password: str

    mongo_ddm_database: str

    rabbitmq_host: str
    rabbitmq_username: str
    rabbitmq_password: str

    class Config:
        env_file: str = '.env'
        validate_assignment: bool = True

        # Environment variables will always take priority over values loaded from a dotenv file.
        fields = {
            'mongo_ddm_username': {'env': ['MONGO_DDM_USERNAME']},
            'mongo_ddm_password': {'env': ['MONGO_DDM_PASSWORD']},
            'mongo_ddm_database': {'env': ['MONGO_DDM_DATABASE']},
            'mongo_root_username': {'env': ['MONGO_INITDB_ROOT_USERNAME']},
            'mongo_root_password': {'env': ['MONGO_INITDB_ROOT_PASSWORD']},
            'rabbitmq_host': {'env': ['RABBITMQ_SERVICE_HOST']},
            'rabbitmq_username': {'env': ['RABBITMQ_USERNAME']},
            'rabbitmq_password': {'env': ['RABBITMQ_PASSWORD']},
            'mongo_host': {'env': ['MONGO_DDM_HOST']},
        }


class AppConfig(BaseSettings):
    prosite_exe_path: str
    prosite_db_path: str

    iedb_mhci_version: str = '3.1.5'
    iedb_mhci_exe_path: str = None

    iedb_mhcii_version: str = '3.1.11'
    iedb_mhcii_exe_path: str = None

    class Config:
        env_file: str = '.env'
        env_file_encoding = 'utf-8'
        validate_assignment: bool = True

        # Environment variables will always take priority over values loaded from a dotenv file.
        fields = {
            'prosite_exe_path': {'env': ['PROSITE_INSTALL_PATH']},
            'prosite_db_path': {'env': ['PROSITE_DB_PATH']},
            'iedb_mhci_exe_path': {'env': ['IEDB_MHCI_INSTALL_PATH']},
            'iedb_mhcii_exe_path': {'env': ['IEDB_MHCI_INSTALL_PATH']},
        }
