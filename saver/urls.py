from django.urls import path
from . import views

urlpatterns = [
	path('',views.saver, name='saver'),
]
