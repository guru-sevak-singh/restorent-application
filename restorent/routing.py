from django.urls import path

from .counsumers.dashboardconsumer import DashboardConsumer
from .counsumers.paymentsconsumers import PaymentConsumer
from .counsumers.softwareconsumer import SoftwareConsumer

websocket_urlpatterns = [
    path('ws/dashboard_data/', DashboardConsumer.as_asgi()),
    path('ws/payment_data/', PaymentConsumer.as_asgi()),
    path('ws/software_socket/', SoftwareConsumer.as_asgi()),
]