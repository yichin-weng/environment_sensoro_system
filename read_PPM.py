import serial
import matplotlib.pyplot as plt
import matplotlib.animation as anime
ser = serial.Serial('COM3', 9600, timeout=0)
keywords = ["b'PPMuart:", "PPMpwm:", "start:"]

PPMuart     = []
PPMpwm      = []
timestamp   = []
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
plt.title('CO2 concentration over Time')

def animate(i):
   avai = ser.in_waiting
   if avai > 0:
      data=ser.readline()
      # f = open('myfile.txt', 'a')
      data=str(data)
      data_from_sensor = data.split()
      for pos, x in enumerate(data_from_sensor):
         try:
            if x == keywords[0]:
               PPMuart.append(int(data_from_sensor[pos+1].split(",")[0]))
            elif x == keywords[1]:
               PPMpwm.append(int(data_from_sensor[pos+1].split(",")[0]))
               ax.clear()
               ax.plot(timestamp, PPMpwm, label="PPM_pwm")
               ax.plot(timestamp, PPMuart, label="PPM_uart")
            elif x == keywords[2]:
               timestamp.append(int(data_from_sensor[pos+1].split(",")[0]))
         except:
            pass
         finally:
            pass

   # f.write(data)
   # f.write('\n')
   # f.close()


ani = anime.FuncAnimation(fig, animate, interval=1000)
plt.show()