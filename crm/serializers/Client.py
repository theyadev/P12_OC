

from rest_framework import serializers

from models.Client import Client


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'mobile',
                  'company_name', 'sales_contact', 'created_at', 'updated_at']
