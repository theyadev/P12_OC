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


class ClientView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, client_id=None):
        if not client_id:
            clients = Client.objects.all()

            return Response(ClientSerializer(clients, many=True).data)

        if not Client.objects.filter(id=client_id).exists():
            return Response(status=404, data={'error': 'Client not found.'})

        client = Client.objects.get(id=client_id)

        return Response(ClientSerializer(client).data)

    @authentication_classes([IsSalesGroup])
    @check_fields(['first_name', 'email', 'last_name', 'sales_contact'])
    def post(self, request, client_id=None):
        if not User.objects.filter(id=request.data['sales_contact']).exists():
            return Response(status=404, data={'error': 'Sales contact not found.'})

        if Client.objects.filter(Q(email=request.data['email'])).exists():
            return Response(status=400, data={'error': 'Client already exists.'})

        sales_contact = User.objects.get(id=request.data['sales_contact'])

        client = Client.objects.create(
            first_name=request.data['first_name'],
            last_name=request.data['last_name'],
            email=request.data['email'],
            sales_contact=sales_contact,
            phone=request.data.get('phone', ""),
            mobile=request.data.get('mobile', ""),
            company_name=request.data.get('company_name', ""),
        )

        return Response(ClientSerializer(client).data)

    @authentication_classes([IsSalesGroup])
    def update(self, request, client_id):
        if not Client.objects.filter(id=client_id).exists():
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
