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
import matplotlib.backends.backend_tkagg as tkagg
from matplotlib.backend_bases import cursors
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import threading
from collections.abc import Iterable, Iterator
from typing import Any, List
from tkinter import *
from tkinter import simpledialog, filedialog
from datetime import datetime
from tkinter import ttk, Menu, Frame

matplotlib.use("Tkagg")

LARGE_FONT = ("Verdana", 12)
keywords = ["b'PPMuart:", "PPMpwm:", "start:"]
PPMuart = []
PPMpwm = []
timestamp = []


def current_time():
    return datetime.now()


"""
create every types of sensor
"""


def create_mhz14a():
    return MHZ14A()


class Sensor(metaclass=abc.ABCMeta):
    """
    This is the basic class for every sensor
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
        Transmit calibrate instruction to set CO2 sensor as 400ppm
        :return:
        status: success or false.
        """

    def store(self):
        """
        Store the data as a file after streaming.
        :return:
        """
        pass

    def create_plot(self):
        """
        Streaming the data on live
        :return:
        """
        pass


class SensorsCollection(Iterable, ABC):
    def __init__(self, collection: List[Any] = []) -> None:
        self._collection = collection

    def __iter__(self):
        return


class StreamingPage(Frame):
    """
    In this page, it implements the live data streaming function.
    Procedure:
    """
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.button1 = Button(self, text="", command=lambda: controller.connect_to_arduino())

    def start(self):
        """
        begin data streaming
        :return:
        """
        pass

    def stop(self):
        """
        stop data streaming
        :return:
        """

    def save(self):
        """
        save the data and figure
        :return:
        """


class GraphPage(Frame):
    """
    In this page, show the basic data from single file. Add some algorithm to analyze this data.
    besides, want to analyze multiple data.
    """

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.label = Label(self, text='CO2 concentration (PPM)', font=LARGE_FONT)
        self.label.pack(side='top')
        self.button1 = Button(self, text="HomePage", command=lambda: controller.homepage())
        self.button1.pack()
        self.button2 = Button(self, text="plot", command=lambda: self.plot_ppm())
        self.button2.pack()
        self.button3 = Button(self, text="compare with other file", command=lambda: self.controller.read_another_file)
        self.button3.pack()
        self.fig = plt.Figure(figsize=(8, 8))
        self.ax = self.fig.add_subplot(111)

    def plot_ppm(self):
        FS = self.controller.file_server
        a = self.ax
        fig = self.fig
        a.plot(FS.time_stamp, FS.avg_ppm, color='blue')
        a.set_title("CO2 average ppm")
        xdata = int(numpy.ceil(float(FS.time_stamp[-1])))
        ydata = int(numpy.ceil(float(FS.avg_ppm[-1])-float(FS.avg_ppm[0])))
        major_xtick = numpy.arange(0, xdata, xdata/5)
        major_ytick = numpy.arange(0, ydata, ydata/5)
        a.set_xticks(major_xtick)
        a.set_yticks(major_ytick)
        a.set_ylabel("ppm", fontsize=14)
        a.set_xlabel("time", fontsize=14)
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)

    def select_algorithm(self, algorithm):
        """

        :param algorithm:
        :return:
        """
        pass


class HomePage(Frame):
    """
        The first page to begin my application,
    """

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.label = Label(self, text="room environment monitoring system", font=LARGE_FONT)
        self.label.pack(side="top")
        self.button1 = Button(self, text="load file", command=lambda: controller.gotofiledialog())
        self.button1.pack()
        self.button2 = Button(self,
                              text="Plot the data from file",
                              command=lambda: controller.plot())  # check the connection between computer and arduino
        self.button2.pack()
        self.button3 = Button(self, text="done", command=quit)
        self.button3.pack()


class FileController:
    """
    In this class, implement everything about file manager, read, write etc.
    """

    def __init__(self):
        self.path = None
        self.length = None
        self.file = []
        self.data = []
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
        self.length = len(self.data[0])
        read_data.close()

    def clear_all(self):
        self.data.clear()
        self.time_stamp.clear()
        self.avg_ppm.clear()
        self.indoor_temp.clear()
        self.outdoor_temp.clear()

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


class GUIController(Tk):
    """
    In this class, implement everything about User interface.
    """

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        Tk.iconbitmap(self)
        Tk.wm_title(self, "Room Monitoring System")
        container = self.container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {"HomePage": HomePage(parent=container, controller=self)}
        self.frames["HomePage"].grid(row=0, column=0, sticky="nsew")

        self.file_server = None
        self.data_server = None
        self.filedialog = None  # this is the diagram for load file interface
        self.filepath = None  #
        self.show_frame("HomePage")

    def homepage(self):
        """
        Change the page to the home page
        :return:
        """
        self.file_server.clear_all()
        self.frames["GraphPage"].destroy()
        self.show_frame("HomePage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def gotofiledialog(self):
        self.filedialog = filedialog.LoadFileDialog(self)
        self.filepath = self.filedialog.go(key="go")
        self.update_data()

    def attach_data_server(self, data_server):
        """
        :param data_server:
        :return:
        """
        self.data_server = data_server

    def attach_file_server(self, file_server):
        """
        add file server as an observer to monitor event
        :param file_server:
        :return:
        """
        self.file_server = file_server

    def detach_file_server(self):
        """
        reset file server
        :param observer:
        :return:
        """
        self.file_server = None

    def detach_data_server(self):
        """
        reset data server
        :return:
        """
        self.data_server = None

    def read_another_file(self):
        self.gotofiledialog()

    def update_data(self):
        """
        update data to data server for data processing
        :return:
        """
        self.file_server.update(self.filepath)

    def create_streamingpage(self):
        """
        Renew the graph page to
        :return:
        """

    def create_graphpage(self):
        """
        Renew the graph page to
        :return:
        """
        self.frames["GraphPage"] = GraphPage(parent=self.container,controller=self)
        self.frames["GraphPage"].grid(row=0, column=0, sticky="nsew")

    def plot(self):
        """
        plot the graph from existing file.
        :return:
        """
        self.create_graphpage()
        self.show_frame("GraphPage")

    def run(self):
        self.mainloop()


class Controller:
    """
    Because DataController and GUIController are independent of each other,
    this controller need to manager
    """

    def __init__(self):
        self.data_server = DataController()
        self.gui_server = GUIController()
        self.file_server = FileController()
        self.gui_server.attach_data_server(self.data_server)
        self.gui_server.attach_file_server(self.file_server)

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
