import logging

from ..decorators import check_fields
from ..models import Client
from ..permissions import IsSalesGroup, IsSupportGroup
from ..serializers import ClientSerializer

from django.contrib.auth.models import User
from django.db.models import Q

from rest_framework.decorators import authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class ClientView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, client_id=None):
        if not client_id:
            clients = Client.objects.all()

            if 'search' in request.GET:
                clients = clients.filter(
                    Q(first_name__icontains=request.GET['search']) |
                    Q(last_name__icontains=request.GET['search']) |
                    Q(email__icontains=request.GET['search']) |
                    Q(company_name__icontains=request.GET['search'])
                )

            return Response(ClientSerializer(clients, many=True).data)

        if not Client.objects.filter(id=client_id).exists():
            logger.warning(f'Client {client_id} not found')
            return Response(status=404, data={'error': 'Client not found.'})

        client = Client.objects.get(id=client_id)

        return Response(ClientSerializer(client).data)

    @authentication_classes([IsSalesGroup])
    @check_fields(['first_name', 'email', 'last_name'])
    def post(self, request, client_id=None):
        if Client.objects.filter(Q(email=request.data['email'])).exists():
            logger.warning(f'Client {request.data["email"]} already exists')
            return Response(status=400, data={'error': 'Client already exists.'})

        client = Client.objects.create(
            first_name=request.data['first_name'],
            last_name=request.data['last_name'],
            email=request.data['email'],
            sales_contact=request.user,
            phone=request.data.get('phone', ""),
            mobile=request.data.get('mobile', ""),
            company_name=request.data.get('company_name', ""),
        )

        return Response(ClientSerializer(client).data)

    @authentication_classes([IsSalesGroup])
    def put(self, request, client_id):
        if not Client.objects.filter(id=client_id).exists():
            logger.warning(f'Client {client_id} not found')
            return Response(status=404, data={'error': 'Client not found.'})

        client = Client.objects.get(id=client_id)

        if 'first_name' in request.data:
            client.first_name = request.data['first_name']

        if 'last_name' in request.data:
            client.last_name = request.data['last_name']

        if 'email' in request.data:
            client.email = request.data['email']

        if 'phone' in request.data:
            client.phone = request.data['phone']

        if 'mobile' in request.data:
            client.mobile = request.data['mobile']

        if 'company_name' in request.data:
            client.company_name = request.data['company_name']

        client.save()

        return Response(ClientSerializer(client).data)

    @authentication_classes([IsSalesGroup])
    def delete(self, request, client_id):
        if not Client.objects.filter(id=client_id).exists():
            logger.warning(f'Client {client_id} not found')
            return Response(status=404, data={'error': 'Client not found.'})

        client = Client.objects.get(id=client_id)

        client.delete()

        return Response(status=204)
