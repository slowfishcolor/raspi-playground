import serial
import time
from protocol_sdk import model, util
import paho.mqtt.client as mqtt
import copy

deviceId = "8c70c4761c556ea3"
subscribe_destination = "messenger/topic/server/" + deviceId
publish_destination = "messenger/topic/device/" + deviceId
brokerUrl = "www.prophet-xu.com"
port = "/dev/ttyUSB0"
ser = serial.Serial(port, 9600, timeout=1, writeTimeout=0.1)



loop_flag = 1


def serial_read():
    size = ser.inWaiting()
    if size:
        res_data = ser.readline()
        return res_data.decode().replace('\n', '')


def serial_send(send_str):
    send_str += '\n'
    ser.write(send_str.encode())


# The callback for when the client receives a CONNACK response from the server.
def on_connect(self, client, userdata, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    self.subscribe(subscribe_destination)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    message = msg.payload.decode('UTF-8')
    print(msg.topic + " " + message)

    payload = util.deserialize_payload(message)
    if payload.type == "InstructionData":
        instructionData = payload.data
        resInstructions = []
        instructions = instructionData.instructions
        for instruction in instructions:
            # instruction = perform_single_instruction(instructions.index(i))
            resInstruction = perform_single_instruction(instruction)
            resInstructions.append(resInstruction)
        res_payload = create_payload(payload.deviceId, payload.userId, resInstructions)
        res_payload.messageId = payload.messageId + 1
        res_json = util.serialize_payload(res_payload)
        print("send: " + res_json)
        client.publish(publish_destination, res_json)


# set up and connect the mqtt client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
# client.connect("iot.eclipse.org", 1883, 60)
client.connect(brokerUrl, 1883, 60)


def perform_single_instruction(instruction):

    resInstruction = copy.deepcopy(instruction)

    serial_send(instruction.name)
    print("serial send: " + instruction.name)
    time.sleep(0.1)
    resValue = serial_read()
    timeout = 0
    while (not resValue) or timeout > 12:
        time.sleep(0.1)
        timeout += 1
        resValue = serial_read()
    print("serial receive: " + resValue)

    resInstruction.type = instruction.type
    if instruction.type == instruction.COMMAND_STRING:
        resInstruction.type = instruction.RESULT_STRING
        resInstruction.valueString = resValue
    if instruction.type == instruction.COMMAND_NUMBER:
        resInstruction.type = instruction.RESULT_NUMBER
        resInstruction.valueNumber = float(resValue)

    resInstruction.timestamp = util.current_timestamp()
    return resInstruction


def create_payload(mockDeviceId, userId, instructions):
    option = model.Option()
    instructionData = model.InstructionData()
    instructionData.instructions = instructions
    instructionData.instructionCount = len(instructions)
    payload = model.Payload(option, instructionData)
    payload.deviceId = mockDeviceId
    payload.physicalDeviceId = deviceId
    payload.timestamp = util.current_timestamp()
    payload.userId = userId
    payload.code = 200
    return payload


print(ser.readall())

# client.loop_forever()
client.loop_start()

while loop_flag:
    time.sleep(0.2)
