from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.RegisterLabUserView.as_view(), name='register_user'),
    path('list/', views.LabUserListView.as_view(), name='list_user'),
    path('update/', views.LabUserUpdateView.as_view(), name='update_user'),
    path('delete/', views.LabUserDeleteView.as_view(), name='delete_user'),
]