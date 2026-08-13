Data Format
***********

We aimed to implement a simple and time-resistant format.

.. note::

    After only finding mentions about a standard for storing sky brightness data we came a across `this document that
    describes a standard <https://darksky.org/app/uploads/bsk-pdf-manager/47_SKYGLOW_DEFINITIONS.PDF>`_ but we don't
    comply to it since it was too late for our release.

Files
^^^^^
By default the data will be saved to files.

SQM-LE
++++++

.. code-block:: text
    :caption: Slide sideways to see all the content.

    # Filename /full/path/to/data/20260310_sqmle_7281.tsv
    # magnitude: mag
    # frequency: Hz
    # period_count: ct
    # period_seconds: s
    # temperature: C
    # latitude: deg
    # longitude: deg
    # elevation: m
    # type	magnitude	frequency	period_count	period_seconds	temperature	serial_number	timestamp	localtime	altitude	azimuth	site	timezone	latitude	longitude	elevation
    r	16.310000000000002	24.0	18638.0	0.04	24.4	7281	2026-03-10T23:47:23.753685+00:00	2026-03-10T20:47:23.753685-03:00	90	90	pachon	America/Santiago	-30.240816	-70.738094	2681.0
    r	16.38	23.0	19955.0	0.043	24.4	7281	2026-03-10T23:47:49.837998+00:00	2026-03-10T20:47:49.837998-03:00	90	90	pachon	America/Santiago	-30.240816	-70.738094	2681.0

TESS-W4C
++++++++

Since TESS-W4C data contains nested dictionaries, in order to save it to a plain text file, it was necessary to
*flatten* the data. i.e. express it in one line.

.. code-block:: text
    :caption: Slide sideways to see all the content.

    # File name: /full/path/to/data/20260602_tess-w4c_stars1567.tsv
    # udp	rev	name	wdBm	hash	ain	F1_freq	F1_mag	F1_zp	F2_freq	F2_mag	F2_zp	F3_freq	F3_mag	F3_zp	F4_freq	F4_mag	F4_zp	tamb	tsky	timestamp	localtime	device	serial_number	altitude	azimuth	site	timezone	latitude	longitude	elevation
    542411	3	stars1567	-54	22C	489	111111.1	7.35	19.96	111111.1	7.43	20.04	76923.1	7.77	19.99	62500.0	7.95	19.94	14.83	-10.23	2026-06-02T21:46:00.605719+00:00	2026-06-02T21:46:00.605719+00:00	tess-w4c	stars1567	30	304	ctio	America/Santiago	-30.1688 deg	-70.8061 deg	2207.0 m
    542427	3	stars1567	-54	22C	474	111111.1	7.35	19.96	111111.1	7.43	20.04	125000.0	7.25	19.99	100000.0	7.44	19.94	14.81	-10.27	2026-06-02T21:46:31.981099+00:00	2026-06-02T21:46:31.981099+00:00	tess-w4c	stars1567	30	304	ctio	America/Santiago	-30.1688 deg	-70.8061 deg	2207.0 m

For API
^^^^^^^

The API receives data in JSON format, below is an example of one payload for each type of instrument. In this case the API
is a little bit more than an interface to the database.

For SQM-LE
++++++++++

.. code-block:: text

    {
        "type": "r",
        "magnitude": 21.39,
        "frequency": 146.0,
        "period_count": 23192.0,
        "period_seconds": 0.05,
        "temperature": 25.4,
        "timestamp": "2025-12-12T19:54:01.704865+00:00",
        "device": {
            "type": "sqm-le",
            "serial_number": "7826",
            "altitude": 45,
            "azimuth": 0,
            "site": {
                "id": "ctio",
                "name": "Cerro Tololo",
                "latitude": -30.169166,
                "longitude": -70.804,
                "elevation": 2174.0,
                "timezone": "America/Santiago"
            }
        }
    }

For TESS-W4C
++++++++++++

.. code-block:: text

    {
        "message_id": "617831",
        "timestamp": "2025-12-12T19:54:01.704865+00:00",
        "localtime": "2025-12-12T16:54:01.704865",
        "photometer_1": {
            "frequency": 90000.0,
            "magnitude": 8.58,
            "zeropoint": 20.97
        },
        "photometer_2": {
            "frequency": 11111.1,
            "magnitude": 7.45,
            "zeropoint": 20.06
        },
        "photometer_3": {
            "frequency": 90000.0,
            "magnitude": 6.99,
            "zeropoint": 20.97
        },
        "photometer_4": {
            "frequency": 90000.0,
            "magnitude": 8.58,
            "zeropoint": 19.85
        },
        "ambient_temperature": 29.13,
        "sky_temperature": -17.55,
        "device": {
            "type": "tess-w4c",
            "serial_number": "stars1402",
            "altitude": 45,
            "azimuth": 0,
            "site": {
                "id": "ctio",
                "name": "Cerro Tololo",
                "latitude": -30.169166,
                "longitude": -70.804,
                "elevation": 2174.0,
                "timezone": "America/Santiago"
            }
        }
    }