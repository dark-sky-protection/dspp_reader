import datetime
import logging

from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

class DeviceTimeRotatingFileHandler(TimedRotatingFileHandler):
    """Custom log filename handler with name rotation"""
    def __init__(self, device_type, device_id, *args, **kwargs):
        self.device_type = device_type
        self.device_id = device_id
        super().__init__(*args, **kwargs)

    def rotation_filename(self, default_name):
        date_str = datetime.datetime.now().strftime('%Y%m%d')
        return f"{date_str}_{self.device_type}_{self.device_id}.log"


def setup_logging(debug=False, device_type='photometer', device_id='0000'):
    """Setup logging

    Args:
        debug (bool, optional): Debug mode. Defaults to False.
        device_type (str, optional): Device type. Defaults to 'photometer'.
        device_id (str, optional): Device ID. Defaults to '0000'.

    Returns:
        logging.Logger: Logging object
    """
    logging_format = '[%(asctime)s][%(levelname).1s]: %(message)s'
    logging_level =logging.INFO
    if debug:
        logging_format = '[%(asctime)s][%(levelname)8s]: %(message)s [%(module)s.%(funcName)s:%(lineno)d]'
        logging_level = logging.DEBUG
    logging_datefmt = "%H:%M:%S"

    logging.basicConfig(format=logging_format, level=logging_level, datefmt=logging_datefmt)

    file_handler = DeviceTimeRotatingFileHandler(
        device_type=device_type,
        device_id=device_id,
        filename=f"{device_type}_{device_id}.log",
        when="D",
        interval=1,
        atTime=datetime.time(12, 0),
        backupCount=7,
        encoding='utf-8'
    )
    file_handler.setLevel(logging_level)
    file_handler.setFormatter(logging.Formatter(logging_format))

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
