from . import views

from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

urlpatterns = [
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('client', views.ClientView.as_view(), name='client_sales'),
    path('client/<int:client_id>', views.ClientView.as_view(), name='client_sales'),
]
