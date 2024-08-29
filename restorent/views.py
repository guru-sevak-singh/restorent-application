from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.http import JsonResponse, HttpResponseRedirect, Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Table, Restorent, Floor, UserProfile, FoodCategory, FoodItem, Order, OrderItems, Payment
from .form import FoodItemForm, PaymentForm, UpdateRestorentDetail, AddTax, RestorentForm
import json
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.conf import settings
from .generatoer import generate_qr
import json
import random
import os
from datetime import datetime
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password



# def is_owner(user):
#     owner_h = user.groups.filter(name="Restorent Owner").exists()
#     if owner_h:
#         return True
#     else:
#         raise PermissionDenied


# Create your views here.
@login_required
def index(request):
    # all floor of this restorent
    restorent = request.user.userprofile.restorent
    floors = Floor.objects.filter(restorent=restorent)
    return render(request, 'restorent/tableView.html', {"floors": floors})

@login_required
def dashboard(request):
    restorent = request.user.userprofile.restorent
    current_year = timezone.now().year
    
    return render(request, "restorent/dashboard.html", {"restorent": restorent, "current_year": current_year})

@login_required
def setting(request):
    return render(request, 'restorent/settings.html')

@login_required
def add_sitting_area(request):
    floors = Floor.objects.filter(restorent=request.user.userprofile.restorent).prefetch_related('table_set')
    return render(request, 'restorent/add_sitting_area.html', {"floors": floors})

@login_required
def add_area(request):
    if request.method == 'POST':
        current_user = request.user
        user_porfile = UserProfile.objects.filter(user=current_user).first()
        restorent = user_porfile.restorent
        work = request.POST['work']
        area_name = request.POST['area_name']
        no_of_tables = request.POST['no_of_tables']

        if work == 'add_area':
            floor = Floor(name=area_name, restorent=restorent)
            floor.save()
            for n in range(int(no_of_tables)):
                Table(floor=floor).save()
            messages.success(request, f'{no_of_tables} tables are added in floor :- {floor}')

        if work == 'remove_table':
            area = Floor.objects.get(pk=area_name)
            tables = area.table_set.order_by('id').reverse()
            try:
                for n in range(int(no_of_tables)):
                    table = tables[n]
                    table.delete()
            except IndexError:
                area.delete()
                
            messages.success(request, f'{no_of_tables} tables are deleted from floor :- {area}')

        return redirect('restorent:add_sitting')
        
@login_required
def add_table(requet, floor_id):
    floor = Floor.objects.get(pk=floor_id)

    Table(floor=floor).save()
    return redirect('restorent:add_sitting')

@login_required
def add_menue(request):
    # add Menue to this restorent
    restorent = request.user.userprofile.restorent
    food_categories = FoodCategory.objects.filter(restorent=restorent)
    form = FoodItemForm()
    return render(request, 'restorent/add_menue.html', {"food_categories": food_categories, "form": form})

@login_required
def add_category(request):
    # add catogary to only this restorent
    if request.method == 'POST':
        category_name = request.POST['category_name']
        current_user = request.user
        restorent = current_user.userprofile.restorent
        FoodCategory(name=category_name, restorent=restorent).save()
        return redirect('restorent:add_menue')
    
@login_required
def add_food_item(request, pk=None):
    if request.method == 'POST':
        if pk:
            food_item = get_object_or_404(FoodItem, pk=pk)
        
            form = FoodItemForm(request.POST, request.FILES, instance=food_item)

        else:
            form = FoodItemForm(request.POST, request.FILES)
        

        if form.is_valid():
            form.save()
        return redirect("restorent:add_menue")
    
@login_required
def delete_food_item(request):
    if request.method == 'POST':
        pk = request.POST.get('pk')
        print(pk)
        food_item = FoodItem.objects.filter(pk=pk)
        food_item.delete()
        return redirect('restorent:add_menue')
    
@login_required
def add_adjustment(request, pk):
    if request.method == 'POST':
        order = Order.objects.get(pk=pk)
        adjustment = request.POST.get('adjustment')
        print(adjustment)
        
        order.adjustment = adjustment
        order.save()
        return redirect('restorent:order_profile', pk)

