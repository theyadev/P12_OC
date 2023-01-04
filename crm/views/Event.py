import logging
import re

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


logger = logging.getLogger(__name__)


def is_valid_date(date_string):
    regex = r'\d{4}-\d{2}-\d{2}'
    if re.match(regex, date_string):
        return True
    return False


class EventView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id=None):
        if not event_id:
            events = Event.objects.all().filter(
                Q(support_contact=request.user) | Q(
                    client__sales_contact=request.user)
            )

            if 'search' in request.GET:
                events = events.filter(
                    Q(client__first_name__icontains=request.GET['search']) |
                    Q(client__last_name__icontains=request.GET['search']) |
                    Q(client__email__icontains=request.GET['search']) |
                    Q(date__icontains=request.GET['search'])
                )

            return Response(EventSerializer(events, many=True).data)

        if not Event.objects.filter(id=event_id).exists():
            logger.warning(f'Event {event_id} not found')
            return Response(status=404, data={'error': 'Event not found.'})

        event = Event.objects.get(id=event_id)

        if event.support_contact != request.user and event.client.sales_contact != request.user:
            logger.warning(
                f'User {request.user} not authorized to view event {event_id}')
            return Response(status=403, data={'error': 'Not authorized.'})

        return Response(EventSerializer(event).data)

    @authentication_classes([IsSalesGroup])
    @check_fields(['client', 'support_contact', 'notes', 'date', 'attendees'])
    def post(self, request, event_id=None):
        if not User.objects.filter(id=request.data['support_contact']).exists():
            logger.warning(
                f'Support contact {request.data["support_contact"]} not found')
            return Response(status=404, data={'error': 'Support contact not found.'})

        if not Client.objects.filter(id=request.data['client']).exists():
            logger.warning(f'Client {request.data["client"]} not found')
            return Response(status=404, data={'error': 'Client not found.'})

        client = Client.objects.get(id=request.data['client'])

        if client.sales_contact != request.user:
            logger.warning(
                f'User {request.user} not authorized to create event for client {client.id}')
            return Response(status=403, data={'error': 'Not authorized.'})

        if not is_valid_date(request.data['date']):
            logger.warning(f'Invalid date format: {request.data["date"]}')
            return Response(status=400, data={'error': 'Invalid date format. Must be YYYY-MM-DD'})

        event = Event.objects.create(
            support_contact=request.user,
            client=client,
            notes=request.data['notes'],
            date=request.data['date'],
            attendees=request.data['attendees']
        )

        return Response(EventSerializer(event).data)

    @authentication_classes([IsSupportGroup])
    def put(self, request, event_id):
        if not Event.objects.filter(id=event_id).exists():
            logger.warning(f'Event {event_id} not found')
            return Response(status=404, data={'error': 'Event not found.'})

        event = Event.objects.get(id=event_id)

        if event.support_contact != request.user:
            logger.warning(
                f'User {request.user} not authorized to edit event {event_id}')
            return Response(status=403, data={'error': 'Not authorized.'})

        if 'attendees' in request.data:
            event.attendees = request.data['attendees']

        if 'notes' in request.data:
            event.description = request.data['notes']

        if 'date' in request.data:
            event.date = request.data['date']

        if 'support_contact' in request.data:
            if not User.objects.filter(id=request.data['support_contact']).exists():
                logger.warning(
                    f'Support contact {request.data["support_contact"]} not found')
                return Response(status=404, data={'error': 'Support contact not found.'})

            event.support_contact = request.data['support_contact']

        event.save()

        return Response(EventSerializer(event).data)

    @authentication_classes([IsSupportGroup])
    def delete(self, request, event_id):
        if not Event.objects.filter(id=event_id).exists():
            logger.warning(f'Event {event_id} not found')
            return Response(status=404, data={'error': 'Event not found.'})

        event = Event.objects.get(id=event_id)

        if event.support_contact != request.user:
            logger.warning(
                f'User {request.user} not authorized to delete event {event_id}')
            return Response(status=403, data={'error': 'Not authorized.'})

        event.delete()

        return Response(status=204)
