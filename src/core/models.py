from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.utils import timezone

# Create your models here.
class TimeStamp(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_revoked = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True


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


class Person(TimeStamp):
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(max_length=150, blank=True, unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        abstract = True


class Employee(AbstractBaseUser, Person, PermissionsMixin):

    username = models.CharField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "password"]

    class Meta:
        abstract = False

    def __str__(self):
        return f'{self.last_name.upper()} {self.first_name}'


class Client(Person):
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, blank=True, null=True)
    sales_contact = models.ManyToManyField(Employee, blank=True, through="ClientAssociation")

    class Meta:
        abstract = False

    def __str__(self):
        return f'{self.last_name.upper()} {self.first_name}'


class Event(TimeStamp):

    class EventStatus(models.Model):
        name = models.CharField(primary_key=True , max_length=50)

    name = models.CharField(max_length=500)
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING, default=0)
    support_contact = models.ManyToManyField(Employee, blank=True, through="EventAssociation")
    event_status = models.ForeignKey(EventStatus, on_delete=models.SET_NULL, blank=True, null=True)
    attendees = models.IntegerField(blank=True, null=True)
    event_date = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True)

    class Meta:
        abstract = False

    def __str__(self):
        return self.name


class Contract(TimeStamp):
    signature_date = models.DateTimeField(blank=True, null=True)
    amount = models.FloatField(null=True)
    payment_due_date = models.DateTimeField()
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING, default=0)

    class Meta:
        abstract = False

    def __str__(self):
        return self.id


class Association(TimeStamp):
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, default=0)

    class Meta:
        abstract = True


class ClientAssociation(Association):
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING, default=0)

    class Meta:
        abstract = False


class EventAssociation(Association):
    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING, default=0)

    class Meta:
        abstract = False
