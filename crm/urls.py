from . import views

from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

urlpatterns = [
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('client', views.ClientView.as_view(), name='client_sales'),
    path('client/<int:client_id>', views.ClientView.as_view(), name='client_sales'),
    path('contract', views.ContractView.as_view(), name='contract_sales'),
    path('contract/<int:contract_id>', views.ContractView.as_view(), name='contract_sales'),
    path('event', views.EventView.as_view(), name='event_sales'),
    path('event/<int:event_id>', views.EventView.as_view(), name='event_sales'),
]
