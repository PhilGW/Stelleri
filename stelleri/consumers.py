import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
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
#Event handler for our device:
class DeviceConsumer(WebsocketConsumer):
    def connect(self):
        self.device_name = "device_" + self.scope['url_route']['kwargs']['device_id']
        self.group_name = "all_devices"
        print("This device is connecting. It shall be called: ", self.device_name)
        print("This device's group name shall be: ", self.group_name)
        # Join group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        # If you do not call accept() within the connect() method then the connection will be rejected and closed.
        # You might want to reject a connection for example because the requesting user is not authorized to perform the requested action.
        self.accept()

    def disconnect(self, close_code):
        # Leave the group on disconnection:
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    # Handle incoming WebSocket data, and spread it out to all in the group (both connected browsers and connected devices):
    def receive(self, text_data):
        # Relay message to all in group:
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'dev_message',
                'message': text_data
            }
        )

    # Core functionality here. This function is run on ALL messages, whether they come from
    # A browser or another device. The 'topic' item in the dict/json is used to determine the response.
    def dev_message(self, event):
        msg = json.loads(event['message'])
        print("New message received by server: ", msg)
        topic = msg.pop('topic')
        #TODO: Error handling if topic is not one of these categories
        if topic == 'new_data':
            #Send a receipt confirmation back to the controller:
            print("New data incoming: ", msg)
            self.send(json.dumps({'topic': 'receipt_confirmation'}) )
        elif topic == 'param_update_request_from_ui':
            #Relay the request for a param change to the controller:
            print('msg type: ', type(msg))
            msg['topic'] = 'param_update'
            print("Param update requested by browser, relaying to controller: ", msg)
            self.send(text_data=json.dumps(msg))


