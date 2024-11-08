from django.urls import path, include
from . import views

urlpatterns = [
    path('register-user/', views.RegisterLabUserView.as_view(), name='register_user')
]