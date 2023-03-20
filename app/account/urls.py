from django.urls import path
from account.views import UserSignupView, UserActivateView

app_name = 'account'

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('activate/<uuid:username>/', UserActivateView.as_view(), name='activate'),
]
