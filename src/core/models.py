from django.db import models
from django.contrib.auth.models import AbstractBaseUser, Group
from datetime import datetime
from abc import ABC
from django.contrib.auth.validators import UnicodeUsernameValidator

# Create your models here.
class TimeStamp(ABC):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


# class TimeStamp(models.Model):
#     date_created = models.DateTimeField(auto_now_add=True)
#     date_updated = models.DateTimeField(auto_now=True)

#     class Meta:
#         abstract = True


class ABCModelMeta(type(ABC), type(models.Model)):
    """New meta class to figure out of metaclass conflicts during multiple inheritance"""
    pass


class Address(models.Model):
    number = models.IntegerField(blank=True, null=True)
    street = models.CharField(max_length=500)
    city = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.number} {self.street}, {self.city}, {self.country}'


class Company(models.Model):
    name = models.CharField(max_length=200)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name


class Person(models.Model, TimeStamp, ABC, metaclass=ABCModelMeta):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    phone = models.CharField(max_length=20, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)


class Employee(AbstractBaseUser, Person):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        ('username'),
        max_length=150,
        unique=True,
        help_text=('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': ("A user with that username already exists."),
        },
    )
    is_staff = models.BooleanField(default=False)
    date_hired = models.DateTimeField(default=datetime.now)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.last_name.upper()} {self.last_name} - {self.group.name}'


class Client(Person, TimeStamp):
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, blank=True, null=True)
    sales_contact = models.ForeignKey(Employee, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.last_name.upper()} {self.first_name}'


class Event(models.Model, TimeStamp, metaclass=ABCModelMeta):

    class EventStatus(models.Model):
        name = models.CharField(primary_key=True , max_length=50)

    name = models.CharField(max_length=500)
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    event_status = models.ForeignKey(EventStatus, on_delete=models.SET_NULL, blank=True, null=True)
    attendees = models.IntegerField(blank=True, null=True)
    event_date = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Contract(models.Model, TimeStamp, metaclass=ABCModelMeta):
    signature_date = models.DateTimeField(blank=True, null=True)
    amount = models.FloatField(null=True)
    payment_due_date = models.DateTimeField()
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.id


class Association(TimeStamp, ABC):
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING)


class ClientAssociation(models.Model, Association, metaclass=ABCModelMeta):
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)


class EventAssociation(models.Model, Association, metaclass=ABCModelMeta):
    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING)


class ContractAssociation(models.Model, Association, metaclass=ABCModelMeta):
    contract = models.ForeignKey(Contract, on_delete=models.DO_NOTHING)
