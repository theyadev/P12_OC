from rest_framework import serializers

from models.Contract import Contract


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ['id', 'sales_contact', 'client',
                  'status', 'amount', 'payment_due', ]
