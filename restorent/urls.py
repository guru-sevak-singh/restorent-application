from django.urls import path
from . import views
from django.contrib.auth import views as authontication_views


app_name = "restorent"
urlpatterns = [
    path('', views.index, name='index'),
    path('login', authontication_views.LoginView.as_view(template_name='restorent/login.html'), name='login'),
    path('setting', views.setting, name='settings'),
    path('add_sitting', views.add_sitting_area, name='add_sitting'),
    path('add_area', views.add_area, name='add_area'),
    path('add_table/<floor_id>', views.add_table, name='add_table'),
    path('add_menue', views.add_menue, name='add_menue'),
    path('add_category', views.add_category, name='add_category'),
    path('add_food_item', views.add_food_item, name='add_food_item'),
    path('delete_food_item', views.delete_food_item, name="delete_food_item"),
    path('add_food_item/<int:pk>', views.add_food_item, name='edit_food_item'),
    path('edit_order/<pk>', views.edit_order, name='edit_order'),
    path('show_menue/<pk>', views.show_menue, name='show_menue'),
    path('delete_order', views.delete_order, name='delete_order'),
    path('cart/<pk>', views.cart, name='cart'),
    path('create_order/<pk>', views.create_order, name='create_order'),
    path('all_orders', views.all_orders, name='all_orders'),
    path('order_profile/<pk>', views.order_profile, name='order_profile'),
    path('add_adjustment/<pk>', views.add_adjustment, name='add_adjustment'),
    path('all_payments', views.all_payments, name='all_payments'),
    path('show_qr/<pk>', views.show_qr, name='show_qr'),
    path('restorent_detail', views.restorent_detail, name='restorent_detail'),
    path('delete_payment/<pk>', views.delete_payment, name='delete_payment'),
    path('payment_added_successfully', views.payment_added_successfully, name='payment_added_successfully'),
    path('add_tax', views.add_tax, name='add_tax'),
    path('update_order_status/<pk>/<status>/', views.update_order_status, name='update_order_status'),
    path('home_delivery/<pk>', views.home_delivery, name='home_delivery'),
    path('delivery_cart/<pk>', views.delivery_cart, name='delivery_cart'),
    path('show_table_status/<pk>', views.show_table_status, name='show_table_status'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('kot/<pk>', views.kot, name='kot'),
    path('bill/<pk>', views.bill, name='bill'),
    path('sign_up', views.sign_up_page, name='sign_up'),
]