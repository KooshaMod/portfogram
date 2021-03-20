from django.urls import path
from . import views

urlpatterns = [
	path('',views.agent_ren, name='agent_ren'),
]
