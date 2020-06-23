import serial
import serial.tools.list_ports
import abc
import matplotlib.pyplot as plt
import matplotlib.animation as anime
from tkinter import *
import asyncio
from datetime import datetime

ser = serial.Serial('COM3', 9600, timeout=0)

PPMuart = []
PPMpwm = []
timestamp = []
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
plt.title('CO2 concentration over Time')


def current_time():
    return datetime.now()


"""
create every types of sensor
"""
class SensorFactory:
    def create_MHZ14A(self):
        return MHZ14A()


class Sensor(metaclass=abc.ABCMeta):
    """
    this is the base class for every sensor
    """

    @abc.abstractmethod
    def calibrate(self):
        """
        :return: this function is not implemented yet
        """
        return NotImplemented

    @abc.abstractmethod
    def interface(self):
        """
        :return: this function is not implemented yet
        """
        return NotImplemented

    @abc.abstractmethod
    def animate(self):
        return NotImplemented


class MHZ14A(Sensor):
    """
    this sensor can detect the concentration of carbon-dioxide.
    the data will be transmitted directly by UART interface
    """
    keywords = ["b'PPMuart:", "PPMpwm:", "start:"]

    def __init__(self):
        self.serial = None
        self.PPM_pwm  = []
        self.PPM_uart = []
        self.serial_en  = True
        self.pwm_en     = True

    def calibrate(self):

    def interface(self):
        """
        need to check the Serial interface is connected or not
        usually arduino use port 3
        :return:
        """
        my_ports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
        arduino_port = [port for port in my_ports if 'COM3' in port][0]
        self.serial = serial.Serial(arduino_port, 9600, timeout=0)

    def animate(self):

    def store(self):

    def create_plot(self):



def animate(i):
    avai = ser.in_waiting
    if avai > 0:
        data = ser.readline()
        data=str(data)
      data_from_sensor = data.split()
      for pos, x in enumerate(data_from_sensor):
         try:
            if x == keywords[0]:
               PPMuart.append(int(data_from_sensor[pos+1].split(",")[0]))
               ax1.clear()
               ax1.plot(timestamp[:-1], PPMuart)
               plt.xlabel('Time (s)')
               plt.ylabel('CO2 concentration (PPM)')
                elif x == keywords[1]:
                    PPMpwm.append(int(data_from_sensor[pos + 1].split(",")[0]))
                    ax2.clear()
                    ax2.plot(timestamp, PPMpwm)
                    plt.xlabel('Time (s)')
               plt.ylabel('CO2 concentration (PPM)')
                elif x == keywords[2]:
                    timestamp.append(int(data_from_sensor[pos + 1].split(",")[0]))
            except:
                pass
            finally:
                pass

#Todo integrate two graph and

ani = anime.FuncAnimation(fig, animate, interval=1000)
plt.show()
