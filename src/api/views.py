from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from core.models import Address, Company, Employee, Client, Event, Contract
from core.permissions import CanGet, CanCreate, CanUpdate, CanDestroy
from .serializers import *

# Create your views here.
def check_permissions(method, action):
    if method == 'GET':
        return [CanGet]
    elif action == 'create':
        return [CanCreate]
    elif action == 'update':
        return [CanUpdate]
    elif action == 'destroy':
        return [CanDestroy]


class EmployeeViewSet(ModelViewSet):
    serializer_class = EmployeeDetailSerializer
    list_serializer_class = EmployeeListSerializer

    def get_permissions(self):
        method = self.request.method
        action = self.action
        self.permission_classes = check_permissions(method, action)
        return super().get_permissions()

    def get_queryset(self):
        queryset = Employee.objects.all()
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return self.list_serializer_class
        return super().get_serializer_class()


class ManagementEmployeesViewSet(EmployeeViewSet):
        def get_queryset(self):
            management_goup_id = 4
            if self.action == 'list':
                queryset = Client.objects.filter(group__contains=management_goup_id)
            else:
                raise Exception('Only list action request can be use on this request')
            return queryset


class ClientViewSet(ModelViewSet):
    serializer_class = ClientDetailSerializer
    list_serializer_class = ClientListSerializer

    def get_permissions(self):
        method = self.request.method
        action = self.action
        self.permission_classes = check_permissions(method, action)
        return super().get_permissions()

    def get_queryset(self):
        queryset = Client.objects.all()
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return self.list_serializer_class
        return super().get_serializer_class()


class MyClientsViewSet(ClientViewSet):
        def get_queryset(self):
            if self.action == 'list':
                queryset = Client.objects.filter(sales_contact=self.request.user.id)
            else:
                raise Exception('Only list action request can be use on this request')
            return queryset


class ContractViewSet(ModelViewSet):
    serializer_class = ContractDetailSerializer
    list_serializer_class = ContractListSerializer

    def get_permissions(self):
        method = self.request.method
        action = self.action
        self.permission_classes = check_permissions(method, action)
        return super().get_permissions()

    def get_queryset(self):
        queryset = Contract.objects.all()
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return self.list_serializer_class
        return super().get_serializer_class()


class MyContractsViewSet(ContractViewSet):
        def get_queryset(self):
            if self.action == 'list':
                my_contracts_queryset = Contract.objects.none()
                all_contracts_queryset = Contract.objects.all()
                for contract in all_contracts_queryset:
                    if contract.client == self.request.user.id:
                        my_contracts_queryset.append(contract)
            else:
                raise Exception('Only list action request can be use on this request')
            return my_contracts_queryset


class EventViewSet(ModelViewSet):
    serializer_class = EventDetailSerializer
    list_serializer_class = EventListSerializer

    def get_permissions(self):
        method = self.request.method
        action = self.action
        self.permission_classes = check_permissions(method, action)
        return super().get_permissions()

    def get_queryset(self):
        queryset = Event.objects.all()
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return self.list_serializer_class
        return super().get_serializer_class()


class MyEventsViewSet(ClientViewSet):
        def get_queryset(self):
            if self.action == 'list':
                queryset = Client.objects.filter(support_contact=self.request.user.id)
            else:
                raise Exception('Only list action request can be use on this request')
            return queryset


class CompanyViewSet(ModelViewSet):
    pass


class GroupViewSet(ModelViewSet):
    pass


class AddressViewSet(ModelViewSet):
    pass