@login_required
def restorent_detail(request):
    current_user = request.user
    restorent = current_user.userprofile.restorent
    if request.method == 'POST':
        form = UpdateRestorentDetail(request.POST, instance=restorent)
        if form.is_valid():
            form.save()
            return redirect('restorent:restorent_detail')
        
    form = UpdateRestorentDetail(instance=restorent)
    return render(request, 'restorent/restorent_detail.html', {'form': form}) 

@login_required
def add_tax(request):
    if request.method == 'POST':
        form = AddTax(request.POST)
        if form.is_valid():
            restorent = request.user.userprofile.restorent
            new_tax = form.save(commit=False)
            new_tax.restorent = restorent
            new_tax.save() 
            messages.success(request, 'New Tax is Added To Your Restorent')
            
            return redirect('restorent:add_tax')
    all_tax = request.user.userprofile.restorent.tax_set.all()
    form = AddTax()
    return render(request, 'restorent/add_tax.html', {'form': form, "all_tax": all_tax})


def show_menue(request, pk):
    # Show Menue of only this restorent
    table = get_object_or_404(Table, pk=pk)

    if table.vacent_status:
        try:
            if request.user.userprofile:
                last_order = Order.objects.filter(table=table).latest('start_time')
                return redirect('restorent:order_profile', last_order.pk)
            else:
                return HttpResponse('This Table alrady ocupied')
        
        except:
            return HttpResponse('This Table alrady ocupied')
        
    restorent = table.floor.restorent
    food_categories = FoodCategory.objects.filter(restorent=restorent)
    floor = table.floor
    tables = floor.table_set.order_by('id')
    tables = list(tables)

    table_number = tables.index(table)
    table_number += 1
    return render(request, 'restorent/show_menue.html', {'table': table, 'food_categories': food_categories, 'table_number': table_number})


def cart(request, pk):
    table = get_object_or_404(Table, pk=pk)

    floor = table.floor
    tables = floor.table_set.order_by('id')
    tables = list(tables)

    table_number = tables.index(table)
    table_number += 1

    restorent = floor.restorent
    return render(request, 'restorent/cart.html', {'table': table, 'table_number': table_number, 'restorent': restorent})

@login_required
def create_order(request, pk):
    if request.method == 'POST':
        table = Table.objects.get(pk=pk)

        order_data = request.POST['order_data']
        order_data = json.loads(order_data)
        
        new_order = Order(table=table, restorent=table.floor.restorent)
        new_order.save()

        # make the table vacent status = True
        table.vacent_status = True
        table.payment_panding = True
        table.order_panding = True
        table.save()
        # send this data to socket
        channel_layer = get_channel_layer()

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
        
        
        for item_id in order_data:
            item = order_data[item_id]
            OrderItems(food_type=item['item_type'], item_name = item['name'], item_quantity = item['quantity'], item_price=item['item_price'], order=new_order).save()
        

        return redirect('restorent:show_qr', new_order.pk)

@login_required
def all_orders(request):
    # all orders of this restorent
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
        except:
            start_date = timezone.now().date()
            end_date = timezone.now().date()

    orders = Order.objects.filter(restorent=restorent, start_time__date__range=(start_date, end_date) )
    return render(request, 'restorent/orderHistory.html', {'orders': orders, "start_date": start_date, "end_date": end_date})


@login_required
def order_profile(request, pk):
    order = Order.objects.get(pk=pk)
    try:
        table = order.table

        floor = table.floor
        tables = floor.table_set.order_by('id')
        tables = list(tables)

        table_number = tables.index(table)
        table_number += 1
    except:
        table_number = "Home Delivery"

    if request.method == 'POST':
        if hasattr(order, 'payment'):
            messages.error(request, 'Payment of this order is already done ! ')

        else:
            form = PaymentForm(request.POST)
            if form.is_valid():
                adjustment_value = form.cleaned_data['adjustment']
                payment = form.save(commit=False)
                payment.order = order
                order.end_time = timezone.now()
                order.adjustment = adjustment_value

                if table != None:
                    table = order.table
                    table.payment_panding = False

                    table.save()
                order.save()
                payment.save()

                file_name = f'qr{order.id}.png'
                media_path = settings.MEDIA_ROOT
                complete_path = os.path.join(media_path, 'qr_images', file_name)
                
                if os.path.exists(complete_path):
                    os.remove(complete_path)


                channel_layer = get_channel_layer()
                # send data to the payment channel
                if table != None:
                    async_to_sync(channel_layer.group_send)(
                        'payments',
                        {
                            'type': 'table_data',
                            'payment_data': json.dumps(
                                {'payment_id': payment.id,
                                'work': 'add_new_payment',
                                'status': 'success',
                                'order_id': order.id,
                                'transaction_id': order.transaction_id
                                }
                            )
                        }
                    )
                    # send data to dashboard socket
                    async_to_sync(channel_layer.group_send)(
                        'dashboard',
                        {
                        'type': 'table_data',
                        'dashboard_data': 
                            {
                                "table_vacent_status": table.vacent_status,
                                "order_panding": table.order_panding,
                                "payment_panding": table.payment_panding,
                                "pk": table.pk 
                            }
                        })


                    order.table.payment_panding = False
                return redirect('restorent:order_profile', pk)

    form = PaymentForm()
    return render(request, 'restorent/order_profile.html', {'order':order, 'table_number': table_number, 'form': form})

