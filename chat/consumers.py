# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.core import serializers
from channels.auth import login

from chat.forms import CALForm
from chat.models import LOG


class ChatConsumer(WebsocketConsumer):
    group_name = 'history_logs'

    def connect(self):
        self.user = self.scope["user"]
        print(self.user)
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        async_to_sync(login)(self.scope, self.user)
        self.scope["session"].save()

        text_data_json = json.loads(text_data)
        message = text_data_json['expression']

        form = CALForm(text_data_json)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = self.user
            log.save()

        # Send message to group
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from group
    def chat_message(self, event):
        logs = LOG.objects.order_by('-date')[:10]
        logs_json = serializers.serialize('json', logs)
        response = dict()
        response['data'] = logs_json
        # Send message to WebSocket
        self.send(text_data=json.dumps(response))
