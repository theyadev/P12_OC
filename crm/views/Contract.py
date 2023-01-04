import logging

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

logger = logging.getLogger(__name__)


class ContractView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, contract_id=None):
        if not contract_id:
            contracts = Contract.objects.all().filter(
                Q(sales_contact=request.user) | Q(
                    client__sales_contact=request.user)
            )

            if 'search' in request.GET:
                contracts = contracts.filter(
                    Q(client__first_name__icontains=request.GET['search']) |
                    Q(client__last_name__icontains=request.GET['search']) |
                    Q(client__email__icontains=request.GET['search']) |
                    Q(client__company_name__icontains=request.GET['search']) |
                    Q(payment_due__icontains=request.GET['search']) |
                    Q(amount__icontains=request.GET['search'])
                )

            return Response(ContractSerializer(contracts, many=True).data)

        if not Contract.objects.filter(id=contract_id).exists():
            logger.warning(f'Contract {contract_id} not found')
            return Response(status=404, data={'error': 'Contract not found.'})

        contract = Contract.objects.get(id=contract_id)

        if contract.sales_contact != request.user and contract.client.sales_contact != request.user:
            logger.warning(f'Contract {contract_id} not authorized')
            return Response(status=403, data={'error': 'Not authorized.'})

        return Response(ContractSerializer(contract).data)

    @authentication_classes([IsSalesGroup])
    @check_fields(['client', 'status', 'amount', 'payment_due'])
    def post(self, request, contract_id=None):
        if not Client.objects.filter(id=request.data['client']).exists():
            logger.warning(f'Client {request.data["client"]} not found')
            return Response(status=404, data={'error': 'Client not found.'})

        if not ContractStatus.objects.filter(id=request.data['status']).exists():
            logger.warning(
                f'Contract status {request.data["status"]} not found')
            return Response(status=404, data={'error': 'Contract status not found.'})

        client = Client.objects.get(id=request.data['client'])
        contract_status = ContractStatus.objects.get(id=request.data['status'])

        if client.sales_contact != request.user:
            logger.warning(f'Client {client.id} not authorized')
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
            logger.warning(f'Contract {contract_id} not found')
            return Response(status=404, data={'error': 'Contract not found.'})

        contract = Contract.objects.get(id=contract_id)

        if contract.sales_contact != request.user and contract.client.sales_contact != request.user:
            logger.warning(f'Contract {contract_id} not authorized')
            return Response(status=403, data={'error': 'Not authorized.'})

        if 'status' in request.data:
            if not ContractStatus.objects.filter(id=request.data['status']).exists():
                logger.warning(
                    f'Contract status {request.data["status"]} not found')
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
            logger.warning(f'Contract {contract_id} not found')
            return Response(status=404, data={'error': 'Contract not found.'})

        contract = Contract.objects.get(id=contract_id)

        if contract.sales_contact != request.user and contract.client.sales_contact != request.user:
            logger.warning(f'Contract {contract_id} not authorized')
            return Response(status=403, data={'error': 'Not authorized.'})

        contract.delete()

        return Response(status=204)
