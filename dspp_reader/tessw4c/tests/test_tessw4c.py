import datetime
import json
import os
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch, MagicMock

import requests
from freezegun import freeze_time
from dspp_reader.tessw4c import TESSW4C
from dspp_reader.tools import augment_data
from dspp_reader.tools.generics import clean_data


class TestTESSW4C(TestCase):

    files_to_remove = []

    def setUp(self):
        self.tessw4c = TESSW4C(
            site_id='site',
            site_name="Site Name",
            site_timezone="America/Santiago",
            site_latitude=-30.169166,
            site_longitude=-30.169166,
            site_elevation=2174,
            sun_altitude=-10,
            device_type="tessw4c",
            device_id='0000',
            device_altitude=0,
            device_azimuth=0,
            device_ip='0.0.0.0',
            device_port=23,
            delay_between_reads=30,
            read_always=False,
            save_to_file=True,
            save_to_database=False,
            post_to_api=False,
            save_files_to=Path(os.getcwd()),
            api_endpoint='http://localhost:8080/sqmle',
            api_token='',
            file_format='tsv'
        )
        self.tessw4c_data = {
            "udp": 617831,
            "rev": 3,
            "name": "stars1402",
            "wdBm": -63,
            "hash": "D30",
            "ain": 501,
            "F1": {
                "freq": 90000.0,
                "mag": 8.58,
                "zp": 20.97
            },
            "F2": {
                "freq": 11111.1,
                "mag": 7.45,
                "zp": 20.06
            },
            "F3": {
                "freq": 90000.0,
                "mag": 6.99,
                "zp": 20.97
            },
            "F4": {
                "freq": 90000.0,
                "mag": 8.58,
                "zp": 19.85
            },
            "tamb": 29.13,
            "tsky": -17.55
        }

    def tearDown(self):
        for f in self.files_to_remove:
            if f.exists():
                f.unlink()

    def test_tessew4c(self):
        self.assertIsInstance(self.tessw4c, TESSW4C)

    def test_get_header(self):
        filename = f"tessw4c_filename.tsv"
        expected_header = f"# File name: {filename}\n# udp\trev\tname\twdBm\thash\tain\tF1_freq\tF1_mag\tF1_zp\tF2_freq\tF2_mag\tF2_zp\tF3_freq\tF3_mag\tF3_zp\tF4_freq\tF4_mag\tF4_zp\ttamb\ttsky\n"
        header = self.tessw4c._get_header(data=self.tessw4c_data, filename=filename)
        self.assertEqual(header, expected_header)

    def test_get_line_for_plain_text(self):
        expected_line = "617831\t3\tstars1402\t-63\tD30\t501\t90000.0\t8.58\t20.97\t11111.1\t7.45\t20.06\t90000.0\t6.99\t20.97\t90000.0\t8.58\t19.85\t29.13\t-17.55\n"
        line = self.tessw4c._get_line_for_plain_text(data=self.tessw4c_data)
        self.assertEqual(line, expected_line)

    @freeze_time("2026-08-20 12:00:00", tz_offset=0)
    def test_write_to_file(self):
        expected_filename = Path(os.getcwd()) / "20260820_tessw4c_stars1402.tsv"
        self.tessw4c._write_to_file(data=self.tessw4c_data)

        self.assertTrue(os.path.isfile(expected_filename))
        self.files_to_remove.append(expected_filename)

    def test_write_to_database(self):
        self.assertRaises(NotImplementedError, self.tessw4c._write_to_database, data=self.tessw4c_data)

    @patch('dspp_reader.tessw4c.tessw4c.sleep')
    @patch('dspp_reader.tessw4c.tessw4c.requests.post')
    def test_post_to_api__success(self, mock_post, mock_sleep):
        mock_post.return_value = MagicMock(status_code=201)

        augmented_data = augment_data(data=self.tessw4c_data, timestamp=datetime.datetime.now(datetime.UTC), device=self.tessw4c.device)

        self.tessw4c._post_to_api(data=augmented_data)

        mock_post.assert_called_once()
        mock_sleep.assert_not_called()

    @patch('dspp_reader.tessw4c.tessw4c.sleep')
    @patch('dspp_reader.tessw4c.tessw4c.requests.post')
    def test_post_to_api__error_status_code(self, mock_post, mock_sleep):
        mock_post.return_value = MagicMock(status_code=500)

        augmented_data = augment_data(data=self.tessw4c_data, timestamp=datetime.datetime.now(datetime.UTC), device=self.tessw4c.device)

        self.tessw4c._post_to_api(data=augmented_data)

        self.assertEqual(mock_post.call_count, 5)
        self.assertEqual(mock_sleep.call_count, 5)

    @patch('dspp_reader.tessw4c.tessw4c.sleep')
    @patch('dspp_reader.tessw4c.tessw4c.requests.post')
    def test_post_to_api__connection_error(self, mock_post, mock_sleep):
        mock_post.side_effect = requests.exceptions.ConnectionError("error")

        augmented_data = augment_data(data=self.tessw4c_data, timestamp=datetime.datetime.now(datetime.UTC), device=self.tessw4c.device)

        self.tessw4c._post_to_api(data=augmented_data)

        self.assertEqual(mock_post.call_count, 5)
        self.assertEqual(mock_sleep.call_count, 5)

    @freeze_time("2026-08-20 12:00:00", tz_offset=0)
    def test_organize_for_api(self):
        augmented_data = augment_data(
            data=self.tessw4c_data,
            timestamp=datetime.datetime.now(datetime.UTC),
            device=self.tessw4c.device)

        cleaned_data = clean_data(augmented_data)

        organized_data = self.tessw4c._organize_for_api(data=cleaned_data)

        self.assertIsInstance(organized_data, dict)

        try:
            json.dumps(organized_data)
        except (TypeError, ValueError) as e:
            self.fail(f"The result is not JSON serializable: {e}")
