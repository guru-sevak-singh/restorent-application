from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import async_to_sync
from django.utils import timezone
from channels.layers import get_channel_layer


class SoftwareConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = None
        self.group_name = 'all_users'

        # Add the channel to the group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()
    
    async def disconnect(self, code):
        if self.user_id:
            # Remove the user id from the list in the JSON file
            try:
                with open('all_users.json', 'r') as file:
                    all_users = json.load(file)
            except FileNotFoundError:
                all_users = []

            # Filter out the user_id
            try:
                all_users.remove(self.user_id)
            except:
                pass

            with open('all_users.json', 'w') as file:
                json.dump(all_users, file, indent=4)
            
            await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'user_data',
                'data': all_users
            }
        )

        # Remove the channel from the group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        text_data = json.loads(text_data)
        self.user_id = text_data.get('user_id')
        action = text_data.get('action')
        try:
            with open('all_users.json') as file:
                all_users = json.load(file)
        except:
            all_users = []

        if action == 'add_user' and self.user_id:
            await self.add_user(self.user_id)
        
        else:
            await self.send(
                text_data=json.dumps(
                {'all_users': all_users}
                )
            )

    async def user_data(self, event):
        all_users = event['data']
        await self.send(
            text_data=json.dumps(
                {'all_users': all_users}
            )
        )

    async def add_user(self, user_id):
        try:
            with open('all_users.json', 'r') as file:
                all_users = json.load(file)
        except FileNotFoundError:
            all_users = []
        

        all_users.append(user_id)
        
        with open('all_users.json', 'w') as file:
            json.dump(all_users, file, indent=4)
        
        # Broadcast updated user list
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'user_data',
                'data': all_users
            }
        )
