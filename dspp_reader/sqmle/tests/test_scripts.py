from unittest.mock import patch

from dspp_reader.sqmle.scripts import read_sqmle
from dspp_reader.sqmle.scripts import CONFIG_FIELDS_DEFAULT

@patch('dspp_reader.sqmle.scripts.read_device')
def test_read_sqmle(mock_read_device):

    read_sqmle()

    mock_read_device.assert_called_once_with(
        device_type='sqm-le',
        config_fields_default=CONFIG_FIELDS_DEFAULT,
        args=None
    )

