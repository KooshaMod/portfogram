from django.urls import path
from . import views

urlpatterns = [
	path('',views.stock, name='stock'),
	path('api',views.api, name='api'),
	path('test', views.last_shares_records, name='last_shares_records'),
]
