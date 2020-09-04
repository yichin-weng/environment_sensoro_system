from abc import ABC
from typing import Optional, List

import serial
import serial.tools.list_ports
import abc
import numpy
import os
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
algorithm_sel = ['FFT', 'Wavelet Transform', 'autocorrelation', 'Poincare plot']


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


class AlgorithmPage(Frame):
    def __init__(self):
        pass


class LivePage(Frame):
    """
    In this page, it implements the live data streaming function.
    Procedure:
    """

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.connect_b = Button(self, text="scan and connect", command=lambda: controller.connect_to_arduino())
        self.connect_b.pack()
        self.start_b = Button(self, text="start", command=lambda: self.start())
        self.start_b.pack()
        self.stop_b = Button(self, text="stop", command=lambda: self.stop())
        self.stop_b.pack()
        self.ani = anime.FuncAnimation(controller.fig, self.animate, interval=1000)
        self.ax = controller.fig.add_subplot(1, 1, 1)

    def start(self):
        """
        begin data streaming
        :return:
        """
        self.controller.file_server.open_new_file()

    def stop(self):
        """
        stop data streaming
        :return:
        """
        pass

    def save(self):
        """
        save the data and figure
        :return:
        """
        pass

    def animate(self, interval):
        """
        :return:
        """
        self.controller.file_server.read_from_serial(self.controller.data_server.serial_read_data())
        self.ax.clear()
        self.ax.plot(self.controller.file_server.time_stamp, self.controller.file_server.avg_ppm, label="PPM")


class GraphPage(Frame):
    """
    In this page, show the basic data from single file. Add some algorithm to analyze this data.
    besides, want to analyze multiple data.
    """

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.label = Label(self, text='CO2 concentration (PPM)', font=LARGE_FONT)
        self.label.place(x=300, y=0)
        # create button
        self.button1 = Button(self, text="HomePage", command=lambda: self.homepage(), height=1, width=20)
        self.button1.place(x=100, y=30)
        self.button2 = Button(self, text="plot", command=lambda: self.plot(), height=1, width=20)
        self.button2.place(x=100, y=60)
        self.button3 = Button(self, text="compare with other file", height=1, width=20,
                              command=lambda: self.controller.read_another_file())
        self.button3.place(x=100, y=90)
        # create checkbutton
        self.ppm = BooleanVar()
        self.temp = BooleanVar()
        self.ppm.set(False)
        self.temp.set(False)
        self.checkbutton1 = Checkbutton(self, text="average PPM", command=lambda: self.set_select_ppm())
        self.checkbutton2 = Checkbutton(self, text="temperature", command=lambda: self.set_select_temp())
        self.checkbutton1.place(x=300, y=30)
        self.checkbutton2.place(x=300, y=60)
        # create listbox
        self.sel_list = StringVar(value=algorithm_sel)
        self.algorithm_sel = Listbox(self, listvariable=self.sel_list, selectmode='algorithm', height=4)
        self.algorithm_sel.bind('<<ListboxSelect>>', lambda: self.test())
        self.algorithm_sel.place(x=400, y=30)
        self.ax = controller.fig.add_subplot(111)
        self.ax2 = controller.fig.add_subplot(411)

    def homepage(self):
        self.controller.file_server.clear_all()
        self.controller.frames["GraphPage"].destroy()
        self.controller.show_frame("HomePage")

    def test(self):
        print(self.ppm.get())

    def set_select_ppm(self):
        """
        By selecting this value, plot figure of ppm.
        :return:
        """
        if self.ppm.get():
            self.ppm.set(False)
        else:
            self.ppm.set(True)

    def set_select_temp(self):
        """
        By selecting this value, plot figure of temperature.
        :return:
        """
        if self.temp.get():
            self.temp.set(False)
        else:
            self.temp.set(True)

    def plot(self):
        if self.temp.get():
            self.plot_temperature()

        if self.ppm.get():
            self.plot_ppm()

        self.plot_canvas()

    def plot_ppm(self):
        FS = self.controller.file_server
        a = self.ax
        a.plot(FS.time_stamp, FS.avg_ppm, color='blue')
        a.set_title("CO2 average ppm")
        xdata = int(numpy.ceil(float(FS.time_stamp[-1])))
        ydata = int(numpy.ceil(float(FS.avg_ppm[-1]) - float(FS.avg_ppm[0])))
        major_xtick = numpy.arange(0, xdata, xdata / 5)
        major_ytick = numpy.arange(0, ydata, ydata / 5)
        a.set_xticks(major_xtick)
        a.set_yticks(major_ytick)
        a.set_ylabel("ppm", fontsize=14)
        a.set_xlabel("time", fontsize=14)

    def plot_temperature(self):
        FS = self.controller.file_server
        a = self.ax2
        a.plot(FS.time_stamp, FS.indoor_temp, color='red')
        a.set_title("indoor temperature (C)")
        xdata = int(numpy.ceil(float(FS.time_stamp[-1])))
        ydata = int(numpy.ceil(float(FS.indoor_temp[-1]) - float(FS.indoor_temp[0])))
        major_xtick = numpy.arange(0, xdata, xdata / 5)
        major_ytick = numpy.arange(0, ydata, ydata / 5)
        a.set_xticks(major_xtick)
        a.set_yticks(major_ytick)
        a.set_ylabel("temperature", fontsize=14)
        a.set_xlabel("time", fontsize=14)

    def plot_canvas(self):
        canvas = FigureCanvasTkAgg(self.controller.fig, self)
        canvas.draw()
        canvas.get_tk_widget().place(x=100, y=120, height=300, width=560)
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.place(x=100, y=120)

    def select_algorithm(self, algorithm):
        """
        From the listbox, applying the corresponding algorithm on the data.
        :param algorithm:
        :return:
        """
        pass


