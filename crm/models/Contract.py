from django.conf import settings
from django.db import models

from rest_framework import serializers


class Contract(models.Model):
    sales_contact = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    client = models.ForeignKey("Client", on_delete=models.PROTECT)
    status = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_due = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ContractSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Contract
        fields = ['id', 'sales_contact', 'client',
                  'status', 'amount', 'payment_due', ]
