Usage
*****

The `DSPP Reader` package provides two console scripts, ``read-sqmle`` and ``read-tessw4c``. They both share similar
arguments options.

You can always starting by getting help with.

.. code-block:: shell

   read-sqmle -h


Will display something very similar to this:

.. code-block:: shell

    usage: read-sqmle [-h] [--site-id SITE_ID] [--site-name SITE_NAME]
                  [--site-latitude SITE_LATITUDE]
                  [--site-longitude SITE_LONGITUDE]
                  [--site-elevation SITE_ELEVATION]
                  [--site-timezone SITE_TIMEZONE]
                  [--sun-altitude SUN_ALTITUDE] [--device-id DEVICE_ID]
                  [--device-altitude DEVICE_ALTITUDE]
                  [--device-azimuth DEVICE_AZIMUTH] [--device-ip DEVICE_IP]
                  [--device-port DEVICE_PORT]
                  [--device-window-correction DEVICE_WINDOW_CORRECTION]
                  [--number-of-reads NUMBER_OF_READS]
                  [--delay-between-reads DELAY_BETWEEN_READS] [--read-always]
                  [--save-to-file] [--save-to-database] [--post-to-api]
                  [--save-files-to SAVE_FILES_TO]
                  [--api-endpoint API_ENDPOINT] [--api-token API_TOKEN]
                  [--file-format {tsv,csv,txt}] [--config-file CONFIG_FILE]
                  [--save-logs-to SAVE_LOGS_TO] [--config-file-example]
                  [--debug]

    SQM-LE reader Version: 0.1.dev82+g756c4f710.d20260811

    options:
      -h, --help            show this help message and exit
      --site-id SITE_ID     A conventional unique site id, for instance, `ctio`,
                            `pachon` or `morado`
      --site-name SITE_NAME
                            Full site name
      --site-latitude SITE_LATITUDE
                            Site latitude
      --site-longitude SITE_LONGITUDE
                            Site longitude
      --site-elevation SITE_ELEVATION
                            Site elevation
      --site-timezone SITE_TIMEZONE
                            Site timezone
      --sun-altitude SUN_ALTITUDE
                            Sun altitude with respect to the horizon. This defines
                            when to start reading.
      --device-id DEVICE_ID
                            Device serial ID
      --device-altitude DEVICE_ALTITUDE
                            Device altitude
      --device-azimuth DEVICE_AZIMUTH
                            Device azimuth
      --device-ip DEVICE_IP
                            Device IP address
      --device-port DEVICE_PORT
                            Device TCP port
      --device-window-correction DEVICE_WINDOW_CORRECTION
                            If an SQM was mounted in housing with acrylic window
                            the correction must be -0.11 mag
      --number-of-reads NUMBER_OF_READS
                            Number of reads to average
      --delay-between-reads DELAY_BETWEEN_READS
                            How many seconds between reads
      --read-always         Allows to ignore the time constraints
      --save-to-file        Save to a plain text file
      --save-to-database    Save to a database
      --post-to-api         Send data through a POST request to a REST API
      --save-files-to SAVE_FILES_TO
                            Destination path to save files
      --api-endpoint API_ENDPOINT
                            API endpoint
      --api-token API_TOKEN
                            API Token
      --file-format {tsv,csv,txt}
                            File format to use
      --config-file CONFIG_FILE
                            Configuration file full path
      --save-logs-to SAVE_LOGS_TO
                            Directory to save logs to
      --config-file-example
                            Print a configuration file example
      --debug               Enable debug mode


Or for TESS-W4C

.. code-block:: shell

   read-tessw4c -h

Will print something like this:

