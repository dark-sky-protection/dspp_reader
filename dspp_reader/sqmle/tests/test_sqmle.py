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

    def test_average_data__no_data(self):
        self.assertRaises(ValueError, self.sqmle._average_data, measurements=[], command=READ_WITH_SERIAL_NUMBER)

    def test_average_data__command_unknown(self):
        self.assertRaises(NotImplementedError, self.sqmle._average_data, measurements=[{}, {}], command=b'ls\r\n')

    def test_average_data__command_READ(self):
        measurements = [
            {
                'type': 'r',
                'magnitude': 1 * u.mag,
                'frequency': 100 * u.Hz,
                'period_count': 5 * u.count,
                'period_seconds': 10 * u.second,
                'temperature': 20 * u.C,
            },
            {
                'type': 'r',
                'magnitude': 3 * u.mag,
                'frequency': 300 * u.Hz,
                'period_count': 7 * u.count,
                'period_seconds': 20 * u.second,
                'temperature': 22 * u.C,

            }]
        data = self.sqmle._average_data(measurements=measurements, command=READ)
        self.assertIsInstance(data, dict)

    def test_average_data__command_READ__multiple_data_type(self):
        measurements = [
            {
                'type': 'r',
                'magnitude': 1 * u.mag,
                'frequency': 100 * u.Hz,
                'period_count': 5 * u.count,
                'period_seconds': 10 * u.second,
                'temperature': 20 * u.C,
            },
            {
                'type': 'c',
                'magnitude': 3 * u.mag,
                'frequency': 300 * u.Hz,
                'period_count': 7 * u.count,
                'period_seconds': 20 * u.second,
                'temperature': 22 * u.C,

            }]
        self.assertRaises(ValueError, self.sqmle._average_data, measurements=measurements, command=READ)

    def test_average_data__command_READ_WITH_SERIAL_NUMBER(self):
        measurements = [
            {
                'type': 'r',
                'magnitude': 1 * u.mag,
                'frequency': 100 * u.Hz,
                'period_count': 5 * u.count,
                'period_seconds': 10 * u.second,
                'temperature': 20 * u.C,
                'serial_number': '12345'
            },
            {
                'type': 'r',
                'magnitude': 3 * u.mag,
                'frequency': 300 * u.Hz,
                'period_count': 7 * u.count,
                'period_seconds': 20 * u.second,
                'temperature': 22 * u.C,
                'serial_number': '12345'
            }]
        data = self.sqmle._average_data(measurements=measurements, command=READ_WITH_SERIAL_NUMBER)
        self.assertIsInstance(data, dict)

    def test_average_data__command_READ_WITH_SERIAL_NUMBER__multiple_serial_number(self):
        measurements = [
            {
                'type': 'r',
                'magnitude': 1 * u.mag,
                'frequency': 100 * u.Hz,
                'period_count': 5 * u.count,
                'period_seconds': 10 * u.second,
                'temperature': 20 * u.C,
                'serial_number': '12345'
            },
            {
                'type': 'r',
                'magnitude': 3 * u.mag,
                'frequency': 300 * u.Hz,
                'period_count': 7 * u.count,
                'period_seconds': 20 * u.second,
                'temperature': 22 * u.C,
                'serial_number': '54321'
            }]
        self.assertRaises(ValueError, self.sqmle._average_data, measurements=measurements, command=READ_WITH_SERIAL_NUMBER)


    def test_average_data__command_REQUEST_CALIBRATION_INFORMATION(self):
        self.assertRaises(NotImplementedError, self.sqmle._average_data, measurements=[{}, {}], command=REQUEST_CALIBRATION_INFORMATION)

    def test_average_data__command_UNIT_INFORMATION_REQUEST(self):
        self.assertRaises(NotImplementedError, self.sqmle._average_data, measurements=[{}, {}], command=UNIT_INFORMATION_REQUEST)

    def test_get_header(self):
        filename = 'test_file.tsv'
        data = {
            'type': 'r',
            'magnitude': 1 * u.mag,
            'frequency': 100 * u.Hz,
            'period_count': 5 * u.count,
            'period_seconds': 10 * u.second,
            'temperature': 20 * u.C,
            'serial_number': '12345'
        }
        expected_header = "# Filename test_file.tsv\n# magnitude: mag\n# frequency: Hz\n# period_count: ct\n# period_seconds: s\n# temperature: C\n# type\tmagnitude\tfrequency\tperiod_count\tperiod_seconds\ttemperature\tserial_number\n"
        header = self.sqmle._get_header(data=data, filename=filename)
        self.assertIsInstance(header, str)
        self.assertEqual(header, expected_header)

    def test_get_line_for_plain_text(self):
        data = {
            'type': 'r',
            'magnitude': 1 * u.mag,
            'frequency': 100 * u.Hz,
            'period_count': 5 * u.count,
            'period_seconds': 10 * u.second,
            'temperature': 20 * u.C,
            'serial_number': '12345'
        }
        expected_line = "r\t1.0\t100.0\t5.0\t10.0\t20.0\t12345\n"
        line = self.sqmle._get_line_for_plain_text(data=data)
        self.assertIsInstance(line, str)
        self.assertEqual(line, expected_line)
