import paho.mqtt.client as mqtt
import random
import time
import sense_hat


# set up sense hat
sense = sense_hat.SenseHat()
# weather need to send message every seconds or not
is_continue_temp = False
is_continue_humidity = False
is_continue_pressure = False


def get_temp_short():
    temp = sense.temp
    temp_str = str("%.2f" % temp)
    return temp_str


def get_humidity_short():
    humidity = sense.humidity
    humidity_str = str("%.2f" % humidity)
    return humidity_str


def get_pressure_short():
    pressure = sense.pressure
    pressure_str = str("%.2f" % pressure)
    return pressure_str


def get_temp():
    return get_temp_short() + " 'C"


def get_humidity():
    return get_humidity_short() + " %rH"


def get_pressure():
    return get_pressure_short() + " hPa"


def stop_continue():
    global is_continue_temp
    global is_continue_humidity
    global is_continue_pressure
    is_continue_temp = False
    is_continue_humidity = False
    is_continue_pressure = False
    return 'continue'


def start_temp():
    stop_continue()
    global is_continue_temp
    is_continue_temp = True
    return 'continue'


def start_humidity():
    stop_continue()
    global is_continue_humidity
    is_continue_humidity = True
    return 'continue'


def start_pressure():
    stop_continue()
    global is_continue_pressure
    is_continue_pressure = True
    return 'continue'


def default_response():
    return "no such command"


def get_sense_hat_job(argument):
    switcher = {
        "temp": get_temp,
        "temperature": get_temp,
        "humidity": get_humidity,
        "pressure": get_pressure,
        "start temp": start_temp,
        "start humidity": start_humidity,
        "start pressure": start_pressure,
        "stop": stop_continue
    }
    # Get the function from switcher dictionary
    func = switcher.get(argument, default_response)
    # Execute the function
    return func()


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("messanger/topic/device")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    message = msg.payload.decode('UTF-8')
    print(msg.topic+" "+message)
    # print(msg.topic + " " + str(msg.payload))
    # client.publish("messanger/topic/server", "receive" + message)
    response_str = get_sense_hat_job(message)
    if response_str != 'continue':
        client.publish("messanger/topic/server", response_str)


# set up and connect the mqtt client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
# client.connect("iot.eclipse.org", 1883, 60)
client.connect("www.prophet-xu.com", 1883, 60)


client.publish("messanger/topic/server", "hello")

# client.loop_forever()
client.loop_start()
while True:
    if is_continue_temp:
        client.publish("messanger/topic/server", get_temp_short())
    if is_continue_humidity:
        client.publish("messanger/topic/server", get_humidity_short())
    if is_continue_pressure:
        client.publish("messanger/topic/server", get_pressure_short())
    time.sleep(1)
