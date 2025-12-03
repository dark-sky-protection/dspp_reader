import argparse
import os
import sys
import tzlocal
import yaml

from importlib.metadata import version
from dspp_reader.tessw4c import TESSW4C
from dspp_reader.tools import setup_logging

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

def get_args(args=None):
    parser = argparse.ArgumentParser(description=f"TESSW4C reader\nVersion: {__version__}")

    parser.add_argument('--use-udp', action='store_true', dest='use_udp', help='Read device by subscribing to an UDP port')
    parser.add_argument('--udp-bind-ip', action='store', dest='udp_bind_ip', type=str, default='0.0.0.0', help='IP address to bind to')
    parser.add_argument('--udp-port', action='store', dest='udp_port', type=int, default=2255,help="UDP port to listen on")
    parser.add_argument('--device-type', action='store', dest='device_type', type=str, default='tessw4c', help='Device type')
    parser.add_argument('--device-id', action='store', dest='device_id', type=str, default='unknown', help='Device serial ID')
    parser.add_argument('--device-altitude', action='store', dest='device_altitude', type=float, default=90, help='Device altitude')
    parser.add_argument('--device-azimuth', action='store', dest='device_azimuth', type=float, default=0, help='Device azimuth')
    parser.add_argument('--device-ip', action='store', dest='device_ip', type=str, default='0.0.0.0', help='Device IP address')
    parser.add_argument('--device-port', action='store', dest='device_port', type=int, default=32, help='Device TCP port')
    parser.add_argument('--site-id', action='store', dest='site_id', type=str, default='ctio', help='Site ID')
    parser.add_argument('--site-name', action='store', dest='site_name', type=str, default='Cerro Tololo', help='Site name')
    parser.add_argument('--site-latitude', action='store', dest='site_latitude', type=float, default=-30.169166, help='Site latitude')
    parser.add_argument('--site-longitude', action='store', dest='site_longitude', type=float, default=-70.804, help='Site longitude')
    parser.add_argument('--site-elevation', action='store', dest='site_elevation', type=int, default=2174, help='Site elevation')
    parser.add_argument('--site-timezone', action='store', dest='site_timezone', default=tzlocal.get_localzone_name(), help='Site timezone')
    parser.add_argument('--save-to-file', action='store_false', dest='save_to_file', help="Save to a plain text file")
    parser.add_argument('--save-to-database', action='store_true', dest='save_to_database', help="Save to a database")
    parser.add_argument('--post-to-api', action='store_true', dest='post_to_api', help="Send data through a POST request to a REST API")
    parser.add_argument('--save-files-to', action='store', dest='save_files_to', default=os.getcwd(), help="Destination path to save files")
    parser.add_argument('--file-format', action='store', dest='file_format', default='tsv', help='File format to use')
    parser.add_argument('--config-file', action='store', dest='config_file', default=None, help="Configuration file full path")
    parser.add_argument('--config-file-example', action='store_true', dest='config_file_example', help="Print a configuration file example")
    parser.add_argument('--debug', action='store_true', dest='debug', default=False, help="Enable debug mode")

    args = parser.parse_args(args=args)
    return args

def read_tessw4c(args=None):
    args = get_args(args=args)


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

    logger = setup_logging(debug=args.debug, device_type=config['device_type'], device_id=config['device_id'])
    logger.info(f"Starting TESSW4C reader, Version: {__version__}")

    tessw4c = TESSW4C(
        use_udp=config["use_udp"],
        udp_bind_ip=config["udp_bind_ip"],
        udp_port=config["udp_port"],
        device_type=config["device_type"],
        device_id=config["device_id"],
        device_altitude=config["device_altitude"],
        device_azimuth=config["device_azimuth"],
        device_tcp_ip=config["device_ip"],
        device_port=config["device_port"],
        site_id=config["site_id"],
        site_name=config["site_name"],
        site_latitude=config["site_latitude"],
        site_longitude=config["site_longitude"],
        site_elevation=config["site_elevation"],
        site_timezone=config["site_timezone"],
        save_to_file=config["save_to_file"],
        save_to_database=config["save_to_database"],
        post_to_api=config["post_to_api"],
        save_files_to=config["save_files_to"],
        file_format=config["file_format"])

    tessw4c()
