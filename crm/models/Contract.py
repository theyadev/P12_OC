from django.conf import settings
from django.db import models


class Contract(models.Model):
    class Meta:
        permissions = [
            ('view_own_contract', 'Can view own contract'),
            ('edit_own_contract', 'Can update, delete own contract'),
        ]

    sales_contact = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, editable=False)
    client = models.ForeignKey("Client", on_delete=models.PROTECT)
    status = models.ForeignKey("ContractStatus", on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_due = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.client} - {self.status}"
