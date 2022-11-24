from django.conf import settings
from django.db import models


class Event(models.Model):
    client = models.ForeignKey("Client", on_delete=models.PROTECT)
    support_contact = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    attendees = models.IntegerField()
    date = models.DateField()
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
