import datetime
import logging
import os
import time

from astropy.units import Quantity
from argparse import ArgumentParser, SUPPRESS
from importlib.metadata import version
from logging.handlers import TimedRotatingFileHandler

from pathlib import Path


__version__ = version('dspp-reader')


class DeviceTimeRotatingFileHandler(TimedRotatingFileHandler): # pragma: no cover
    """Custom log filename handler with name rotation"""
    def __init__(self, device_type, device_id, save_logs_to=None, *args, **kwargs):
        self.device_type = device_type
        self.device_id = device_id
        self.save_logs_to = save_logs_to
        self._current_date = datetime.datetime.now().strftime('%Y%m%d')

        if self.save_logs_to:
            os.makedirs(self.save_logs_to, exist_ok=True)
            if 'filename' in kwargs:
                kwargs['filename'] = os.path.join(self.save_logs_to, self._get_dated_filename())

        super().__init__(*args, **kwargs)

    def _get_dated_filename(self):
        return f"{self._current_date}_{self.device_type}_{self.device_id}.log"

    def rotation_filename(self, default_name):
        filename = self._get_dated_filename()
        return os.path.join(self.save_logs_to, filename) if self.save_logs_to else filename

    def emit(self, record):
        today = datetime.datetime.now().strftime('%Y%m%d')
        if today != self._current_date:
            self._current_date = today
            self.doRollover()
        super().emit(record)

