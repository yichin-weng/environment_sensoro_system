from typing import Optional, List

import serial
import serial.tools.list_ports
import abc
import matplotlib.pyplot as plt
import matplotlib.animation as anime
import threading
from tkinter import *
from tkinter import simpledialog
from datetime import datetime
from tkinter import ttk

ser = serial.Serial('COM3', 9600, timeout=0)
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

    @abc.abstractmethod
    def animate(self):
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

    def animate(self):
        if self.serial.in_waiting > 0:
            data = self.serial.readline()
            data = str(data)
            data_from_sensor = data.split()
            for pos, x in enumerate(data_from_sensor):
                try:
                    if x == keywords[0]:
                        PPMuart.append(int(data_from_sensor[pos + 1].split(",")[0]))
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

class StartPage(Frame):
    """
    initial page of this
    """
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text=" CO2 sensor control system ", font=)
        bu


class Window(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.canvas = Canvas
        self.pack()
        self.create_buttons()
        self.start = None
        self.stop  = None
        self.store = None
        self.calibrate = None

    def create_buttons(self):
        self.start = Button(self, text="start", command=self.start_plot)
        self.stop  = Button(self, text="stop", command=self.stop_plot)
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

class Controller:
    def __init__(self):
        my_ports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
        arduino_port = [port for port in my_ports if 'COM3' in port][0]
        self.serial = serial.Serial(arduino_port, 9600, timeout=0)
        self.sensor = List[Optional[Sensor]]
        self.new_window = Tk()
        self.new_window.mainloop()
        self.s = simpledialog.askstring()

    # create a popup window with start, stop, calibrate and icon
    def create_interactive_window(self):

    def read_option(self):

    def create_sensor(self, sensor_type):

    def calibrate(self):

    def save_file(self):

    def plot(self):

    def stop(self):

    def run(self):

    def log(self):
        """
        save all the information for debug
        :return:
        """


def animate(i):
    avai = ser.in_waiting
    if avai > 0:
        data = ser.readline()
        data = str(data)
        data_from_sensor = data.split()
        for pos, x in enumerate(data_from_sensor):
            try:
                if x == keywords[0]:
                    PPMuart.append(int(data_from_sensor[pos + 1].split(",")[0]))
                    ax1.clear()
                    ax1.plot(timestamp[:-1], PPMuart)
                    plt.xlabel('Time (s)')
                    plt.ylabel('CO2 concentration (PPMUart)')
                elif x == keywords[1]:
                    PPMpwm.append(int(data_from_sensor[pos + 1].split(",")[0]))
                    ax1.clear()
                    ax1.plot(timestamp, PPMpwm)
                    plt.xlabel('Time (s)')
                    plt.ylabel('CO2 concentration (PPMpwm)')
                elif x == keywords[2]:
                    timestamp.append(int(data_from_sensor[pos + 1].split(",")[0]))
            except:
                pass
            finally:
                pass


# Todo integrate two graph and


def main():
    ani = anime.FuncAnimation(fig, animate, interval=200)
    plt.show()

#create a new window and
if __name__ == '__name__':
    root = Tk()
    root.title("CO2 control system")
    main = Window(root)
    root.mainloop()
