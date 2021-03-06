"""
Provide 'drivers' for the various hardware peripherals the drone can have.

This currently only has the AirSensor object, the RF sensor object should
probably be merged into this file, or this file should be renamed.
"""
import threading
from threading import Thread
import json
import random
import math
import serial
import time
import drone_control
import dronekit
from subprocess import Popen, PIPE, call
import sys
from pubsub import pub
    

class AirSensor(threading.Thread):
    """Provide an interface to Christine/Michael's air sensor.

    This class can either connect to an existing air sensor plugged into one of
    the drone's RPi's USB ports or it can generate fake CO2 readings. It
    inherits from python's threading.Thread class and should probably always be
    a daemon.

    """

    def __init__(self, simulated=False):
        """Construct an instance of the AirSensor class.

        simulated -- Whether or not to connect to a real air sensor
        """
        super(AirSensor, self).__init__()
        self.daemon = True
        self._simulated = simulated
        self._delay = 5
        self._serial_speed = 9600
        self._serial_port = '/dev/ttyACM0'
        self._timeout = 1
        self._connection = None
        self.filewrite = False
        self.callback = False
        if not self._simulated:
            self.connect_to_sensor()
            print("connected to air")
        self.start()

    def connect_to_sensor(self):
        """Connect to an air sensor and prepare it for reading data. Should add
        ability to take exception if unable to connect and print error msg"""
        try:
            self._connection = serial.Serial(
                    self._serial_port,
                    self._serial_speed,
                    timeout= self._timeout
            )
            # Ask Michael about why this is necessary
            self._connection.write('{"usb_en":true}')
            # time.sleep(0.01)
            self._connection.write('{"co2_en":true}')
        except serial.serialutil.SerialException as e:
            sys.stderr.write("Could not open serial for RealAirSensor\n")
            sys.stderr.write(e.__repr__())

    def filewrite_callback(self):
        """Publish air sensor data on the appropriate PyPubSub topic."""
        #pub.sendMessage("sensor-messages.air-data", arg1=air_data)
        self.filewrite = True

    def end_callback(self):
        self.callback = True

    def run(self):
        """Gather and publish data periodically while the thread is alive."""
        if not self._simulated:
            if self._connection is None:
                print("DEBUG: no air conn.")
                return
            while(True):
                data = self.get_reading()
                if data is not None:
                    #print "Got air sensor reading: {}".format(data)
                    self._callback(data)
                else:
                    print("DEBUG: no air data")
        else:
            while(True):
                data = self.generate_fake_reading()
                #print "Got air sensor reading: {}".format(data)
                self._callback(data)
                time.sleep(self._delay / drone_control.Pilot.sim_speedup)

    def get_reading(self):
        """Get a reading from the air sensor and return it."""
        while True:
            with open('air_quality', "w+") as f_air:

                if self.callback:
                    break

                while not self.filewrite:
                    time.sleep(0.1)

                self.filewrite = False

                latest_raw = self._connection.readline()
                if latest_raw:
                    try:
                        readings = json.loads(latest_raw)
                        f_air.write(readings)

                    except Exception as e:
                        print "JSON error"
                        return None
		return readings

    def generate_fake_reading(self):
        """Generate a fake CO2 reading.

        This will generate mostly ~410, occasionally higher values.
        """
        raw = random.expovariate(1)
        reading = max(raw, 2) * 200 + random.uniform(5, 15)
        reading_dict = {"CO2":reading}
        return reading_dict