@login_required
def all_payments(request):
    # all payment of this restorent
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
        except:
            start_date = timezone.now().date()
            end_date = timezone.now().date()

    payments = Payment.objects.filter(order__restorent=restorent, timing__date__range=(start_date, end_date))
    return render(request, 'restorent/all_payments.html', {'payments': payments, "start_date": start_date, "end_date": end_date})


@login_required
def update_order_status(request, pk, status):
    try:
        order = Order.objects.get(pk=pk)
        table = order.table
        if status == 'true':
            order.food_delivered = True
            table.order_panding = False
        else:
            order.food_delivered = False
            table.order_panding = True
        table.save()
        order.save()
        
        # send order status to the socket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
        'dashboard',
        {
        'type': 'table_data',
        'dashboard_data': 
            {
                "table_vacent_status": table.vacent_status,
                "order_panding": table.order_panding,
                "payment_panding": table.payment_panding,
                "pk": table.pk
            }
        })

        if order.food_delivered == True and order.normal_table == False:
            table.delete()
    except:
        pass
    return HttpResponse("done")

@login_required
def edit_order(request, pk):
    order = Order.objects.get(pk=pk)
    if order.end_time != None:
        table = order.table
        messages.error(request, "Payment of This Order is Completed, So this is not Editable !")
        return redirect("restorent:order_profile", pk)

    else:
        if order.normal_table == True:
            order.delete()
            table.vacent_status = False
            table.save()
        
        else:
            messages.error(request, "Delivery Order's Are Not Editable !")
            return redirect("restorent:order_profile", pk)

    return redirect("restorent:show_menue", table.pk)


@login_required
def delete_payment(request, pk):
    try:
        payment = get_object_or_404(Payment, pk=pk)
        order = payment.order
        order.end_time = None
        payment.delete()
        order.save()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'payments',
            {
                'type': 'table_data',
                'payment_data': json.dumps(
                    {'payment_id': pk,
                     'work': 'delete',
                     'status': 'success',
                     'order_id': order.id
                    }
                )
            }
        )
        messages.success(request, f'Payment of Order: {order.pk} has been Added Successfully ! ')
        
    except Http404:
        messages.error(request, "This payment is no more in existence!")

    # redirect to previous page    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def delete_order(request):
    if request.method == 'POST':
        try:
            order_id = request.POST.get('order-id')
            order = Order.objects.get(pk=order_id)
            if order.normal_table:
                order.delete()

            else:
                table = order.table
                if table != None:
                    table.delete()
                order.delete()
            
            messages.success(request, f'Payment of Order: {order.pk} has been Added Successfully ! ')

        except Http404:
            messages.error(request, 'This Order is no more in Existence !')

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def kot(request, pk):
    order = Order.objects.get(pk=pk)
    try:
        table = order.table

        floor = table.floor
        tables = floor.table_set.order_by('id')
        tables = list(tables)

        table_number = tables.index(table)
        table_number += 1
    except:
        table_number = "Home Delivery"
    return render(request, 'restorent/kot.html', {"order": order, "table_number": table_number})

