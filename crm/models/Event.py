from django.conf import settings
from django.db import models


class Event(models.Model):
    class Meta:
        ordering = ['date']
        permissions = [
            ('view_own_event', 'Can view own event'),
            ('edit_own_event', 'Can update, delete own event'),
        ]

    client = models.ForeignKey("Client", on_delete=models.PROTECT)
    support_contact = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    attendees = models.IntegerField()
    date = models.DateField()
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.client} - {self.date} ({self.attendees} attendees)"
