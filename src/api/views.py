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
    elif action == 'update' or 'patch':
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
            queryset = Employee.objects.filter(groups__contains=management_goup_id)
        else:
            raise Exception('Only list action request can be use on this request')
        return queryset


class ClientViewSet(ModelViewSet):
    serializer_class = ClientDetailSerializer
    list_serializer_class = ClientListSerializer
    post_serializer_class = ClientPostSerializer

    def get_permissions(self):
        method = self.request.method
        action = self.action
        self.permission_classes = check_permissions(method, action)
        return super().get_permissions()

    def get_queryset(self):
        status = self.request.GET.get('status')
        if status is None:
            queryset = Client.objects.all()
        else:
            queryset = Client.objects.filter(sales_contact=self.request.user.id)
            if status == 'contacts':
                pass
            elif status == 'contracted-clients':
                signed_contract_clients_id_list = []
                for contract in Contract.objects.all():
                    if contract.signature_date is not None:
                        signed_contract_clients_id_list.append(contract.client_id)
                queryset = queryset.filter(id__in=signed_contract_clients_id_list)
            else:
                contract_clients_id_list = []
                for contract in Contract.objects.all():
                    contract_clients_id_list.append(contract.client_id)
                if status == 'prospects':
                    contract_clients_id_list = []
                    for contract in Contract.objects.all():
                        contract_clients_id_list.append(contract.client_id)
                    queryset = queryset.exclude(id__in=contract_clients_id_list)
                elif status == 'clients':
                    queryset = queryset.filter(id__in=contract_clients_id_list)
                else:
                    raise ValueError(
                        """The 'status' parameter must be either empty, either has one of the following values :
                        'contacts', 'prospects', 'clients', 'contracted-clients'"""
                     )
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return self.list_serializer_class
        elif self.request.method == 'POST':
            return self.post_serializer_class
        return super().get_serializer_class()


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
    post_serializer_class = EventPostSerializer

    def get_permissions(self):
        method = self.request.method
        action = self.action
        self.permission_classes = check_permissions(method, action)
        return super().get_permissions()

    def get_queryset(self):
        status = self.request.GET.get('status')
        if status is None:
            queryset = Event.objects.all()
        else:
            queryset = Event.objects.filter(support_contact=self.request.user.id)
            if status == 'all':
                pass
            elif status == 'planned':
                queryset = queryset.filter(event_status='Planned')
            elif status == 'on-going':
                queryset = queryset.filter(event_status='On going')
            elif status == 'canceled':
                queryset = queryset.filter(event_status='Canceled')
            elif status == 'achieved':
                queryset = queryset.filter(event_status='Achieved')
            else:
                raise ValueError(
                    """The 'status' parameter must be either empty, either has one of the following values :
                    'on-going', 'planned', 'canceled', 'achieved'"""
                    )
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return self.list_serializer_class
        elif self.request.method == 'POST':
            return self.post_serializer_class
        return super().get_serializer_class()


class MyEventsViewSet(ClientViewSet):
    def get_queryset(self):
        if self.action == 'list':
            queryset = Client.objects.filter(support_contact=self.request.user.id)
        else:
            raise Exception('Only list action request can be use on this request')
        return queryset


class CompanyViewSet(ModelViewSet):
    serializer_class = CompanyDetailSerializer
    list_serializer_class = CompanyListSerializer
    post_serializer_class = CompanyPostSerializer

    def get_permissions(self):
        method = self.request.method
        action = self.action
        self.permission_classes = check_permissions(method, action)
        return super().get_permissions()

    def get_queryset(self):
        queryset = Company.objects.all()
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return self.list_serializer_class
        elif self.request.method == 'POST':
            return self.post_serializer_class
        return super().get_serializer_class()


class GroupViewSet(ModelViewSet):
    serializer_class = GroupDetailSerializer
    list_serializer_class = GroupListSerializer

    def get_permissions(self):
        method = self.request.method
        action = self.action
        self.permission_classes = check_permissions(method, action)
        return super().get_permissions()

    def get_queryset(self):
        queryset = Group.objects.all()
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return self.list_serializer_class
        return super().get_serializer_class()


class AddressViewSet(ModelViewSet):
    serializer_class = AddressDetailSerializer
    list_serializer_class = AddressListSerializer

    def get_permissions(self):
        method = self.request.method
        action = self.action
        self.permission_classes = check_permissions(method, action)
        return super().get_permissions()

    def get_queryset(self):
        queryset = Address.objects.all()
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return self.list_serializer_class
        return super().get_serializer_class()

class ClientAssociationViewSet(ModelViewSet):
    serializer_class = ClientAssociationSerializer

    def get_permissions(self):
        method = self.request.method
        action = self.action
        self.permission_classes = check_permissions(method, action)
        return super().get_permissions()

    def get_queryset(self):
        queryset = ClientAssociation.objects.all()
        return queryset

class EventAssociationViewSet(ModelViewSet):
    serializer_class = EventAssociationSerializer

    def get_permissions(self):
        method = self.request.method
        action = self.action
        self.permission_classes = check_permissions(method, action)
        return super().get_permissions()

    def get_queryset(self):
        queryset = EventAssociation.objects.all()
        return queryset
