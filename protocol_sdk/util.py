from protocol_sdk import json
from protocol_sdk import time

from protocol_sdk import model



def serialize_payload(payload):
    return json.dumps(payload, default=lambda obj:obj.__dict__)


def deserialize_payload(jsonStr):
    return json.loads(jsonStr, object_hook=decode_payload)


def current_timestamp():
    t = time.time()
    return round(t * 1000)


def decode_payload(d):

    if 'code' not in d:
        # print('no code', d)
        return d
    # print('has code', d)
    option = model.Option()
    option.password = d['option']['password']
    option.username = d['option']['username']
    option.qos = d['option']['qos']
    option.publish = d['option']['publish']
    option.subscribe = d['option']['subscribe']
    option.url = d['option']['url']
    option.will = d['option']['will']

    type = d['type']
    if type == 'AnalogSampleData':
        data = model.AnalogSampleData()
        data.port = d['data']['port']
        data.method = d['data']['method']
        data.frequency = d['data']['frequency']
        data.sampleCount = d['data']['sampleCount']
        data.timestamp = d['data']['value']
    if type == 'ControlData':
        data = model.ControlData()
        data.commandCount = d['data']['commandCount']
        data.command = d['data']['command']
        data.commands = d['data']['commands']
        data.commandMap = d['data']['commandMap']
    if type == 'InstructionData':
        data = model.InstructionData()
        data.instructionCount = d['data']['instructionCount']
        # if d['data']['instruction'] != 0:
        #     data.instruction = instruction_from_dict(d['data']['instruction'])
        if len(d['data']['instructions']):
            instructions = []
            for ins in d['data']['instructions']:
                instructions.append(instruction_from_dict(ins))
            data.instructions = instructions
        # if d['data']['instructionMap']:
        #     instructionMap = {}
        #     for key in d['data']['instructionMap']:
        #         instructionMap[key] = instruction_from_dict(d['data']['instructionMap'][key])
        #     data.instructionMap = instructionMap

    payload = model.Payload(option, data)
    payload.messageId = d['messageId']
    payload.destination = d['destination']
    payload.deviceId = d['deviceId']
    payload.physicalDeviceId = d['physicalDeviceId']
    payload.timestamp = d['timestamp']
    payload.userId = d['userId']
    payload.code = d['code']
    payload.type = d['type']
    return payload


def instruction_from_dict(d):
    instruction = model.Instruction()
    instruction.name = d['name']
    instruction.type = d['type']
    instruction.valueString = d['valueString']
    instruction.valueNumber = d['valueNumber']
    instruction.minValue = d['minValue']
    instruction.maxValue = d['maxValue']
    instruction.interval = d['interval']
    instruction.timestamp = d['timestamp']
    instruction.remark = d['remark']
    instruction.port = d['port']
    return instruction


