import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

# Channels also supports writing asynchronous consumers for greater performance.
# However any asynchronous consumer must be careful to avoid directly performing blocking operations,
# such as accessing a Django model. See the Consumers reference for more information about writing asynchronous consumers:
# https://channels.readthedocs.io/en/stable/topics/consumers.html

# ChatConsumer only uses async-native libraries (Channels and the channel layer) and in particular
# it does not access synchronous Django models. Therefore it can be rewritten to be asynchronous without complications.
#Even if ChatConsumer did access Django models or other synchronous code it would still be possible
# to rewrite it as asynchronous. Utilities like asgiref.sync.sync_to_async and channels.db.database_sync_to_async
# can be used to call synchronous code from an asynchronous consumer.
# The performance gains however would be less than if it only used async-native libraries.


# More info: https://channels.readthedocs.io/en/stable/tutorial/part_2.html
# Group names may only contain letters, digits, hyphens, and periods.
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        # If you do not call accept() within the connect() method then the connection will be rejected and closed.
        # You might want to reject a connection for example because the requesting user is not authorized to perform the requested action.
        # It is recommended that accept() be called as the LAST action in connect()
        self.accept()



    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group. An event has a special 'type' key corresponding to the name of the method
        # that should be invoked on consumers that receive the event.
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event): #Name is the same as the "type:" in the dict() above
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))