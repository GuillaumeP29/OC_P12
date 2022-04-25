from django.contrib import admin

from .models import (
    Address, Company, Employee, Client, Event, Contract, ClientAssociation, EventAssociation
    )

# Register your models here.
admin.site.register(
    [Address, Company, Employee, Client, Event, Contract, ClientAssociation, EventAssociation]
    )
