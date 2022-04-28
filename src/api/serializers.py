from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import Group, Permission
import datetime

from core.models import Address, Company, Employee, Client, Event, Contract, ClientAssociation, EventAssociation


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


class CompanyPostSerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'address']


class PermissionSerializer(ModelSerializer):
    class Meta:
        model = Permission
        fields = ['name']


class GroupDetailSerializer(ModelSerializer):
    permissions = PermissionSerializer(many=True)
    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions']


class GroupListSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']


class EmployeeListSerializer(ModelSerializer):
    groups = GroupListSerializer(many=True)

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


class SalerSerializer(ModelSerializer):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name']


class ClientDetailSerializer(ModelSerializer):
    company = CompanyDetailSerializer()
    sales_contact = SalerSerializer(many=True)

    class Meta:
        model = Client
        fields = ['id', 'last_name', 'first_name', 'email', 'phone', 'mobile', 'company', 'sales_contact']


class ClientPostSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'last_name', 'first_name', 'email', 'phone', 'mobile', 'company']


class EventStatusSerializer(ModelSerializer):
    class Meta:
        model = Event.EventStatus
        fields = ['name']


class EventListSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = ['name', 'contract', 'event_status', 'event_date']


class EventDetailSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = ['name', 'contract', 'event_status', 'attendees', 'event_date', 'notes']


class EventPostSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = ['name', 'contract', 'attendees', 'event_date', 'notes']

    def validate_contract(self, value):
        """Check if the contract has been signed"""
        signed_contracts_id_list = []
        signed_contracts = Contract.objects.exclude(signature_date__isnull=True)
        for contract in signed_contracts:
            signed_contracts_id_list.append(contract.id)
        if value.id in signed_contracts_id_list:
            return value
        else:
            raise serializers.ValidationError('An event cannot be created for an unsigned contract')

    def create(self, validated_data):
        if validated_data.get('event_date') is not None:
            validated_data['event_status'] = Event.EventStatus.objects.get(pk='Planned')
        event = super(EventPostSerializer, self).create(validated_data)
        event.save()
        return event


class ContractListSerializer(ModelSerializer):
    class Meta:
        model = Contract
        fields = ['id', 'client']


class ContractDetailSerializer(ModelSerializer):
    class Meta:
        model = Contract
        fields = ['id', 'signature_date', 'amount', 'payment_due_date', 'client']


class ClientAssociationSerializer(ModelSerializer):
    class Meta:
        model = ClientAssociation
        fields = ['id', 'employee', 'client']

    def validate_client(self, value):
        """Revoke other assigned saler, to be sure the client has only one active sales_contact"""
        for assigned_saler in ClientAssociation.objects.filter(client=value):
            if assigned_saler.date_revoked is None:
                assigned_saler.date_revoked = datetime.datetime.now()
                assigned_saler.save()
        return value
    
    def validate_employee(self, value):
        """check that the employee is a saler"""
        saler_goup_id = 2
        salers_id_list = []
        for saler in Employee.objects.filter(groups=saler_goup_id):
            salers_id_list.append(saler.id)
        if value.id in salers_id_list:
            return value
        else:
            raise serializers.ValidationError("The assigned employee must be a saler")


class EventAssociationSerializer(ModelSerializer):
    class Meta:
        model =  EventAssociation
        fields = ['id', 'employee', 'event']

    def validate_event(self, value):
        """Revoke other assigned support, to be sure the event has only one active support"""
        for assigned_support in  EventAssociation.objects.filter(event=value):
            if assigned_support.date_revoked is None:
                assigned_support.date_revoked = datetime.datetime.now()
                assigned_support.save()
        return value
    
    def validate_employee(self, value):
        """check that the employee is a support"""
        support_goup_id = 3
        supports_id_list = []
        for support in Employee.objects.filter(groups=support_goup_id):
            supports_id_list.append(support.id)
        if value.id in supports_id_list:
            return value
        else:
            raise serializers.ValidationError("The assigned employee must be a support")
