from ..decorators import check_fields
from ..models import Client, Contract, ContractStatus
from ..permissions import IsSalesGroup, IsSupportGroup
from ..serializers import ClientSerializer, ContractSerializer

from django.contrib.auth.models import User
from django.db.models import Q

from rest_framework.decorators import authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class ContractView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, contract_id=None):
        if not contract_id:
            contracts = Contract.objects.all().filter(
                Q(sales_contact=request.user) | Q(
                    client__sales_contact=request.user)
            )

            return Response(ContractSerializer(contracts, many=True).data)

        if not Contract.objects.filter(id=contract_id).exists():
            return Response(status=404, data={'error': 'Contract not found.'})

        contract = Contract.objects.get(id=contract_id)

        if contract.sales_contact != request.user and contract.client.sales_contact != request.user:
            return Response(status=403, data={'error': 'Not authorized.'})

        return Response(ContractSerializer(contract).data)

    @authentication_classes([IsSalesGroup])
    @check_fields(['client', 'status', 'amount', 'payment_due'])
    def post(self, request, contract_id=None):
        if not Client.objects.filter(id=request.data['client']).exists():
            return Response(status=404, data={'error': 'Client not found.'})

        if not ContractStatus.objects.filter(id=request.data['status']).exists():
            return Response(status=404, data={'error': 'Contract status not found.'})

        client = Client.objects.get(id=request.data['client'])
        contract_status = ContractStatus.objects.get(id=request.data['status'])

        if client.sales_contact != request.user:
            return Response(status=403, data={'error': 'Not authorized.'})

        contract = Contract.objects.create(
            sales_contact=request.user,
            client=client,
            status=contract_status,
            amount=request.data['amount'],
            payment_due=request.data['payment_due'],
        )

        return Response(ContractSerializer(contract).data)

    @authentication_classes([IsSalesGroup])
    def put(self, request, contract_id):
        if not Contract.objects.filter(id=contract_id).exists():
            return Response(status=404, data={'error': 'Contract not found.'})

        contract = Contract.objects.get(id=contract_id)

        if contract.sales_contact != request.user and contract.client.sales_contact != request.user:
            return Response(status=403, data={'error': 'Not authorized.'})

        if 'status' in request.data:
            if not ContractStatus.objects.filter(id=request.data['status']).exists():
                return Response(status=404, data={'error': 'Contract status not found.'})

            contract_status = ContractStatus.objects.get(
                id=request.data['status'])
            contract.status = contract_status

        contract.amount = request.data.get('amount', contract.amount)
        contract.payment_due = request.data.get(
            'payment_due', contract.payment_due)
        contract.save()

        return Response(ContractSerializer(contract).data)

    @authentication_classes([IsSalesGroup])
    def delete(self, request, contract_id):
        if not Contract.objects.filter(id=contract_id).exists():
            return Response(status=404, data={'error': 'Contract not found.'})

        contract = Contract.objects.get(id=contract_id)

        if contract.sales_contact != request.user and contract.client.sales_contact != request.user:
            return Response(status=403, data={'error': 'Not authorized.'})

        contract.delete()

        return Response(status=204)
