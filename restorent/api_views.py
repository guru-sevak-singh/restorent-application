# DJANGO REST FRAME WORK
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import JsonResponse

# import channels
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
import calendar

# models
from .models import Payment, Order, Table


@api_view(['POST'])
def add_payment_by_url(request):
    return_data = {}
    data = request.data

    transaction_id = data.get('transaction_id')
    try:
        all_ids = transaction_id.split("-")
        current_date = timezone.now()
        if all_ids[0] == 'restorent'and  len(all_ids[1]) == 8 and len(all_ids[2]) == 6:
            # its best id
            if all_ids[1] == current_date.strftime("%Y%m%d"):
                paid_amount = float(data.get('amount'))
                payment_method = 'UPI'
                order_id = all_ids[3]
                message = data.get('method')
                order = Order.objects.get(pk=order_id)

                new_payment = Payment(order=order, paid_amount=paid_amount, payment_method=payment_method, message=message)
                new_payment.save()
                order.end_time = timezone.now()

                table = order.table
                if table != None:
                    table.payment_panding = False
                    table.save()

                order.save()

                # send to channel layer
                channel_layer = get_channel_layer()
                # send data to the payent socket
                async_to_sync(channel_layer.group_send)(
                    'payments',
                    {
                        'type': 'table_data',
                        'payment_data': json.dumps(
                            {'payment_id': new_payment.id,
                            'work': 'add_new_payment',
                            'status': 'success',
                            'order_id': order.id,
                            'transaction_id': order.transaction_id
                            }
                        ) 
                    }
                )

                if table != None:
                    # send data to the dashboard socket
                    async_to_sync(channel_layer.group_send)(
                        'dashboard',
                        {
                    'type': 'table_data',
                    'dashboard_data': {
                            "table_vacent_status": table.vacent_status,
                            "order_panding": table.order_panding,
                            "payment_panding": table.payment_panding,
                            "pk": table.pk 
                        }
                    })

                    if order.normal_table == False:
                        if order.food_delivered == False:
                            pass
                        else:
                            table.delete()

                return_data = {'message': 'payment done'}
                
            else:
                # its not an restorent payment
                return_data = {'message': 'wrong payment id'}
        else:
            return_data = {'message': 'wrong payment id'}
                    
    except:
        # its not a restorent payment
        return_data = {'message': 'wrong payment id'}

    # Save data logic here
    return Response(return_data)

@login_required
@api_view(['GET'])
def dashboard_data(request):
    restorent = request.user.userprofile.restorent
    date_range = request.GET.get('daterange', "")
    if date_range == "":
        start_date = timezone.now().date()
        end_date = timezone.now().date()
    else:
        try:
            start_date = date_range.split(" - ")[0]
            end_date = date_range.split(" - ")[1]

            start_date = datetime.strptime(start_date, "%d/%b/%Y").date()
            end_date = datetime.strptime(end_date, "%d/%b/%Y").date()
        except :
            start_date = timezone.now().date()
            end_date = timezone.now().date()
    
    print(start_date, end_date)

    all_orders = Order.objects.filter(restorent=restorent ,start_time__date__range=(start_date, end_date))
    print(all_orders.count())
    
    table_orders = all_orders.filter(normal_table=True).count()
    deliver_table = all_orders.count() - table_orders

    total_payment = Payment.objects.filter(order__in=all_orders).aggregate(total=Sum('paid_amount'))['total']
    total_payment = total_payment if total_payment is not None else 0

    vacent_table = Table.objects.filter(floor__restorent=restorent, vacent_status = True).count()
    # vacent_table = 0

    return_data = {"all_orders": all_orders.count(), "table_orders": table_orders, "Delivery_order": deliver_table, "Total Payment": total_payment, "Vacant Table": vacent_table}
    return Response(return_data)

@api_view(['GET'])
def get_yearly_revenue(request, year):
    # Get the current year or any specific year you want to calculate for

    # Initialize the revenue dictionary
    revenue_by_month = {}

    # Loop through each month of the year
    for month in range(1, 13):
        # First and last day of the current month
        first_day = datetime(year, month, 1)
        last_day = datetime(year, month, calendar.monthrange(year, month)[1])

        # Filter payments within the month
        payments = Payment.objects.filter(order__restorent=request.user.userprofile.restorent, timing__date__range=(first_day, last_day))
        
        # Sum the paid_amount for these payments
        monthly_total = payments.aggregate(total=Sum('paid_amount'))['total'] or 0
        
        # Update the dictionary with the total revenue for the month
        revenue_by_month[calendar.month_name[month]] = round(monthly_total, 2)


    return JsonResponse(revenue_by_month)