import datetime
import os.path
import socket

import logging
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger("sqm")

READ = b'rx\r\n'
READ_WITH_SERIAL_NUMBER = b'Rx\r\n'
REQUEST_CALIBRATION_INFORMATION = b'cx\r\n'
UNIT_INFORMATION_REQUEST = b'ix\r\n'


class SQM(object):
    def __init__(self,
                 ip,
                 port=10001,
                 number_of_reads=3,
                 reads_frequency=30,
                 serial_number=None,
                 save_to_file=True,
                 save_to_database=False,
                 post_to_api=False):
        self.ip = ip
        self.port = port
        self.number_of_reads = number_of_reads
        self.reads_frequency = reads_frequency
        self.serial_number = serial_number
        self.save_to_file = save_to_file
        self.save_to_database = save_to_database
        self.post_to_api = post_to_api
        self.data = None

    def __call__(self, *args, **kwargs):
        self.read()

        if self.save_to_file:
            self._write_to_txt()
        if self.save_to_database:
            self._write_to_database()
        if self.post_to_api:
            self._post_to_api()

    def read_looping(self):
        try:
            pass
        except KeyboardInterrupt:
            logger.info("Closing connection on request")

    def read(self):
        with socket.create_connection((self.ip, self.port), timeout=5) as sock:
            self.data = self._send_command(command=READ_WITH_SERIAL_NUMBER, sock=sock)

            logger.info(f"Response: {self.data}")

            parsed_data = self._parse_data(command=READ_WITH_SERIAL_NUMBER)

            if self.serial_number:
                logger.info(f"Serial number: {self.serial_number}")
                if self.serial_number != parsed_data['serial_number']:
                    logger.warning(f"Serial number mismatch: {self.serial_number} != {parsed_data['serial_number']}")
            else:
                self.serial_number = parsed_data['serial_number']
            for d in parsed_data:
                print(d)

    def _send_command(self, command, sock):
        sock.sendall(command)
        data = sock.recv(1024)
        return data.decode()

    def _parse_data(self, command):
        data =  self.data.split(',')
        if command == READ:
            return {
                'type': data[0],
                'magnitude': float(data[1]),
                'frequency': float(data[2]),
                'period_count': float(data[3]),
                'period_seconds': float(data[4]),
                'temperature': float(data[5])
            }
        elif command == READ_WITH_SERIAL_NUMBER:
            return {
                'type': data[0],
                'magnitude' : float(data[1]),
                'frequency' : float(data[2]),
                'period_count' : float(data[3]),
                'period_seconds' : float(data[4]),
                'temperature' : float(data[5]),
                'serial_number' : data[6],
            }
        elif command == REQUEST_CALIBRATION_INFORMATION:
            return {
                'type': data[0],
                'magnitude_offset_calibration': float(data[1]),
                'dark_period': float(data[2]),
                'temperature_light_calibration': float(data[3]),
                'magnitude_offset_manufacturer': float(data[4]),
                'temperature_dark_calibration': float(data[5]),
            }
        elif command == UNIT_INFORMATION_REQUEST:
            return {
                'type': data[0],
                'protocol_number': data[1],
                'model_number': data[2],
                'feature_number': data[3],
                'serial_number': data[4],
            }
        else:
            logger.error(f"Unknown command: {command}")
            return data





    def _write_to_txt(self):
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        output_file = f"{date}_{self.serial_number or 0000}.txt"

        with open(output_file, "wb") as f:
            print(os.path.exists(output_file))
            f.write(self.data)

    def _write_to_database(self):
        pass

    def _post_to_api(self):
        pass
