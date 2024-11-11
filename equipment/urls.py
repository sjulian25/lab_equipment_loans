from django.urls import path, include
from . import views

urlpatterns = [
    path('equipment/', views.EquipmentView.as_view(), name='equipment-list'),
    path('equipment/<str:equipment_id>/', views.EquipmentView.as_view(), name='equipment-detail'),
]