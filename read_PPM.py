from abc import ABC
from typing import Optional, List

import serial
import serial.tools.list_ports
import abc
import numpy
import scipy
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.figure as figure
import matplotlib.animation as anime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
matplotlib.use("Tkagg")
import threading
from collections.abc import Iterable, Iterator
from typing import Any, List
from tkinter import *
from tkinter import simpledialog, filedialog
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


class FileController:
    """
    In this class, implement everything about file manager, read, write etc.
    """

    def __init__(self):
        self.path = None
        self.file = []
        self.data = []  #
        self.time_stamp = []
        self.avg_ppm = []
        self.indoor_temp = []
        self.outdoor_temp = []

    def update(self, file):
        read_data = open(file, 'r')
        self.data.append(read_data.readlines())
        for i in range(len(self.data[0])):
            temporary_data = str.split(self.data[0][i], sep=" ")
            self.time_stamp.append(temporary_data[2])
            self.avg_ppm.append(temporary_data[4])
            self.indoor_temp.append(temporary_data[12])
            self.outdoor_temp.append(temporary_data[11])

    def print_data(self):
        print(self.avg_ppm)

class DataController:
    """
    In this class, implement everything about data processing.
    """

    def __init__(self):
        self.start_time = current_time()
        my_ports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
        try:
            arduino_port = [port for port in my_ports if 'Arduino' in port[1]][0]
        except:
            arduino_port = []
        try:
            self.serial = serial.Serial(arduino_port[0], 9600,
                                        timeout=0)  # consider a method to change serial data rate.
        except:
            self.serial = None

    def serial_read_data(self):
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
        self.label = []
        self.button = []
        self.canvas = []
        self.observers = []
        self.filedialog = None  # this is the diagram for load file interface
        self.filepath = None  #
        self.plot_window = None
        self.new_window = None

    def create_label(self):
        self.label.append(Label(self.top, text="room environment monitor"))

    def create_button(self):
        self.button.append(Button(self.top, text="setting", command=self.setting_callback))
        self.button.append(Button(self.top, text="load file", command=self.gotofiledialog))

    def create_canvas(self):
        self.canvas.append(Canvas(self.plot_window))
        self.canvas[0].pack()

    def create_all(self):
        self.create_label()
        self.create_button()

    def gotofiledialog(self):
        self.filedialog = filedialog.LoadFileDialog(self.top)
        self.filepath = self.filedialog.go(key="go")
        self.openfile()
        self.plot_window = Toplevel(self.top)
        self.plot_ppm()

    def setting_callback(self):
        self.new_window = Toplevel(self.top)

    def attach_observers(self, observer):
        """
        Event based GUI interface. interaction between Data controller and file controller.
        :param observer:
        :return:
        """
        self.observers.append(observer)

    def detach_observer(self, observer):
        """

        :param observer:
        :return:
        """
        self.observers.remove(observer)

    def openfile(self):
        """
        :return:
        """
        for observer in self.observers:
            if isinstance(observer, FileController):
                observer.update(self.filepath)

    def pack_label(self):
        """pack all the label into the window"""
        for label in self.label:
            label.pack()

    def pack_button(self):
        for b in self.button:
            b.pack()

    def pack_all(self):
        self.pack_button()
        self.pack_label()

    def plot_ppm(self):
        for observer in self.observers:
            if isinstance(observer, FileController):
                fig = figure.Figure(figsize=(8,8))
                a = fig.add_subplot(111)
                a.plot(numpy.array(observer.time_stamp), numpy.array(observer.avg_ppm), color='blue')
                a.set_title("CO2 average ppm")
                a.set_ylabel("ppm", fontsize=14)
                a.set_xlabel("time", fontsize=14)
                canvas = FigureCanvasTkAgg(fig, master=self.plot_window)
                canvas.get_tk_widget().pack()
                canvas.draw()


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
        self.file_server = FileController()
        self.gui_server.attach_observers(self.data_server)
        self.gui_server.attach_observers(self.file_server)

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
        self.gui_server.create_all()
        self.gui_server.pack_all()
        self.gui_server.run()

    def log(self):
        pass


# Todo integrate two graph and


if __name__ == '__main__':
    server = Controller()
    server.run()

# create a new window and
