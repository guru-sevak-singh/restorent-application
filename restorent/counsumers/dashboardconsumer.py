import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.db.models import Q
from asgiref.sync import sync_to_async

class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'dashboard'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()


    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name,
        )

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'update_table_status':
            pk = data.get('pk')
            status = data.get('status')
            await self.update_table_status(pk, status)
        

    async def table_data(self, event):
        dashboard_data = event['dashboard_data']
        await self.send(
            text_data=json.dumps(
                {
                    'dashboard_data': dashboard_data
                }
            )
        )

    async def update_table_status(self, pk, status):
        from restorent.models import Table, Order
        return_data = {}
        table = await database_sync_to_async(Table.objects.get)(pk=pk)
        
        if status == "free":
            try:
                last_order = await database_sync_to_async(Order.objects.filter(table=table).latest)('start_time')
                
                if last_order.end_time is None or last_order.food_delivered is False:
                    status = True
                    return_data['alert_message'] = 'There is Still Some Work Pending On This Table !'
                else:
                    status = False
            except:
                status = False
        else:
            status = True
            table.order_panding = True
            table.payment_panding = True

        print(status)

        table.vacent_status = status
        await database_sync_to_async(table.save)()

        return_data['table_vacent_status']= table.vacent_status
        return_data["order_panding"] = table.order_panding
        return_data["payment_panding"] =  table.payment_panding
        return_data["pk"] = table.pk

        await self.channel_layer.group_send(
            'dashboard',
                {   
                    'type': 'table_data',
                    'dashboard_data': return_data
                }
            
        )

