from django.urls import path
from . import api_views as views

app_name = 'restorent_api'
urlpatterns = [
    path('add_payment_by_url', views.add_payment_by_url, name='add_payment_url'),
    path('dashboard_data', views.dashboard_data, name='dashboard_data'),
    path('get_yearly_revenue/<int:year>', views.get_yearly_revenue, name='yearly_revenue'),
]