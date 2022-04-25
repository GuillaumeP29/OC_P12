from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import Group

from core.models import Address, Company, Employee, Client, Event, Contract


class AddressListSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = ['number', 'street', 'city', 'country']


class AddressDetailSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'number', 'street', 'city', 'zip_code', 'country']


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
    address = AddressListSerializer()

    class Meta:
        model = Company
        fields = ['id', 'name', 'address']


class GroupNameSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']


class EmployeeListSerializer(ModelSerializer):
    groups = GroupNameSerializer(many=True)

    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'last_name', 'groups']


class EmployeeDetailSerializer(ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            'id', 'username', 'password', 'first_name', 'last_name', 'email', 'phone', 'mobile',
            'is_staff', 'date_updated', 'groups'
            ]

    def create(self, validated_data):
        employee = super(EmployeeDetailSerializer, self).create(validated_data)
        employee.set_password(validated_data['password'])
        employee.save()
        return employee


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


class ContractDetailSerializer(ModelSerializer):
    class Meta:
        model = Contract
        fields = ['id', 'signature_date', 'amount', 'payment_due_date', 'client']
