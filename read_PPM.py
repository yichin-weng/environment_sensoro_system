from abc import ABC
from typing import Optional, List

import serial
import serial.tools.list_ports
import abc
import matplotlib.pyplot as plt
import matplotlib.animation as anime
import threading
from collections.abc import Iterable, Iterator
from typing import Any, List
from tkinter import *
from tkinter import simpledialog
from datetime import datetime
from tkinter import ttk

keywords = ["b'PPMuart:", "PPMpwm:", "start:"]
PPMuart = []
PPMpwm = []
timestamp = []
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)
plt.title('CO2 concentration over Time')


def current_time():
    return datetime.now()


"""
create every types of sensor
"""


def create_mhz14a():
    return MHZ14A()


class Sensor(metaclass=abc.ABCMeta):
    """
    this is the basic class for every sensor
    """

    @abc.abstractmethod
    def calibrate(self):
        """
        :return:
        """
        return NotImplemented


class MHZ14A(Sensor):
    """
    this sensor can detect the concentration of carbon-dioxide.
    the data will be transmitted directly by UART interface
    """

    def __init__(self):
        self.PPM_pwm = []
        self.PPM_uart = []
        self.serial_en = True
        self.pwm_en = True

    def calibrate(self):
        """
        set
        :return:
        status: success or false.
        """

    def store(self):
        """
        :return:
        """
        pass

    def create_plot(self):
        """

        :return:
        """
        pass


class SensorsCollection(Iterable, ABC):
    def __init__(self, collection: List[Any] = []) -> None:
        self._collection = collection

    def __iter__(self):
        return


class StartPage(Frame):
    """
    initial page of this
    """

    def __init__(self, parent):
        Frame.__init__(self, parent)


class Window(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.canvas = Canvas
        self.pack()
        self.create_buttons()
        self.start = None
        self.stop = None
        self.store = None
        self.calibrate = None

    def create_buttons(self):
        self.start = Button(self, text="start", command=self.start_plot)
        self.stop = Button(self, text="stop", command=self.stop_plot)
        self.store = Button(self, text="store", command=self.store_plot)
        self.calibrate = Button(self, text="calibrate", command=self.calibrate)

    # collect CO2 data and plot live graph
    def start_plot(self):
        pass

    #
    def stop_plot(self):
        pass

    def calibrate(self):
        pass


class DataController:
    """
    In this class, implement everything about data processing.
    """

    def __init__(self):
        my_ports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
        arduino_port = [port for port in my_ports if 'Arduino' in port[1]][0]
        self.start_time = current_time()
        if arduino_port is not None:
            self.serial = serial.Serial(arduino_port[0], 9600,
                                        timeout=0)  # consider a method to change serial data rate.

    def read_data(self):
        if self.serial.inWaiting():
            self.serial.readlines()

    def store_data(self):
        pass

    def set_serial_baudrate(self, target):
        self.serial.baudrate = target


class GUIController:
    """
    In this class, implement everything about User interface.

    """

    def __init__(self):
        self.top = Tk()
        self.label = Label(self.top, text="room environment monitor")
        self.label.pack()
        self.setting = Button(self.top, text="setting", command=self.settingcallback)
        self.setting.pack()
        self.newwindow = None

    def settingcallback(self):
        self.newwindow = Toplevel(self.top)

    def plot(self):
        pass

    def pack_label(self):
        for l in self.label:
            l.pack()

    def pack_button(self):
        for b in self.button:
            b.pack()

    def run(self):
        self.top.mainloop()


class Controller:
    """
    Because DataController and GUIController are independent of each other,
    this controller need to manager
    """

    def __init__(self):
        self.data_server = DataController()
        self.gui_server = GUIController()

    # create a popup window with start, stop, calibrate and icon
    def create_interactive_window(self):
        pass

    def read_option(self):
        pass

    def create_sensor(self, sensor_type):
        pass

    def calibrate(self):
        pass

    def save_file(self):
        pass

    def plot(self):
        pass

    def stop(self):
        pass

    def run(self):
        """

        :return:
        """
        self.gui_server.run()

    def log(self):
        pass


# Todo integrate two graph and


if __name__ == '__main__':
    server = Controller()
    server.run()

# create a new window and