@login_required
def bill(request, pk):
    order = Order.objects.get(pk=pk)
    try:
        table = order.table

        floor = table.floor
        tables = floor.table_set.order_by('id')
        tables = list(tables)

        table_number = tables.index(table)
        table_number += 1
    except:
        table_number = "Home Delivery"
    return render(request, 'restorent/bill.html', {"order": order, "table_number": table_number})

# without login any body can get this link...

def show_qr(request, pk):
    order = Order.objects.get(pk=pk)
    if order.end_time != None:
        return redirect('restorent:payment_added_successfully')
    
    transaction_id = order.generate_transaction_id()
    order.transaction_id = transaction_id
    order.save()
    restorent = order.table.floor.restorent
    upi_id = restorent.upi_id
    owner_name = restorent.owner_name
    amount = order.order_amount()
    total_amount = order.complete_amount()


    url = f'upi://pay?pa={upi_id}&pn={owner_name}&tr={transaction_id}&tn=restorent payment&am={total_amount}&cu=INR'
    file_name = f'qr{order.id}'
    media_path = settings.MEDIA_ROOT
    complete_path = os.path.join(media_path, 'qr_images', file_name)
    file_name = generate_qr(complete_path, url)

    return render(request, 'restorent/qr_template.html', {"order": order, 'total_amount': total_amount})

def payment_added_successfully(request):
    return render(request,'restorent/payment_added_successfully.html')


def home_delivery(request, pk):
    restorent = Restorent.objects.get(pk=pk)
    food_categories = FoodCategory.objects.filter(restorent=restorent)
    return render(request, 'restorent/home_delivery.html', {'food_categories': food_categories, "restorent": restorent})

def delivery_cart(request, pk):
    if request.method == 'POST':
        restorent = Restorent.objects.get(pk=pk)
        floor = Floor.objects.filter(restorent=restorent, name='Delivery')
        floor_count = floor.count()
        if floor_count == 0:
            # create new floor
            floor = Floor(name='Delivery' ,restorent=restorent)
            floor.save()
        
        else:
            floor = floor.first()
        # adding the new table to the restorent
        table = Table(floor=floor)
        table.vacent_status = True
        table.save()
        order_data = request.POST['order_data']

        user_information = request.POST['user_detail']
        user_information = json.loads(user_information)

        order_data = json.loads(order_data)
        new_order = Order(table=table, restorent=restorent)
        new_order.normal_table = False

        new_order.name = user_information['name']
        new_order.phone_number = user_information['phone_number']
        new_order.address = user_information['address']
        new_order.save()

        # make the table vacent status = True
        table.vacent_status = True
        table.payment_panding = True
        table.order_panding = True
        table.save()
        # send this data to socket
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
                    'dashboard',
                    {
                    'type': 'table_data',
                    'dashboard_data': {
                            "table_vacent_status": table.vacent_status,
                            "order_panding": table.order_panding,
                            "payment_panding": table.payment_panding,
                            "pk": table.pk,
                            "table_name": user_information['name'],
                            "restorent_id": restorent.id,
                        }
                })
        
        
        for item_id in order_data:
            item = order_data[item_id]
            OrderItems(food_type=item['item_type'], item_name = item['name'], item_quantity = item['quantity'], item_price=item['item_price'], order=new_order).save()
        

        return redirect('restorent:show_qr', new_order.pk)

    restorent = Restorent.objects.get(pk=pk)
    return render(request, 'restorent/delivery_cart.html', {'restorent': restorent})

def show_table_status(request, pk):
    table = Table.objects.get(pk=pk)
    return render(request, 'restorent/show_table_status.html', {"table": table})



def sign_up_page(request):
    if request.method == 'POST':
        form = RestorentForm(request.POST)
        if form.is_valid():
            restorent_name = form.cleaned_data['restorent_name']
            address = form.cleaned_data['address']
            name = form.cleaned_data['name']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']

            # CREATE THE USER
            user = User.objects.create(
                username=phone_number,
                password=make_password(password)
            )

            # CREATE THE RESTORENT
            restorent = Restorent.objects.create(
                name=restorent_name,
                owner_name = name,
                address = address,
                phone_number=phone_number
            )

            # CREATE USER PROFILE
            UserProfile.objects.create(
                user=user,
                restorent=restorent
            )

            return HttpResponse(f'new user is created.... | Thankyou {restorent_name}')

    form = RestorentForm()
    return render(request, 'restorent/sign_up.html', {'form': form})
