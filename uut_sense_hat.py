import sense_hat
import serial
import time
import random

# set up sense hat
sense = sense_hat.SenseHat()

ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=0.1, writeTimeout=0.1)

loop_flag = 1

sense.low_light = True
sense.set_imu_config(True, True, True)


def serial_read():
    size = ser.inWaiting()
    if size:
        res_data = ser.readline()
        return res_data.decode().replace('\n', '')


def serial_send(send_str):
    send_str += '\n'
    ser.write(send_str.encode())


def get_temp():
    sense.show_letter('T')
    temp = sense.temp
    temp_str = str("%.2f" % temp)
    return temp_str


def get_humidity():
    sense.show_letter('H')
    humidity = sense.humidity
    humidity_str = str("%.2f" % humidity)
    return humidity_str


def get_pressure():
    sense.show_letter('P')
    pressure = sense.pressure
    pressure_str = str("%.2f" % pressure)
    return pressure_str


def get_temp_str():
    temp = sense.temp
    temp_str = str("%.2f" % temp)
    return get_temp() + " 'C"


def get_humidity_str():
    humidity = sense.humidity
    humidity_str = str("%.2f" % humidity)
    return get_humidity() + " %rH"


def get_pressure_str():
    pressure = sense.pressure
    pressure_str = str("%.2f" % pressure)
    return get_pressure() + " hPa"


def get_orientation():
    sense.show_letter('O')
    orientation = sense.get_orientation_degrees()
    return str(orientation)


def get_compass():
    sense.show_letter('C')
    north = sense.get_compass()
    return "north: " + str("%.2f" % north)


def get_gyroscope():
    sense.show_letter("G")
    return str(sense.get_gyroscope())


def show_letter(s):
    sense.show_letter(s)
    return 'letter: ' + s + ' displayed'


def show_message(s):
    sense.show_message(s)
    return 'message: ' + s + ' displayed'


def get_accelerometer():
    return str(sense.get_accelerometer())


def show_color():
    sense.clear(255, 0, 0)
    time.sleep(0.1)
    sense.clear(128, 128, 0)
    time.sleep(0.1)
    sense.clear(0, 255, 0)
    time.sleep(0.1)
    sense.clear(0, 128, 128)
    time.sleep(0.1)
    sense.clear(0, 0, 255)
    time.sleep(0.1)
    sense.clear(128, 128, 128)
    time.sleep(0.1)
    sense.clear(255, 255, 255)
    time.sleep(0.1)
    sense.clear()
    return 'color displayed'


def init():
    return 'init finished'


def default_response():
    return "unknown"


def random_result():
    if random.random() < 0.5:
        return "pass"
    else:
        return "block"


def get_sense_hat_job(argument):
    switcher = {
        "init": init,
        "temp": get_temp,
        "temperature": get_temp,
        "humidity": get_humidity,
        "pressure": get_pressure,
        "temperature_str": get_temp_str,
        "humidity_str": get_humidity_str,
        "pressure_str": get_pressure_str,
        "orientation": get_orientation,
        "compass": get_compass,
        "gyroscope": get_gyroscope,
        "show_color": show_color,
        "random": random_result
    }
    # Get the function from switcher dictionary
    func = switcher.get(argument, default_response)
    # Execute the function
    return func()


while loop_flag:
    command = serial_read()
    if command:
        reply = get_sense_hat_job(command)
        print("command: " + command)
        print("replay: " + reply)
        serial_send(reply)
    time.sleep(0.1)