class HomePage(Frame):
    """
        The first page to begin my application, real time monitoring or file controller
    """

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.label = Label(self, text="room environment monitoring system", font=LARGE_FONT)
        self.label.pack(side="top")
        self.button1 = Button(self, text="load file", command=lambda: controller.gotofiledialog())
        self.button1.pack(fill=X)
        self.button2 = Button(self,
                              text="Plot the data from file",
                              command=lambda: controller.plot_from_file())  # check the connection between computer and arduino
        self.button2.pack(fill=X)
        self.button3 = Button(self, text="done", command=quit)
        self.button3.pack(fill=X, side="bottom")
        self.button4 = Button(self, text="plot real time data", command=lambda: controller.start_streaming())
        self.button4.pack(fill=X)


class FileController:
    """
    In this class, implement everything about file manager, read, write etc.
    """

    def __init__(self):
        self.path = os.getcwd()
        self.length = None
        self.file = None
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

    def open_new_file(self):
        """
        before beginning streaming data from arduino
        :return:
        """
        name_of_file = current_time().strftime("%Y%m%d-%H%M%S")
        self.file = open(name_of_file+".dat", 'w')

    def close_file(self):
        self.file.close()

    def read_from_serial(self, data):
        """
        :return:
        """
        self.data = str(data).split()
        for x, pos in enumerate(self.data):
            if x == keywords[0]:
                self.avg_ppm.append(int(self.data[pos+1].split(",")[0]))

            if x == keywords[2]:
                self.time_stamp.append(int(self.data[pos+1].split(",")[0]))

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
        """
        :return:
        """
        if self.serial.inWaiting():
            return self.serial.readlines()

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
        self.streaming_data = []
        self.file_server = None
        self.data_server = None
        self.filedialog = None  # this is the diagram for load file interface
        self.filepath = None  #
        self.show_frame("HomePage")
        self.geometry("800x600+20+20")
        self.fig = plt.Figure(figsize=(8, 8))

    def start_streaming(self):
        """
        check the Uart connection with arduino
        :return:
        """
        self.file_server.open_new_file()
        serial_data = self.data_server.serial_read_data()

    def stop_streaming(self):
        """
        stop real time graph but still collecting data from sensors
        :return:
        """
        pass

    def show_frame(self, page_name):
        """
        Change the page to corresponding page name.
        :param page_name:
        :return:
        """
        frame = self.frames[page_name]
        frame.tkraise()

    def gotofiledialog(self):
        """
        show the Filedialog
        :return:
        """
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

    def create_graphpage(self):
        """
        Renew the graph page
        :return:
        """
        self.frames["GraphPage"] = GraphPage(parent=self.container, controller=self)
        self.frames["GraphPage"].grid(row=0, column=0, sticky="nsew")

    def create_livepage(self):
        """
        Renew the live data page
        :return:
        """
        self.frames["LivePage"] = LivePage(parent=self.container, controller=self)
        self.frames["LivePage"].grid(row=0, column=0, sticky="nsew")

    def plot_from_file(self):
        """
        plot the graph from existing file.
        :return:
        """
        self.create_graphpage()
        self.show_frame("GraphPage")

    def connect_to_arduino(self):
        """
        check if the 
        :return:
        """
        pass

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
