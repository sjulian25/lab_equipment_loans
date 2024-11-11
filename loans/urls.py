from django.urls import path
from .views import LoanCreateView, LoanReturnView

urlpatterns = [
    path('loans/', LoanCreateView.as_view(), name='loan-create'),
    path('loans/return/<int:pk>/', LoanReturnView.as_view(), name='loan-return'),
]