import serial
import re
import pyqtgraph as pg
import numpy as np
import psutil
import datetime
from datetime import date



#INIT COM PORT
portx = "COM3"
bps = 115200
timex = 2
# Последовательный порт выполняется до тех пор, пока он не будет открыт, а затем использование команды open сообщит об ошибке
try:
    ser = serial.Serial(portx, int(bps), timeout=1, parity=serial.PARITY_NONE, stopbits=1)
except serial.SerialException as e:
    # There is no new data from serial port
    print("No COM port")

def write_data_log(data_in):
    current_date = date.today()
    file = open(str(current_date)+"_data_log.txt", "a")
    dt_now = datetime.datetime.now()
    file.write(str(dt_now)+";"+str(data_in)+";")
    file.write('\n')
    file.close()

ret_data = []
def read_port(): #SERIAL OPERATION

    global ret_data
    line = ser.readline()
    #print("Get from COM^ " + str(line))
    cls_data = line.splitlines()
    cls_data = re.split("'", str(cls_data))
    print("ret_data arr[1]^", str(cls_data[1]))
    ret_data.append(int(cls_data[1]))
    write_data_log(cls_data[1])
    print(cls_data[1])
    plot.setData(ret_data, pen='g')

# Get timing callback functions for CPU usage
def get_cpu_info():
    cpu = "%0.2f" % psutil.cpu_percent(interval=1)
    data_list.append(float(cpu))
    print(float(cpu))
    plot.setData(data_list, pen='g')


if __name__ == '__main__':
    data_list = []

    # pyqtgragh initialization
    # Create a window
    app = pg.mkQApp()  # Establish a app
    win = pg.GraphicsLayoutWidget(show=True, title="Basic plotting examples")  # Create a window
    win.setWindowTitle(u'Pyqtgraph Real Time Waveform Display Tool')
    win.resize(800, 500)  #
    # Create a chart
    historyLength = 10000  # How many points we are remember
    p = win.addPlot()  # Add Figure P to the window
    p.showGrid(x=True, y=True)  # Open the form of X and Y
    p.setRange(xRange=[0, historyLength], yRange=[0, 100000], padding=0)
    p.setLabel(axis='left', text='Measured')  #
    p.setLabel(axis='bottom', text='time ms')
    p.setTitle('Real-time data')  #
    plot = p.plot()

    timer = pg.QtCore.QTimer()
    timer.timeout.connect(read_port)  # Timed refresh data display
    timer.start(200)  # How much MS calls once

    app.exec_()