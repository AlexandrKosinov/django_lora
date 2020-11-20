from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/dev/(?P<dev_name>\w+)/$', consumers.LoraConsumer),
    re_path(r'ws/test', consumers.TestConsumer),
    re_path(r'ws/node', consumers.NodeConsumer),
]