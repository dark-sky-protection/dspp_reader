import os

from importlib.metadata import version

__version__ = version("dspp-reader")

from dspp_reader.tools.common import read_device

CONFIG_FIELDS_DEFAULT = {
    "site_id": "ctio",
    "site_name": "Cerro Tololo",
    "site_latitude": -30.169166,
    "site_longitude": -70.804,
    "site_elevation": 2174,
    "site_timezone": "America/Santiago",
    "sun_altitude": -10,
    "device_type": "tess-w4c",
    "device_id": "stars1823",
    "device_altitude": 45,
    "device_azimuth": 0,
    "device_ip": "0.0.0.0",
    "device_port": 32,
    "delay_between_reads": 30,
    "read_always": False,
    "save_to_file": True,
    "save_to_database": False,
    "post_to_api": False,
    "save_files_to": os.getcwd(),
    "api_endpoint": "http://localhost:8000/api/tess-w4c",
    "api_token": "<get-an-appropriate-api-token>",
    "file_format": 'tsv',
    "save_logs_to": None,
}


def read_tessw4c(args=None):
    read_device(device_type='tess-w4c',
                config_fields_default=CONFIG_FIELDS_DEFAULT,
                args=args)
