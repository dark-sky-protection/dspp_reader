import argparse
import logging
import os

from importlib.metadata import version
from dspp_reader.tessw4c import TESSW4C

__version__ = version("dspp-reader")

def get_args(args=None):
    parser = argparse.ArgumentParser(description=f"TESSW4C reader\nVersion: {__version__}")

    parser.add_argument('--bind-ip', action='store', dest='bind_ip', default='0.0.0.0', help='IP address to bind to')
    parser.add_argument('--udp-port', action='store', dest='udp_port', default=2255,help="UDP port to listen on")
    parser.add_argument('--save-to-file', action='store_false', dest='save_to_file', help="Save to a plain text file")
    parser.add_argument('--save-to-database', action='store_true', dest='save_to_database', help="Save to a database")
    parser.add_argument('--post-to-api', action='store_true', dest='post_to_api', help="Send data through a POST request to a REST API")
    parser.add_argument('--save-files-to', action='store', dest='save_files_to', default=os.getcwd(), help="Destination path to save files")
    parser.add_argument('--file-format', action='store', dest='file_format', default='tsv', help='File format to use')
    parser.add_argument('--config-file', action='store', dest='config_file', help="Configuration file full path")
    parser.add_argument('--debug', action='store_true', dest='debug', default=False, help="Enable debug mode")

    args = parser.parse_args(args=args)
    return args


def script(args=None):
    args = get_args(args=args)

    logging_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging_level = logging.DEBUG if args.debug else logging.INFO
    logging_datefmt = "%H:%M:%S"

    # logging_formatter = logging.Formatter(fmt=logging_format, datefmt=logging_datefmt)

    logging.basicConfig(format=logging_format, level=logging_level, datefmt=logging_datefmt)

    logger = logging.getLogger()

    tessw4c = TESSW4C(
        bind_ip=args.bind_ip,
        udp_port=args.udp_port,
        save_to_file=args.save_to_file,
        save_to_database=args.save_to_database,
        post_to_api=args.post_to_api,
        save_files_to=args.save_files_to,
        file_format=args.file_format,
        config_file=args.config_file)

    tessw4c()


if __name__ == "__main__":
    script()
