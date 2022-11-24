from django.contrib import admin
from .models.Client import Client
from .models.Contract import Contract
from .models.ContractStatus import ContractStatus
from .models.Event import Event

admin.site.register(Client)
admin.site.register(Contract)
admin.site.register(ContractStatus)
admin.site.register(Event)
