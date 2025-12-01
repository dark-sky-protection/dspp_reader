import datetime
import json
import os
import socket
import logging
import sys

import yaml

from pathlib import Path
from pytz import timezone as tz

from dspp_reader.tools import Site, Device

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

class TESSW4C(object):

    def __init__(self,
                 bind_ip: str='0.0.0.0',
                 udp_port: int =2255,
                 save_to_file: bool=True,
                 save_to_database: bool=False,
                 post_to_api: bool=False,
                 save_files_to: Path = os.getcwd(),
                 file_format: str = 'tsv',
                 config_file: Path = None):
        self.bind_ip = bind_ip
        self.udp_port = udp_port
        self.save_to_file = save_to_file
        self.save_to_database = save_to_database
        self.post_to_api = post_to_api
        self.save_files_to = Path(save_files_to)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.bind_ip, self.udp_port))
        self.timestamp = datetime.datetime.now()
        self.separator = ' '
        self.format = file_format
        if self.format == 'tsv':
            self.separator = '\t'
        elif self.format == 'csv':
            self.separator = ','
        elif self.format == 'txt':
            self.separator = ' '
        self.config_file = Path(config_file) if config_file else Path(os.getcwd()) / 'config.yaml'
        self.sites = set({})
        self.devices = set({})
        if os.path.exists(self.config_file) and os.path.isfile(self.config_file):
            with open(self.config_file, 'r') as f:
                config = yaml.safe_load(f)
                if len(config['sites']) == 0:
                    logger.error('No sites defined')
                    sys.exit(1)
                for site in config['sites']:
                    new_site = Site(
                        id=site['id'],
                        latitude=site['latitude'],
                        longitude=site['longitude'],
                        elevation=site['elevation'],
                        timezone=site['timezone'],
                        name=site['name']
                    )
                    logger.info(f"Adding new site: {new_site.name}")
                    self.sites.add(new_site)
                    if len(site['devices']) == 0:
                        logger.warning(f"No devices found for site: {new_site.name}")
                    for device in site['devices']:
                        if device['type'].upper() == 'TESSW4C' and device['active']:
                            new_device = Device(
                                serial_id=device['serial_id'],
                                type=device['type'].upper(),
                                altitude=device['altitude'],
                                azimuth=device['azimuth'],
                                site=new_site)
                            logger.info(f"Adding new device: Type: {new_device.type} Serial ID: {new_device.serial_id}")
                            self.devices.add(new_device)

        else:
            logger.error('Site and Devices configuration file not found')

        logger.debug(f"TESSW4C initialized, listening on {self.bind_ip}:{self.udp_port}")

    def __call__(self):
        try:
            while True:
                self.timestamp = datetime.datetime.now(datetime.UTC)
                data, addr = self.socket.recvfrom(2048)
                parsed_data = json.loads(data.decode('utf-8'))
                device_serial = parsed_data['name']
                device = self.__get_device(serial_id=device_serial)
                if not device:
                    logger.debug(f"No matching device found with serial id: {device_serial}")
                else:
                    logger.debug(f"Found device: {device.serial_id} for site: {device.site.name}")
                    next_sunset, next_sunrise, time_to_sunset, time_to_sunrise = device.site.get_time_range()
                    if time_to_sunrise > time_to_sunset:
                        logger.debug(f"Next Sunset is at {next_sunset.strftime('%Y-%m-%d %H:%M:%S %Z (UTC%z)')}")
                        hours = int(time_to_sunset.sec // 3600)
                        minutes = int((time_to_sunset.sec % 3600) // 60)
                        seconds = int(time_to_sunset.sec % 60)
                        print(f"\rWaiting for {hours:02d} hours {minutes:02d} minutes {seconds:02d} seconds until next "
                              f"sunset {next_sunset.to_datetime(timezone=tz(device.site.timezone)).strftime('%Y-%m-%d %H:%M:%S')} {device.site.timezone}", end="", flush=True)
                        continue


                logger.info(f"TESSW4C received message at {self.timestamp.strftime('%Y-%m-%d %H:%M:%S %Z')} from ip address: {addr[0]}, device name: {device.serial_id if device else parsed_data['name']}")
                augmented_data = self._augment_data(data=parsed_data, device=device)
                if self.save_to_file:
                    self._write_to_file(data=augmented_data)
                if self.save_to_database:
                    self._write_to_database(data=augmented_data)
                if self.post_to_api:
                    self._post_to_api(data=augmented_data)

        except KeyboardInterrupt:
            logger.info("TESSW4C stopped by user")
        finally:
            self.socket.close()

    def __get_device(self, serial_id):
        for device in self.devices:
            if device.serial_id == serial_id:
                return device
        return None

    def _augment_data(self, data, device=None):
        data['timestamp'] = self.timestamp.isoformat()
        if device:
            data['altitude'] = device.altitude
            data['azimuth'] = device.azimuth
            if device.site:
                data['site'] = device.site.id
                data['timezone'] = device.site.timezone
                data['latitude'] = device.site.latitude.value
                data['longitude'] = device.site.longitude.value
                data['elevation'] = device.site.elevation.value

        return data

    def __get_filename(self, device_name):

        date = datetime.datetime.now().strftime("%Y%m%d")
        return self.save_files_to / f"{date}_{device_name}.{self.format}"

    def __get_header(self, data, filename):
        columns = []
        for key in data.keys():
            if key.startswith('F'):
                for subkey in data[key].keys():
                    columns.append(f"{key}_{subkey}")
            else:
                columns.append(key)
        return f"# File name: {filename}\n# {self.separator.join(columns)}\n"

    def __get_line_for_plain_text(self, data):
        fields = []
        for key in data.keys():
            if key.startswith('F'):
                for subkey in data[key].keys():
                    fields.append(str(data[key][subkey]))
            else:
                fields.append(str(data[key]))
        return f"{self.separator.join(fields)}\n"

    def _write_to_file(self, data):
        filename = self.__get_filename(device_name=data['name'])
        if not os.path.exists(filename):
            header = self.__get_header(data=data, filename=filename)
            with open(filename, 'w') as f:
                f.write(header)
        data_line = self.__get_line_for_plain_text(data)
        with open(filename, 'a') as f:
            f.write(data_line)
            logger.debug(f"TESSW4C data written to {filename}")

    def _write_to_database(self, data):
        print(data)

    def _post_to_api(self, data):
        print(json.dumps(data, indent=4))




if __name__ == '__main__':
    tess = TESSW4C()
    tess()
