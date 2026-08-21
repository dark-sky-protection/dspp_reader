from unittest import TestCase

from dspp_reader.tools.device import Device
from dspp_reader.tools.site import Site


class TestSite(TestCase):
    site_id = 'site'
    site_name = 'My Site'
    site_latitude = -30.169166
    site_longitude = -70.804
    site_elevation = 2174.
    site_timezone = 'America/Santiago'
    site_sun_altitude = -10

    site = Site(id=site_id,
                name=site_name,
                latitude=site_latitude,
                longitude=site_longitude,
                elevation=site_elevation,
                timezone=site_timezone)

    device_serial_id = '0000'
    device_altitude = 0
    device_azimuth = 0
    device_ip = '0.0.0.0'
    device_port = 1001


    def test_known_device(self):
        device_type = 'sqm-le'
        sqm_window_correction = 2
        device = Device(serial_id=self.device_serial_id,
                        type=device_type,
                        altitude=self.device_altitude,
                        azimuth=self.device_azimuth,
                        site=self.site,
                        ip=self.device_ip,
                        port=self.device_port,
                        window_correction=sqm_window_correction)

        self.assertEqual(device.serial_id, self.device_serial_id)
        self.assertEqual(device.type, device_type)
        self.assertEqual(device.altitude, self.device_altitude)
        self.assertEqual(device.azimuth, self.device_azimuth)
        self.assertEqual(device.site, self.site)
        self.assertEqual(device.ip, self.device_ip)
        self.assertEqual(device.port, self.device_port)

        self.assertEqual(device.__repr__(), f"Type: {device_type}\nSerial ID: {self.device_serial_id}\nAlt: {self.device_altitude}\nAz: {self.device_azimuth}\nSite: {self.site.name}\nIP: {self.device_ip}\nPort: {self.device_port}\nWindow Correction {sqm_window_correction}")

    def test_unknown_device(self):
        device_type = 'spectropgraph'
        device = Device(serial_id=self.device_serial_id,
                        type=device_type,
                        altitude=self.device_altitude,
                        azimuth=self.device_azimuth,
                        site=self.site,
                        ip=self.device_ip,
                        port=self.device_port)


        self.assertEqual(str(device), f"Device of unknown type: {device_type}")
