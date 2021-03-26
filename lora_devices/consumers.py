from channels.generic.websocket import WebsocketConsumer
import json
import time
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from lora_networks.models import Device_info, Device, Node


class LoraConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(message)
        self.send(text_data=json.dumps({
            'message': message
        }))


class TestConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def getDeviceId(self, name):
        dev = Device.objects.get(name=name)
        dev_id = dev.id
        return dev_id

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        dev_name = text_data_json['device']
        date = text_data_json['date']
        datetime_object = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        info = text_data_json['info']
        dev_id = self.getDeviceId(dev_name)
        print(dev_name)
        print(dev_id)
        print(str(datetime_object))
        print(info)
        devInfo = Device_info.objects.create(device_id=dev_id, date=date, info=info)
        self.send(text_data=json.dumps({
            'message': 'Yes!'
        }))


class NodeConsumer(WebsocketConsumer):

    def __init__(self, path):
        WebsocketConsumer.__init__(self, path)
        self.buf = b''
        self.node_name = ''
        self.sensors = dict()
        self.response = dict()
        self.response['message'] = 'ok'

    def get_node_id(self, name):
        dev_id = -1
        try:
            dev = Node.objects.get(name=name)
            dev_id = dev.id
            return dev_id
        except ObjectDoesNotExist:
            self.response['message'] = 'error'
            self.response['error'] = 'NodeDoesNotExist'
            return dev_id

    def get_device_id(self, name):
        dev_id = -1
        try:
            dev = Device.objects.get(name=name)
            dev_id = dev.id
            return dev_id
        except ObjectDoesNotExist:
            self.response['message'] = 'error'
            self.response['error'] = 'DeviceDoesNotExist'
            return dev_id

    def update_node(self):
        k = self.node_name
        k += 'vdd'
        vdd = self.sensors.pop(k, -1)
        if vdd > -1:
            Node.objects.filter(name=self.node_name).update(charge=vdd)

    def create_sensor_data(self):
        for key, value in self.sensors.items():
            dev_id = self.get_device_id(key)
            if dev_id > -1:
                Device_info.objects.create(device_id=dev_id, date=datetime.now(), info=value)

    def save_to_db(self):
        if self.response.get('message') == 'ok':
            self.update_node()
            self.create_sensor_data()

    def crc99(self, data_len):
        b = 65535
        s = 255
        crc = 0
        for i in range(data_len):
            crc = (crc << 2) + crc + self.buf[i]
            crc = crc & b
            crc = (crc << 2) + crc + self.buf[i]
            crc = crc & b
            crc = (crc ^ (crc >> 8))
        return crc & s

    def parser(self):
        message_length = len(self.buf)-1
        i = 0
        for c in reversed(self.buf):
            if c == 35:
                break
            i += 1
        message_length -= i-2
        if message_length > 0:
            sensors_count = (message_length - 25)//16
            crc = self.buf[message_length-1]
            p_crc = self.crc99(message_length-1)
            if p_crc == crc:
                self.node_name = self.buf[0:24].decode()
                node_id = self.get_node_id(self.node_name)
                if node_id >= 0:
                    j = 0
                    for i in range(sensors_count):
                        n = 25 + j
                        m = n + 12
                        name_sensor = self.node_name
                        name_sensor += self.buf[n:m].decode()
                        name_sensor = name_sensor.rstrip('\x00')
                        num = self.buf[38+j] << 8 | self.buf[39+j]
                        num /= 100
                        self.sensors[name_sensor] = num
                        j = j + 16
            else:
                self.response['message'] = 'error'
                self.response['error'] = 'CRCError'
        else:
            self.response['message'] = 'error'
            self.response['error'] = 'LengthError'

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        if text_data:
            self.send(text_data=json.dumps({
                'message': 'Has text'
            }))
        else:
            self.buf = bytes_data
            self.parser()
            self.save_to_db()
            self.send(text_data=json.dumps(self.response))


class TimeConsumer(WebsocketConsumer):

    def __init__(self, path):
        WebsocketConsumer.__init__(self, path)
        self.buf = b''
        self.response = dict()
        self.response['message'] = 'ok'

    def crc99(self, data_len):
        b = 65535
        s = 255
        crc = 0
        for i in range(data_len):
            crc = (crc << 2) + crc + self.buf[i]
            crc = crc & b
            crc = (crc << 2) + crc + self.buf[i]
            crc = crc & b
            crc = (crc ^ (crc >> 8))
        return crc & s

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        tim = round(time.time()*1000)
        self.buf = bytes(str(tim), 'utf-8')
        message_length = len(self.buf)-1
        crc = self.crc99(message_length)
        self.response['message'] = str(tim) + "#" + str(crc)
        self.send(text_data=json.dumps(self.response))
