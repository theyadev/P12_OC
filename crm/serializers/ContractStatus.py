from rest_framework import serializers

from ..models import ContractStatus


class ContractStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractStatus
        fields = ['id', 'name', ]
