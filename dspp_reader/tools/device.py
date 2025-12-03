from typing import Union

from dspp_reader.tools import Site

class Device(object):

    def __init__(self, serial_id: str, type: str, altitude: float, azimuth: float, site: Site, ip: Union[str, None] = None, port: Union[int, None] = None):
        self.serial_id = serial_id
        self.type = type
        self.altitude = altitude
        self.azimuth = azimuth
        self.site = site
        self.ip = ip
        self.port = port
        if self.type == 'sqmle' and ip is None and port is None:
            raise ValueError('ip and port must be specified for SQM-LE device')

    def __repr__(self):
        if self.type == 'sqmle':
            return f"Type: {self.type}\nSerial ID: {self.serial_id}\nAlt: {self.altitude}\nAz: {self.azimuth}\nSite: {self.site.name if self.site else 'No site'}\nIP: {self.ip}\nPort: {self.port}"
        elif self.type == 'tessw4c':
            return f"Type: {self.type}\nSerial ID: {self.serial_id}\nAlt: {self.altitude}\nAz: {self.azimuth}\nSite: {self.site.name if self.site else 'No site'}"
        else:
            return f"Device of unknown type: {self.type}"
