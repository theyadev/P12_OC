from .admins.Client import ClientAdmin
from .admins.Contract import ContractAdmin
from .admins.ContractStatus import ContractStatusAdmin
from .admins.Event import EventAdmin

from .models.Client import Client
from .models.Contract import Contract
from .models.ContractStatus import ContractStatus
from .models.Event import Event

from django.contrib import admin

admin.site.register(Client, ClientAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(ContractStatus, ContractStatusAdmin)
admin.site.register(Event, EventAdmin)
