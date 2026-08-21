from unittest.mock import patch

from dspp_reader.tessw4c.scripts import read_tessw4c
from dspp_reader.tessw4c.scripts import CONFIG_FIELDS_DEFAULT

@patch('dspp_reader.tessw4c.scripts.read_device')
def test_read_tessw4c(mock_read_device):

    read_tessw4c()

    mock_read_device.assert_called_once_with(
        device_type='tess-w4c',
        config_fields_default=CONFIG_FIELDS_DEFAULT,
        args=None
    )

