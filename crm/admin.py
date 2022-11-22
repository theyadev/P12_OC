from django.contrib import admin
from .models.Client import Client
from .models.Contract import Contract
from .models.Event import Event

admin.site.register(Client)
admin.site.register(Contract)
admin.site.register(Event)





# Register your models here.
