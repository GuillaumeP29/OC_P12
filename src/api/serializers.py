from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from core.models import Address, Company, Group, Employee, Client, Event, Contract


class AdressListSerializer(ModelSerializer):
    class Meta:
        model = Address
        fileds = ['number', 'street', 'city', 'country']


class AddressDetailSerializer(ModelSerializer):
    class Meta:
        model = Address
        fileds = ['id', 'number', 'street','city', 'zip_code', 'country']


class CompanyNameSerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = ['name']

    def validate_name(self, value):
        if Company.objects.filter(name=value).exists():
            raise serializers.ValidationError('Another company has already this name')
        return value


class CompanyListSerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name']


class CompanyDetailSerializer(ModelSerializer):
    address = AddressDetailSerializer()

    class Meta:
        model = Company
        fields = ['id', 'name', 'address']


class GroupNameSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']


class EmployeeListSerializer(ModelSerializer):
    group = GroupNameSerializer()

    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'last_name', 'group']


class EmployeeDetailSerializer(ModelSerializer):
    group = GroupNameSerializer()

    class Meta:
        model = Employee
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone', 'mobile',
            'is_staff', 'date_hired', 'date_updated', 'group'
            ]


class ClientListSerializer(ModelSerializer):
    company = CompanyNameSerializer()

    class Meta:
        model = Client
        fields = ['id', 'last_name', 'first_name', 'company']


class ClientDetailSerializer(ModelSerializer):
    company = CompanyDetailSerializer()

    class Meta:
        model = Client
        fields = ['id', 'last_name', 'first_name', 'email', 'phone', 'mobile', 'company']


class EventStatusSerializer(ModelSerializer):
    class Meta:
        model = Event.EventStatus
        fields = ['name']


class EventListSerializer(ModelSerializer):
    event_status = EventStatusSerializer()

    class Meta:
        model = Event
        fields = ['name', 'client', 'event_status', 'event_date']


class EventDetailSerializer(ModelSerializer):
    event_status = EventStatusSerializer()

    class Meta:
        model = Event
        fields = ['name', 'client', 'event_status', 'attendees', 'event_date', 'notes']


class ContractListSerializer(ModelSerializer):
    class Meta:
        model = Contract
        fields = ['id', 'client']


class ContracDetailSerializer(ModelSerializer):
    class Meta:
        model = Contract
        fields = ['id', 'signature_date', 'amount', 'payment_due_date', 'client']
