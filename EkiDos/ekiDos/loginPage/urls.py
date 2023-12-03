from django.urls import path

from .views import *

app_name = 'loginPage'

urlpatterns = [
    path('', LoginUserView.as_view(), name='loginView'),
    path('register/', RegisterUserView.as_view(), name='registerUser'),
    
]