.. code-block:: shell

    usage: read-tessw4c [-h] [--site-id SITE_ID] [--site-name SITE_NAME]
                    [--site-latitude SITE_LATITUDE]
                    [--site-longitude SITE_LONGITUDE]
                    [--site-elevation SITE_ELEVATION]
                    [--site-timezone SITE_TIMEZONE]
                    [--sun-altitude SUN_ALTITUDE] [--device-id DEVICE_ID]
                    [--device-altitude DEVICE_ALTITUDE]
                    [--device-azimuth DEVICE_AZIMUTH] [--device-ip DEVICE_IP]
                    [--device-port DEVICE_PORT]
                    [--delay-between-reads DELAY_BETWEEN_READS]
                    [--read-always] [--save-to-file] [--save-to-database]
                    [--post-to-api] [--save-files-to SAVE_FILES_TO]
                    [--api-endpoint API_ENDPOINT] [--api-token API_TOKEN]
                    [--file-format {tsv,csv,txt}] [--config-file CONFIG_FILE]
                    [--save-logs-to SAVE_LOGS_TO] [--config-file-example]
                    [--debug]

    TESS-W4C reader Version: 0.1.dev82+g756c4f710.d20260811

    options:
      -h, --help            show this help message and exit
      --site-id SITE_ID     A conventional unique site id, for instance, `ctio`,
                            `pachon` or `morado`
      --site-name SITE_NAME
                            Full site name
      --site-latitude SITE_LATITUDE
                            Site latitude
      --site-longitude SITE_LONGITUDE
                            Site longitude
      --site-elevation SITE_ELEVATION
                            Site elevation
      --site-timezone SITE_TIMEZONE
                            Site timezone
      --sun-altitude SUN_ALTITUDE
                            Sun altitude with respect to the horizon. This defines
                            when to start reading.
      --device-id DEVICE_ID
                            Device serial ID
      --device-altitude DEVICE_ALTITUDE
                            Device altitude
      --device-azimuth DEVICE_AZIMUTH
                            Device azimuth
      --device-ip DEVICE_IP
                            Device IP address
      --device-port DEVICE_PORT
                            Device TCP port
      --delay-between-reads DELAY_BETWEEN_READS
                            How many seconds between reads
      --read-always         Allows to ignore the time constraints
      --save-to-file        Save to a plain text file
      --save-to-database    Save to a database
      --post-to-api         Send data through a POST request to a REST API
      --save-files-to SAVE_FILES_TO
                            Destination path to save files
      --api-endpoint API_ENDPOINT
                            API endpoint
      --api-token API_TOKEN
                            API Token
      --file-format {tsv,csv,txt}
                            File format to use
      --config-file CONFIG_FILE
                            Configuration file full path
      --save-logs-to SAVE_LOGS_TO
                            Directory to save logs to
      --config-file-example
                            Print a configuration file example
      --debug               Enable debug mode


Each argument will be described in more detail later. Keep in mind that although the best effort is made to
keep this documentation in sync with respect to the code, there is a small chance that they will not match, so always trust
the console's print and use this as a reference.

In both cases you can use a configuration file or pass the options by command line arguments, the command line arguments
can be used to override the configuration files.

In order to create a configuration file you have the command line argument ``--config-file-example`` so I would use it as follows
(the same applies for ``read-tessw4c``):

.. note::

  The configuration file must be in yaml.

.. code-block:: shell

  read-sqmle --config-file-example

This will print the content to the terminal, but in order to save it to a file we have to do the following:


.. code-block:: shell

  read-sqmle --config-file-example > config.yaml

Which later can be used with the ``--config-file`` flag.

.. code-block:: shell

  read-sqmle --config-file config.yaml




SQM-LE
^^^^^^

.. code-block:: yaml

    # Add this to a .yaml file, reference it later with --config-file <file_name>.yaml
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
    delay_between_reads: 30
    read_always: false
    save_to_file: true
    save_to_database: false
    post_to_api: false
    save_files_to: <some-path-where-it-is-allowed-to-write>
    api_endpoint: http://localhost:8000/api/sqm-le
    api_token: <get-an-appropriate-api-token>
    file_format: tsv
    save_logs_to: null



TESS-W4C
^^^^^^^^

.. code-block:: yaml

    # Add this to a .yaml file, reference it later with --config-file <file_name>.yaml
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
    delay_between_reads: 30
    read_always: false
    save_to_file: true
    save_to_database: false
    post_to_api: false
    save_files_to:  <some-path-where-it-is-allowed-to-write>
    api_endpoint: http://localhost:8000/api/tess-w4c
    api_token: <get-an-appropriate-api-token>
    file_format: tsv
    save_logs_to: null


.. note::

    If you just want to test the device, the critical parameters to set are the **IP** address, the **PORT**, the
    device **TYPE** and device **ID**.

Use as a class
^^^^^^^^^^^^^^

If you want to control the acquisition of parameters or write your custom parser you can import the respective class and
use all the power of class inheritance, method override and so on.

This is how you can import the respective class once the package is installed.

.. code-block:: python

   # for SQM-LE
   from dspp_reader.sqmle.sqmle import SQMLE

   # for TESS-W4C
   from dspp_reader.tessw4c import TESSW4C