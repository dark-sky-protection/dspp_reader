from dspp_reader.tools import Site

class Device(object):

    def __init__(self, serial_id, type, altitude, azimuth, site: Site):
        self.serial_id = serial_id
        self.type = type
        self.altitude = altitude
        self.azimuth = azimuth
        self.site = site

    def __repr__(self):
        return f"Type: {self.type}\nSerial ID: {self.serial_id}\nAlt: {self.altitude}\nAz: {self.azimuth}\nSite: {self.site.name}"
