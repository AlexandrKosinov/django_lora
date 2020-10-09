from channels.generic.websocket import WebsocketConsumer
import json
from datetime import datetime

from lora_networks.models import Device_info, Device


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