def clean_data(obj):
    """Recursively convert Quantities to plain numbers inside nested structures."""
    if isinstance(obj, Quantity):
        return obj.value
    elif isinstance(obj, dict):
        return {k: clean_data(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return type(obj)(clean_data(v) for v in obj)
    else:
        return obj

def augment_data(data, timestamp, device=None):
    data['timestamp'] = timestamp.isoformat() # UT, buscar formato con menos decimales si no formatear a mano
    data['localtime'] = timestamp.astimezone().isoformat() # Local Time with UT Offset
    if device:
        data['device'] = device.type
        data['serial_number'] = device.serial_id
        data['altitude'] = device.altitude
        data['azimuth'] = device.azimuth
        if device.site:
            data['site'] = device.site.id
            data['timezone'] = device.site.timezone
            data['latitude'] = device.site.latitude
            data['longitude'] = device.site.longitude
            data['elevation'] = device.site.elevation
    return data

def setup_logging(debug=False, device_type='photometer', device_id='0000', save_logs_to=None):
    """Setup logging

    Args:
        debug (bool, optional): Debug mode. Defaults to False.
        device_type (str, optional): Device type. Defaults to 'photometer'.
        device_id (str, optional): Device ID. Defaults to '0000'.
        save_logs_to (str, optional): Log directory. Defaults to None.

    Returns:
        logging.Logger: Logging object
    """
    logging_format = '[%(asctime)s][%(levelname).1s]: %(message)s'
    logging_level =logging.INFO
    if debug:
        logging_format = '[%(asctime)s][%(levelname)8s]: %(message)s [%(module)s.%(funcName)s:%(lineno)d]'
        logging_level = logging.DEBUG
    logging_datefmt = "%Y-%m-%d %H:%M:%S UTC"
    logging.Formatter.converter = time.gmtime

    logging.basicConfig(format=logging_format, level=logging_level, datefmt=logging_datefmt)

    file_handler = DeviceTimeRotatingFileHandler(
        device_type=device_type,
        device_id=device_id,
        save_logs_to=save_logs_to,
        filename=f"{device_type}_{device_id}.log",
        when="D",
        interval=1,
        atTime=datetime.time(12, 0),
        backupCount=7,
        encoding='utf-8'
    )
    file_handler.setLevel(logging_level)
    formatter = logging.Formatter(logging_format, datefmt=logging_datefmt)
    formatter.converter = time.gmtime
    file_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.addHandler(file_handler)

    return logger


def get_filename(save_files_to: Path, device_name:str, device_type: str, file_format:str) -> Path:
    """Get filename to save data to

    Args:
        save_files_to: Path where to save data to
        device_name: Device name
        device_type: Device type
        file_format: File format

    Returns:
         Path with filename
    """
    now_local = datetime.datetime.now().astimezone()

    local_noon = now_local.replace(hour=12, minute=0, second=0, microsecond=0)
    if now_local < local_noon:
        date_string = (now_local - datetime.timedelta(days=1)).strftime('%Y%m%d')
    else:
        date_string = now_local.strftime('%Y%m%d')
    return save_files_to / f"{date_string}_{device_type}_{device_name}.{file_format}"

def get_args(device_type, args=None): # pragma: no cover
    parser = ArgumentParser(description=f"{device_type.upper()} reader\nVersion: {__version__}")

    parser.add_argument('--site-id', action='store', dest='site_id', type=str, default=SUPPRESS, help='A conventional unique site id, for instance, `ctio`, `pachon` or `morado`')
    parser.add_argument('--site-name', action='store', dest='site_name', type=str, default=SUPPRESS, help='Full site name')
    parser.add_argument('--site-latitude', action='store', dest='site_latitude', type=float, default=SUPPRESS, help='Site latitude')
    parser.add_argument('--site-longitude', action='store', dest='site_longitude', type=float, default=SUPPRESS, help='Site longitude')
    parser.add_argument('--site-elevation', action='store', dest='site_elevation', type=int, default=SUPPRESS, help='Site elevation')
    parser.add_argument('--site-timezone', action='store', dest='site_timezone', default=SUPPRESS, help='Site timezone')
    parser.add_argument('--sun-altitude', action='store', dest='sun_altitude', type=float, default=SUPPRESS, help='Sun altitude with respect to the horizon. This defines when to start reading.')
    parser.add_argument('--device-id', action='store', dest='device_id', type=str, default=SUPPRESS, help='Device serial ID')
    parser.add_argument('--device-altitude', action='store', dest='device_altitude', type=float, default=SUPPRESS, help='Device altitude')
    parser.add_argument('--device-azimuth', action='store', dest='device_azimuth', type=float, default=SUPPRESS, help='Device azimuth')
    parser.add_argument('--device-ip', action='store', dest='device_ip', type=str, default=SUPPRESS, help='Device IP address')
    parser.add_argument('--device-port', action='store', dest='device_port', type=int, default=SUPPRESS, help='Device TCP port')
    if device_type in ['sqm-le']:
        parser.add_argument('--device-window-correction', action='store', dest='device_window_correction', type=float, default=SUPPRESS, help='If an SQM was mounted in housing with acrylic window the correction must be -0.11 mag')
        parser.add_argument('--number-of-reads', action='store', dest='number_of_reads', type=int, default=SUPPRESS, help='Number of reads to average')
    parser.add_argument('--delay-between-reads', action='store', dest='delay_between_reads', type=int, default=SUPPRESS, help='How many seconds between reads')
    parser.add_argument('--read-always', action='store_true', dest='read_always', default=False, help='Allows to ignore the time constraints')
    parser.add_argument('--save-to-file', action='store_true', dest='save_to_file', help="Save to a plain text file")
    parser.add_argument('--save-to-database', action='store_true', dest='save_to_database', help="Save to a database")
    parser.add_argument('--post-to-api', action='store_true', dest='post_to_api', help="Send data through a POST request to a REST API")
    parser.add_argument('--save-files-to', action='store', dest='save_files_to', default=SUPPRESS, help="Destination path to save files")
    parser.add_argument('--api-endpoint', action='store', dest='api_endpoint', type=str, default=SUPPRESS, help='API endpoint')
    parser.add_argument('--api-token', action='store', dest='api_token', type=str, default=SUPPRESS, help='API Token')
    parser.add_argument('--file-format', action='store', dest='file_format', choices=['tsv', 'csv', 'txt'], default=SUPPRESS, help='File format to use')
    parser.add_argument('--config-file', action='store', dest='config_file', default=SUPPRESS, help="Configuration file full path")
    parser.add_argument('--save-logs-to', action='store', dest='save_logs_to', default=SUPPRESS, help="Directory to save logs to")
    parser.add_argument('--config-file-example', action='store_true', dest='config_file_example', help="Print a configuration file example")
    parser.add_argument('--debug', action='store_true', dest='debug', default=False, help="Enable debug mode")

    args = parser.parse_args(args=args)

    if not any(list(args.__dict__.values())):
        parser.print_help()
        exit(1)
    return args
