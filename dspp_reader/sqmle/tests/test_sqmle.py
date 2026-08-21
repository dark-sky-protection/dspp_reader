import os
from pathlib import Path

import astropy.units as u

from unittest import TestCase

from dspp_reader.sqmle.sqmle import SQMLE
from dspp_reader.sqmle.sqmle import (
    READ,
    READ_WITH_SERIAL_NUMBER,
    REQUEST_CALIBRATION_INFORMATION,
    UNIT_INFORMATION_REQUEST)


class TestSQMLE(TestCase):
    def setUp(self):
        self.window_correction = -1
        self.sqmle = SQMLE(
            site_id="site",
            site_name="My Site",
            site_timezone="America/Santiago",
            site_latitude=-30.169166,
            site_longitude=-30.169166,
            site_elevation=2174,
            sun_altitude=-10,
            device_type="sqm-le",
            device_id='0000',
            device_altitude=0,
            device_azimuth=0,
            device_ip='0.0.0.0',
            device_port=8080,
            device_window_correction=self.window_correction,
            number_of_reads=3,
            reads_spacing=1,
            delay_between_reads=30,
            read_always=False,
            save_to_file=True,
            save_to_database=False,
            post_to_api=False,
            save_files_to=Path(os.getcwd()),
            api_endpoint='http://localhost:8080/sqmle',
            api_token='',
            file_format='tsv')


    def test_sqmle(self):
        self.assertIsInstance(self.sqmle, SQMLE)

    def test_write_to_database(self):
        self.assertRaises(NotImplementedError, self.sqmle._write_to_database, {})

    def test_apply_window_correction(self):
        input_magnitude = 4 * u.mag
        expected_magnitude = input_magnitude + self.window_correction * u.mag
        test_data = {"magnitude": input_magnitude }

        new_data = self.sqmle._apply_window_correction(data=test_data)

        self.assertEqual(new_data["magnitude"], expected_magnitude)

    def test_parse_data_no_data(self):
        data = ""
        self.assertRaises(ValueError, self.sqmle._parse_data, data=data, command=READ)

    def test_parse_data__command_unknown(self):
        line = "some,fake,data"
        data = self.sqmle._parse_data(data=line, command=b'ls\r\n')
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 3)
        self.assertListEqual(data, ['some', 'fake', 'data'])


    def test_parse_data__command_READ__wrong_data_format(self):
        line = "r, 16.72m,0000000020Hz,0000023192c,0000000.050s"
        self.assertRaises(ValueError, self.sqmle._parse_data, data=line, command=READ)

    def test_parse_data__command_READ(self):
        line = "r, 16.72m,0000000020Hz,0000023192c,0000000.050s, 025.4C"
        data = self.sqmle._parse_data(data=line, command=READ)
        self.assertIsInstance(data, dict)
        self.assertEqual(len(data), 6)
        self.assertIsInstance(data['type'], str)
        self.assertIsInstance(data['magnitude'], u.Quantity)
        self.assertEqual(data['magnitude'].unit, u.mag)
        self.assertIsInstance(data['frequency'], u.Quantity)
        self.assertEqual(data['frequency'].unit, u.Hz)
        self.assertIsInstance(data['period_count'], u.Quantity)
        self.assertEqual(data['period_count'].unit, u.count)
        self.assertIsInstance(data['period_seconds'], u.Quantity)
        self.assertEqual(data['period_seconds'].unit, u.second)
        self.assertIsInstance(data['temperature'], u.Quantity)
        self.assertEqual(data['temperature'].unit, u.C)

    def test_parse_data__command_READ_WITH_SERIAL_NUMBER__wrong_data_format(self):
        line = "r, 16.72m,0000000020Hz,0000023192c,0000000.050s, 025.4C"

        self.assertRaises(ValueError, self.sqmle._parse_data, data=line, command=READ_WITH_SERIAL_NUMBER)

    def test_parse_data__command_READ_WITH_SERIAL_NUMBER__wrong_data_type(self):
        line = "b, 16.72m,0000000020Hz,0000023192c,0000000.050s, 025.4C,00007826"

        self.assertRaises(ValueError, self.sqmle._parse_data, data=line, command=READ_WITH_SERIAL_NUMBER)

    def test_parse_data__command_READ_WITH_SERIAL_NUMBER(self):
        line = "r, 16.72m,0000000020Hz,0000023192c,0000000.050s, 025.4C,00007826"

        data = self.sqmle._parse_data(data=line, command=READ_WITH_SERIAL_NUMBER)
        self.assertIsInstance(data, dict)
        self.assertEqual(len(data), 7)
        self.assertIsInstance(data['type'], str)
        self.assertIsInstance(data['magnitude'], u.Quantity)
        self.assertEqual(data['magnitude'].unit, u.mag)
        self.assertIsInstance(data['frequency'], u.Quantity)
        self.assertEqual(data['frequency'].unit, u.Hz)
        self.assertIsInstance(data['period_count'], u.Quantity)
        self.assertEqual(data['period_count'].unit, u.count)
        self.assertIsInstance(data['period_seconds'], u.Quantity)
        self.assertEqual(data['period_seconds'].unit, u.second)
        self.assertIsInstance(data['temperature'], u.Quantity)
        self.assertEqual(data['temperature'].unit, u.C)
        self.assertIsInstance(data['serial_number'], str)

    def test_parse_data__command_REQUEST_CALIBRATION_INFORMATION_wrong_data_format(self):
        line = "c,00000017.60m,0000000.000s, 039.4C,00000008.71m, 039.4C, 12345 "
        self.assertRaises(ValueError, self.sqmle._parse_data, data=line, command=REQUEST_CALIBRATION_INFORMATION)

    def test_parse_data__command_REQUEST_CALIBRATION_INFORMATION_wrong_data_type(self):
        line = "s,00000017.60m,0000000.000s, 039.4C,00000008.71m, 039.4C "
        self.assertRaises(ValueError, self.sqmle._parse_data, data=line, command=REQUEST_CALIBRATION_INFORMATION)

    def test_parse_data__command_REQUEST_CALIBRATION_INFORMATION(self):
        line = "c,00000017.60m,0000000.000s, 039.4C,00000008.71m, 039.4C "
        data = self.sqmle._parse_data(data=line, command=REQUEST_CALIBRATION_INFORMATION)
        self.assertIsInstance(data, dict)
        self.assertEqual(len(data), 6)
        self.assertIsInstance(data['type'], str)
        self.assertIsInstance(data['magnitude_offset_calibration'], u.Quantity)
        self.assertEqual(data['magnitude_offset_calibration'].unit, u.mag)
        self.assertIsInstance(data['dark_period'], u.Quantity)
        self.assertEqual(data['dark_period'].unit, u.second)
        self.assertIsInstance(data['temperature_light_calibration'], u.Quantity)
        self.assertEqual(data['temperature_light_calibration'].unit, u.C)
        self.assertIsInstance(data['magnitude_offset_manufacturer'], u.Quantity)
        self.assertEqual(data['magnitude_offset_manufacturer'].unit, u.mag)
        self.assertIsInstance(data['temperature_dark_calibration'], u.Quantity)
        self.assertEqual(data['temperature_dark_calibration'].unit, u.C)


    def test_parse_data__command_UNIT_INFORMATION_REQUEST_wrong_data_format(self):
        line = "i,00000002,00000003"
        self.assertRaises(ValueError, self.sqmle._parse_data, data=line, command=UNIT_INFORMATION_REQUEST)

    def test_parse_data__command_UNIT_INFORMATION_REQUEST_wrong_data_type(self):
        line = "x,00000002,00000003,00000001,00000413 "
        self.assertRaises(ValueError, self.sqmle._parse_data, data=line, command=UNIT_INFORMATION_REQUEST)

    def test_parse_data__command_UNIT_INFORMATION_REQUEST(self):
        line = "i,00000002,00000003,00000001,00000413 "
        data = self.sqmle._parse_data(data=line, command=UNIT_INFORMATION_REQUEST)
        self.assertIsInstance(data, dict)
        self.assertEqual(len(data), 5)
        self.assertIsInstance(data['type'], str)