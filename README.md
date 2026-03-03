# Dark Sky Protection Photometers Reader

[![Upload Python Package](https://github.com/dark-sky-protection/dspp_reader/actions/workflows/python-publish.yml/badge.svg)](https://github.com/dark-sky-protection/dspp_reader/actions/workflows/python-publish.yml)
[![Documentation Status](https://readthedocs.org/projects/dspp-reader/badge/?version=latest)](https://dspp-reader.readthedocs.io/en/latest/?badge=latest)
![PyPI - Version](https://img.shields.io/pypi/v/dspp-reader)



# Overview

This package implements two console scripts `read-sqmle` and `read-tessw4c`

Those scripts implement very similar arguments. Use `--help` to get a list of usable arguments

The recommended way to make it work is through a configuration file, in order to create a configuration
file use `--config-file-example` and to use an existing configuration file use `--config-file <path-to-file.yaml>`


# Configuration file example

>[!NOTE]
>This is not updated automatically, so always rely on `--config-file-example`

For TESS-W4C devices
```yaml
site_id: ctio
site_name: Cerro Tololo
site_latitude: -30.169166
site_longitude: -70.804
site_elevation: 2174
site_timezone: America/Santiago
sun_altitude: -10
device_type: tess-w4c
device_id: stars1823
device_altitude: 45
device_azimuth: 0
device_ip: 0.0.0.0
device_port: 32
reads_frequency: 30
read_all_the_time: false
save_to_file: true
save_to_database: false
post_to_api: false
save_files_to: /path/to/where/to/save/the/data
api_endpoint: http://<hostname>/api/tess-w4c
api_token: <get-an-appropriate-api-token>
file_format: tsv
```

For SQM-LE devices
```yaml
site_id: ctio
site_name: Cerro Tololo
site_latitude: -30.169166
site_longitude: -70.804
site_elevation: 2174
site_timezone: America/Santiago
sun_altitude: -10
device_type: sqm-le
device_id: '1823'
device_altitude: 45
device_azimuth: 0
device_ip: 0.0.0.0
device_port: 10001
device_window_correction: -0.11
number_of_reads: 5
reads_frequency: 30
read_all_the_time: false
save_to_file: true
save_to_database: false
post_to_api: false
save_files_to:  /path/to/where/to/save/the/data
api_endpoint: http://<hostname>/api/sqm-le
api_token: <get-an-appropriate-api-token>
file_format: tsv
```
