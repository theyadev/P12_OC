from django.db import models


class ContractStatus(models.Model):
    class Meta:
        verbose_name_plural = "Contract Statuses"

    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
