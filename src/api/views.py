from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated

from core.models import Address, Company, Group, Employee, Client, Event, Contract
from serializers import *

# Create your views here.
# class ProjectViewSet(ModelViewSet):
#     serializer_class = ProjectDetailSerializer
#     list_serializer_class = ProjectListSerializer

#     def get_permissions(self):
#         if self.action == ('update' or 'destroy'):
#             self.permission_classes = [IsAuthorOrOwner, ]
#         else:
#             self.permission_classes = [IsContributor, ]
#         return super().get_permissions()

#     def get_queryset(self):
#         user = self.request.user
#         queryset = Project.objects.all()
#         if user.is_superuser:
#             return queryset
#         else:
#             user_contributions = Contributor.objects.filter(user=user.id)
#             user_contributions_id_list = []
#             for contribution in user_contributions:
#                 user_contributions_id_list.append(contribution.project.id)
#             print(user_contributions_id_list)
#             queryset = queryset.filter(id__in=user_contributions_id_list)
#             return queryset

#     def get_serializer_class(self):
#         if self.action == 'list':
#             return self.list_serializer_class
#         return super().get_serializer_class()


class EventViewSet(ModelViewSet):
    pass


class ContractViewSet(ModelViewSet):
    pass


class EmployeeViewSet(ModelViewSet):
    pass


class ClientViewSet(ModelViewSet):
    pass


class CompanyViewSet(ModelViewSet):
    pass


class GroupViewSet(ModelViewSet):
    pass


class AddressViewSet(ModelViewSet):
    serializer_class = AddressDetailSerializer
    list_serializer_class = AdressListSerializer

    def get_permissions(self):
        if self.action == ('update' or 'destroy'):
            self.permission_classes = []
        else:
            self.permission_classes = []
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        queryset = Address.objects.all()
