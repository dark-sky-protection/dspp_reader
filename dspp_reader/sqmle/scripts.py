import logging
import os
import sys

from importlib.metadata import version
from pathlib import Path

import yaml

from dspp_reader.sqmle.sqmle import SQMLE
from dspp_reader.tools import get_args, setup_logging

__version__ = version("dspp-reader")

CONFIG_FIELDS_DEFAULT = {
    "site_id": "ctio",
    "site_name": "Cerro Tololo",
    "site_latitude": -30.169166,
    "site_longitude": -70.804,
    "site_elevation": 2174,
    "site_timezone": "America/Santiago",
    "sun_altitude": -10,
    "device_type": "sqmle",
    "device_id": "1823",
    "device_altitude": 45,
    "device_azimuth": 0,
    "device_ip": "0.0.0.0",
    "device_port": 10001,
    "device_window_correction": -0.11,
    "number_of_reads": 5,
    "reads_frequency": 30,
    "read_all_the_time": False,
    "save_to_file": True,
    "save_to_database": False,
    "post_to_api": False,
    "save_files_to": os.getcwd(),
    "file_format": 'tsv',
}


def read_sqmle(args=None):
    args = get_args(device_type='sqm-le', args=args)

    if args.config_file_example:
        print("# Add this to a .yaml file, reference it later with --config-file <file_name>.yaml")
        print(yaml.dump(CONFIG_FIELDS_DEFAULT, default_flow_style=False, sort_keys=False))
        sys.exit(0)

    site_config = {}
    if 'config_file' in args.__dict__.keys() and os.path.isfile(args.config_file):
        with open(args.config_file, "r") as f:
            site_config = yaml.safe_load(f) or {}

    config = {"device_type": 'sqmle'}
    for field in CONFIG_FIELDS_DEFAULT.keys():
        if field not in args.__dict__:
            config[field] = site_config.get(field)
        else:
            config[field] = getattr(args, field)



    setup_logging(debug=args.debug, device_type=config["device_type"], device_id=config["device_id"])
    logger = logging.getLogger()
    logger.info(f"Starting SQMLE reader, Version: {__version__}")

    logger.debug(f"Using the following configuration:\n{yaml.dump(config, default_flow_style=False, sort_keys=False)}")

    try:
        sqmle = SQMLE(
            site_id=config["site_id"],
            site_name=config["site_name"],
            site_latitude=config["site_latitude"],
            site_longitude=config["site_longitude"],
            site_elevation=config["site_elevation"],
            site_timezone=config["site_timezone"],
            sun_altitude=float(config["sun_altitude"]),
            device_type=config["device_type"],
            device_id=config["device_id"],
            device_altitude=float(config["device_altitude"]),
            device_azimuth=float(config["device_azimuth"]),
            device_ip=config["device_ip"],
            device_port=config["device_port"],
            device_window_correction=float(config["device_window_correction"]),
            number_of_reads=config["number_of_reads"],
            reads_frequency=config["reads_frequency"],
            read_all_the_time=bool(config["read_all_the_time"]),
            save_to_file=config["save_to_file"],
            save_to_database=config["save_to_database"],
            post_to_api=config["post_to_api"],
            save_files_to=Path(config["save_files_to"]),
            file_format=config["file_format"]
        )

        sqmle()
    except KeyboardInterrupt:
        print("\n")
        logger.info(f"Exiting SQMLE reader on user request, Version: {__version__}")
        sys.exit(0)
