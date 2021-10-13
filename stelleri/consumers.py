import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.consumer import SyncConsumer
# A consumer = event handler. Messages are put onto the channel by producers, and then given to just one of the consumers listening to that channel.
# Inside a network, we identify channels uniquely by a name string - you can send to any named channel
# from any machine connected to the same channel backend.
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
            #self.channel_name
        )
        # If you do not call accept() within the connect() method then the connection will be rejected and closed.
        # You might want to reject a connection for example because the requesting user is not authorized to perform the requested action.
        # It is recommended that accept() be called as the LAST action in connect()
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            #self.channel_name
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

#Event handler for our device:
class DeviceConsumer(WebsocketConsumer):
    def connect(self):
        self.device_name = "device_" + self.scope['url_route']['kwargs']['device_id']
        print("This device is connecting. It shall be called: ", self.device_name)
        self.group_name = "all_devices"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        # If you do not call accept() within the connect() method then the connection will be rejected and closed.
        # You might want to reject a connection for example because the requesting user is not authorized to perform the requested action.
        # It is recommended that accept() be called as the LAST action in connect()
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    # Handle incoming WebSocket data, and divvy it up among potential other functions based on the content:
    def receive(self, text_data):
        print("text_data received: ", text_data)
        print("Type: ", type(text_data))
        # text_data_json = json.loads(text_data)
        #message = text_data_json['message']
        #print("Message recieved: ", message)
        # Send message to room group. An event has a special 'type' key corresponding to the name of the method
        # that should be invoked on consumers that receive the event.

        # Send the message along to the log_data() method
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'log_data',
                'message': text_data
            }
        )

    # Receive message from room group:
    def log_data(self, event): #Name is the same as the "type:" in the dict() above
        message = event['message']
        print ("Holy crap! the message was received: ", message)
        # Send message to WebSocket
        self.send(text_data="Back atcha")
        # self.send(text_data=json.dumps({
        #     'message': message
        # }))