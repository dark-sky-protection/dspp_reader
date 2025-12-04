import logging
import os
import sys
import yaml

from importlib.metadata import version
from dspp_reader.tessw4c import TESSW4C
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
    "use_udp",
    "udp_bind_ip",
    "udp_port",
    "save_to_file",
    "save_to_database",
    "post_to_api",
    "save_files_to",
    "file_format",
]

def read_tessw4c(args=None):
    args = get_args(args=args, has_upd=True, default_device_type='tessw4c')


    site = {}
    if args.config_file and os.path.isfile(args.config_file):
        with open(args.config_file, 'r') as f:
            site = yaml.safe_load(f) or {}

    config = {}
    for field in CONFIG_FIELDS:
        config[field] = site.get(field, getattr(args, field))

    if args.config_file_example:
        print("# Add this to a .yaml file, reference it later with --config-file <file_name>.yaml")
        print(yaml.dump(config, default_flow_style=False, sort_keys=False))
        sys.exit(0)

    setup_logging(debug=args.debug, device_type=config['device_type'], device_id=config['device_id'])
    logger = logging.getLogger()
    logger.info(f"Starting TESSW4C reader, Version: {__version__}")

    try:
        tessw4c = TESSW4C(
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
            use_udp=config["use_udp"],
            udp_bind_ip=config["udp_bind_ip"],
            udp_port=config["udp_port"],
            save_to_file=config["save_to_file"],
            save_to_database=config["save_to_database"],
            post_to_api=config["post_to_api"],
            save_files_to=config["save_files_to"],
            file_format=config["file_format"])

        tessw4c()
    except KeyboardInterrupt:
        print("\n")
        logger.info(f"Exiting TESSW4C reader on user request, Version: {__version__}")
        sys.exit(0)
