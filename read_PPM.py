import serial
import matplotlib.pyplot as plt
import matplotlib.animation as anime
ser = serial.Serial('COM3', 9600, timeout=0)
keywords = ["b'PPMuart:", "PPMpwm:", "start:"]

PPMuart     = []
PPMpwm      = []
timestamp   = []
fig = plt.figure()
ax1 = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)

def animate(i):
   avai = ser.in_waiting
   if avai > 0:
      data=ser.readline()
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
               PPMpwm.append(int(data_from_sensor[pos+1].split(",")[0]))
               ax2.clear()
               ax2.plot(timestamp, PPMpwm)
               plt.xlabel('Time (s)')
               plt.ylabel('CO2 concentration (PPM)')
            elif x == keywords[2]:
               timestamp.append(int(data_from_sensor[pos+1].split(",")[0]))
         except:
            pass
         finally:
            pass

#Todo integrate two graph and

ani = anime.FuncAnimation(fig, animate, interval=1000)
plt.show()