import logging
import os
import sys

from importlib.metadata import version

import yaml

from dspp_reader.sqmle.sqmle import SQMLE
from dspp_reader.tools import get_args, setup_logging

__version__ = version("dspp-reader")

CONFIG_FIELDS = [
    "site_id",
    "site_name",
    "site_latitude",
    "site_longitude",
    "site_elevation",
    "site_timezone",
    "device_type",
    "device_id",
    "device_altitude",
    "device_azimuth",
    "device_ip",
    "device_port",
    "device_window_correction",
    "number_of_reads",
    "reads_frequency",
    "save_to_file",
    "save_to_database",
    "post_to_api",
    "save_files_to",
    "file_format",
]


def read_sqmle(args=None):
    args = get_args(args=args, has_upd=False, default_device_type='sqmle')

    site = {}
    if args.config_file and os.path.isfile(args.config_file):
        with open(args.config_file, "r") as f:
            site = yaml.safe_load(f) or {}

    config = {}
    for field in CONFIG_FIELDS:
        config[field] = site.get(field, getattr(args, field))

    if args.config_file_example:
        print("# Add this to a .yaml file, reference it later with --config-file <file_name>.yaml")
        print(yaml.dump(config, default_flow_style=False, sort_keys=False))
        sys.exit(0)

    setup_logging(debug=args.debug, device_type=config["device_type"], device_id=config["device_id"])
    logger = logging.getLogger()
    logger.info(f"Starting SQMLE reader, Version: {__version__}")

    try:
        sqmle = SQMLE(
            site_id=config["site_id"],
            site_name=config["site_name"],
            site_latitude=config["site_latitude"],
            site_longitude=config["site_longitude"],
            site_elevation=config["site_elevation"],
            site_timezone=config["site_timezone"],
            device_type=config["device_type"],
            device_id=config["device_id"],
            device_altitude=config["device_altitude"],
            device_azimuth=config["device_azimuth"],
            device_ip=config["device_ip"],
            device_port=config["device_port"],
            device_window_correction=config["device_window_correction"],
            number_of_reads=config["number_of_reads"],
            reads_frequency=config["reads_frequency"],
            save_to_file=config["save_to_file"],
            save_to_database=config["save_to_database"],
            post_to_api=config["post_to_api"],
            save_files_to=config["save_files_to"],
            file_format=config["file_format"]
        )

        sqmle()
    except KeyboardInterrupt:
        print("\n")
        logger.info(f"Exiting SQMLE reader on user request, Version: {__version__}")
        sys.exit(0)
