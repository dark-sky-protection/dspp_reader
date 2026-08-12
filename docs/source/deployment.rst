Large Scale Deployment
**********************

This section, more than a Step-by-step guide is a suggestion, it must be adapted to your needs. This scenario is the
most complex case.

.. important::

    We describe several components that must be developed and maintained independently. This document focuses on what's
    related to the **dspp_reader** package.

Components
^^^^^^^^^^

Photometers:

Photometers distributed across several geographical locations and since they are *queried*, the reading can be
centralized, provided they are accessible.

Reader:

This is where this package will work. It can be the last step of the process or an intermediate one before storing the
data in a database.

Database & API:

The data is stored in a database, the database is not directly exposed, the data is POSTed to an API's endpoint with
authentication, data validation and data augmentation.

Dashboard:

A dashboard is necessary for visualizing trends and statuses.

Organization
^^^^^^^^^^^^

We'll start by describing how to organize the files in the server. Let's define our root folder on the server as
``/home/dspp/`` we'll create the following structure of folders inside it:

.. note::

    For simplicity we'll assume this server is dedicated only to this project. Feel free to reorganize according to
    your own system.

.. code-block:: shell

    project_setup/
        readers/
            production/
                .env
                compose.yaml
        config/
            sqmle/
                7826.yaml
                7826.yaml
                <...>.yaml
            tessw4c/
                1396.yaml
                1397.yaml
                <...>.yaml

We will also need to create a folder structure to organize the data produced.

.. code-block:: shell


    data/
        sqmle/
            7826/
            7827/
            <...>/
        tessw4c/
            1396/
            1397/
            <...>/


.. note::

    In the examples above the numbers (**7826** or **1396**) are the serial id of the devices, feel free to give them
    names if you wish but be consistent.


Configuration Files
^^^^^^^^^^^^^^^^^^^

In this case we'll be showing the *configuration file* for the device **7826**, if we had one device we would call it
``config.yaml`` but we assumed we had several devices, so we'll use ``7826.yaml`` or even better ``ctio_7826.yaml``.
The same logic applies for the *tess w4c* devices.

.. important::

    In the case of ``site_id`` we decided not to enforce a give id per site, just define it very clearly, for instance
    we have ``ctio``, ``morado`` or ``pachon``.


.. code-block:: yaml

    site_id: ctio
    site_name: Cerro Tololo
    site_timezone: America/Santiago
    site_latitude: -30.169166
    site_longitude: -70.804
    site_elevation: 2174
    sun_altitude: -10
    device_type: sqmle
    device_id: 7826
    device_altitude: 45
    device_azimuth: 0
    device_ip: '192.168.1.101'
    device_port: 10001
    device_window_correction: -0.11
    number_of_reads: 1
    reads_frequency: 30
    read_all_the_time: false
    save_to_file: true
    save_to_database: false
    post_to_api: true
    save_files_to: /home/dspp/data/
    api_endpoint: http://localhost:8000/api/sqm-le
    api_token: <add-api-token-here>
    file_format: tsv


.. note::

    It might appear that the path in ``save_files_to`` is wrong, but is not. This path is relative the docker container
    which then is mapped to the host in the Orchestration_ part.

Docker
^^^^^^

In order to virtualize using Docker we need to create a *docker image* which is then used as the starting template to
create the *containers* which are the running instances.

Save the following content on a file named ``Dockerfile``.

.. code-block:: dockerfile

    FROM python:3.13-slim
    ENV PYTHONUNBUFFERED=1
    RUN apt-get update

    RUN addgroup --gid 1057 dspp
    RUN useradd --create-home -u 1057 -g dspp -ms /bin/bash dspp
    RUN pip install --upgrade pip

    USER dspp
    WORKDIR /home/dspp
    ENV PATH="/home/dspp/.local/bin:${PATH}"

    COPY --chown=1057:1057 . .
    RUN pip install --user -r requirements.txt

    # This should be overwritten with the appropriate command for TESS-W4C
    # Alternatively create another docker image
    CMD ["read-sqmle", "--config-file", "/home/dspp/config/config.yaml"]

Before creating the docker image we need to define a ``requirements.txt`` file which will be placed in the same folder
as the ``Dockerfile``.

.. code-block:: plaintext

    dspp-reader==1.0.0

.. note::

    Don't forget to check what is the actual latest version of the package.

After you have all that, from the same directory we'll run the following command:

.. code-block:: shell

    docker build . -t dspp-reader:1.0.0

Ideally this should be automated but for now it'll do.

Orchestration
^^^^^^^^^^^^^

Until now we have been just gathering the building blocks and now the fun begins.

The orchestration is defined in a file named ``compose.yaml``. To demonstrate the power of ``docker compose`` we will
present made up instrument in different locations.

.. code-block:: yaml

    services:
      sqmle-pachon-7826:
        image: dspp-reader:1.0.0
        container_name: sqmle-pachon-7826
        restart: unless-stopped
        volumes:
          - ./config/config/sqmle/7826.yaml:/home/dspp/config/config.yaml:ro
          - ./data/sqmle/7826:/home/dspp/data/:rw
        command: ["read-sqmle", "--config-file", "/home/dspp/config/config.yaml"]
      sqmle-tololo-7827:
        image: dspp-reader:1.0.0
        container_name: sqmle-tololo-7827
        restart: unless-stopped
        volumes:
          - ./config/config/sqmle/7827.yaml:/home/dspp/config/config.yaml:ro
          - ./data/sqmle/7827:/home/dspp/data:rw
        command: ["read-sqmle", "--config-file", "/home/dspp/config/config.yaml"]
      tessw4c-morado-1396:
        image: dspp-reader:1.0.0
        container_name: tessw4c-morado-1396
        restart: unless-stopped
        volumes:
          - ./config/config/tessw4c/1396.yaml:/home/dspp/config/config.yaml:ro
          - ./data/tessw4c/1396:/home/dspp/data:rw
        command: ["read-tessw4c", "--config-file", "/home/dspp/config/config.yaml"]
      tessw4c-kpno-1397:
        image: dspp-reader:1.0.0
        container_name: tessw4c-kpno-1397
        restart: unless-stopped
        volumes:
          - ./config/config/tessw4c/1397.yaml:/home/dspp/config/config.yaml:ro
          - ./data/tessw4c/1397:/home/dspp/data:rw
        command: ["read-tessw4c", "--config-file", "/home/dspp/config/config.yaml"]
      # repeat as needed

.. important::

    Notice that here we are reusing the same image for all the services/photometers and overriding the command to
    specify a different shell script. The configuration file name is the same inside every container because we are
    mapping them to the same name. This comes from the idea that there could be a different image for each type of
    detector, in which case we could avoid to override the command, either way is valid.


Start & Stop Services
^^^^^^^^^^^^^^^^^^^^^

To start all the services use:

.. code-block:: shell

    docker compose up -d

To stopp al the services use:

.. code-block:: shell

    docker compose stop

If you named your compose file other than ``compose.yaml`` you can specify it with the ``-f`` options:

.. code-block:: shell

    docker compose -f custom_compose_file_name.yaml up -d