import paho.mqtt.client as mqtt
import random
import time
import sense_hat


# set up sense hat
sense = sense_hat.SenseHat()


def get_temp():
    temp = sense.temp
    temp_str = str("%.2f" % temp)
    return temp_str + " 'C"


def get_humidity():
    humidity = sense.humidity
    humidity_str = str("%.2f" % humidity)
    return humidity_str + " %rH"


def get_pressure():
    pressure = sense.pressure
    pressure_str = str("%.2f" % pressure)
    return pressure_str + " hPa"


def default_response():
    return "no such command"


def get_sense_hat_job(argument):
    switcher = {
        "temp": get_temp,
        "temperature": get_temp,
        "humidity": get_humidity,
        "pressure": get_pressure
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
    client.publish("messanger/topic/server", response_str)


# set up and connect the mqtt client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
#client.connect("iot.eclipse.org", 1883, 60)
client.connect("www.prophet-xu.com", 1883, 60)


client.publish("messanger/topic/server", "hello")

# client.loop_forever()
client.loop_start()
while True:
    temp = random.uniform(10, 20)
    #client.publish("messanger/topic/server", temp)
    time.sleep(2)