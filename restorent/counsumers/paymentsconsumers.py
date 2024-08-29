import json
from channels.generic.websocket import AsyncWebsocketConsumer


class PaymentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'payments'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()
    

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
    
    async def table_data(self, event):
        payment_data = event['payment_data']
        await self.send(
            text_data=json.dumps(
                {
                    'payment_data': payment_data
                }
            )
        )
    
    async def add_payment(self, transaction_id):
        pass
    