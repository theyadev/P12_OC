from ..decorators import check_fields
from ..models import Client, Contract, Event
from ..permissions import IsSalesGroup, IsSupportGroup
from ..serializers import ClientSerializer, ContractSerializer, EventSerializer

from django.contrib.auth.models import User
from django.db.models import Q

from rest_framework.decorators import authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class EventView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id=None):
        if not event_id:
            events = Event.objects.all().filter(
                Q(support_contact=request.user) | Q(
                    client__sales_contact=request.user)
            )

            return Response(EventSerializer(events, many=True).data)

        if not Event.objects.filter(id=event_id).exists():
            return Response(status=404, data={'error': 'Event not found.'})

        event = Event.objects.get(id=event_id)

        if event.support_contact != request.user and event.client.sales_contact != request.user:
            return Response(status=403, data={'error': 'Not authorized.'})

        return Response(EventSerializer(event).data)

    @authentication_classes([IsSalesGroup])
    @check_fields(['client', 'status', 'support_contact', 'description', 'date'])
    def post(self, request, event_id=None):
        if not User.objects.filter(id=request.data['support_contact']).exists():
            return Response(status=404, data={'error': 'Support contact not found.'})

        if not Client.objects.filter(id=request.data['client']).exists():
            return Response(status=404, data={'error': 'Client not found.'})

        client = Client.objects.get(id=request.data['client'])

        if client.sales_contact != request.user:
            return Response(status=403, data={'error': 'Not authorized.'})

        event = Event.objects.create(
            support_contact=request.user,
            client=client,
            status=request.data['status'],
            description=request.data['description'],
            date=request.data['date'],
        )

        return Response(EventSerializer(event).data)

    @authentication_classes([IsSupportGroup])
    def put(self, request, event_id):
        if not Event.objects.filter(id=event_id).exists():
            return Response(status=404, data={'error': 'Event not found.'})

        event = Event.objects.get(id=event_id)

        if event.support_contact != request.user:
            return Response(status=403, data={'error': 'Not authorized.'})

        if 'status' in request.data:
            event.status = request.data['status']

        if 'description' in request.data:
            event.description = request.data['description']

        if 'date' in request.data:
            event.date = request.data['date']

        event.save()

        return Response(EventSerializer(event).data)

    @authentication_classes([IsSupportGroup])
    def delete(self, request, event_id):
        if not Event.objects.filter(id=event_id).exists():
            return Response(status=404, data={'error': 'Event not found.'})

        event = Event.objects.get(id=event_id)

        if event.support_contact != request.user:
            return Response(status=403, data={'error': 'Not authorized.'})

        event.delete()

        return Response(status=204)
