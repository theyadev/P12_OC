from rest_framework import serializers

from ..models import Contract
from . import ClientSerializer


class ContractSerializer(serializers.ModelSerializer):
    # serialize id username and id
    sales_contact = serializers.SerializerMethodField()
    status = serializers.StringRelatedField()
    client = ClientSerializer()

    def get_sales_contact(self, obj):
        return {'id': obj.sales_contact.id, 'username': obj.sales_contact.username}

    class Meta:
        model = Contract
        fields = ['id', 'sales_contact', 'client',
                  'status', 'amount', 'payment_due', ]
