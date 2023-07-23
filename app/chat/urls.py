from django.urls import path

from chat.views import lobby

app_name = 'chat'

urlpatterns = [
    path('lobby/', lobby, name='lobby')
]
