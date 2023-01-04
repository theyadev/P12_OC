from rest_framework import serializers

from ..models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'client', 'support_contact', 'attendees', 'notes', 'date', 'created_at', 'updated_at']
