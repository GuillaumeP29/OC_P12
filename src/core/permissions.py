from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Group
from core.models import Client, Contract, Event, Employee, ClientAssociation


def is_superuser(user):
        return user.is_superuser


def get_obj_name(object):
    if (isinstance(object, Client)):
        return 'client'
    elif (isinstance(object, Contract)):
        print("On a bien un contrat !!!")
        return 'contract'
    elif (isinstance(object, Event)):
        return 'event'
    elif (isinstance(object, Employee)):
        return 'employee'
    elif (isinstance(object, Group)):
        return 'group'
    elif (isinstance(object, ClientAssociation)):
        return 'clientassociation'


def user_has_permission(user, obj, method_name):
    app_name = 'core'
    if (isinstance(obj, Group)):
        app_name = 'auth'
    object_name = get_obj_name(obj)
    permission_name = f'{app_name}.{method_name}_{object_name}'
    return user.has_perm(permission_name)


def is_in_charge_of(user, obj):
        if (isinstance(obj, Client)):
            return obj.sales_contact == user.id
        elif (isinstance(obj, Contract)):
            return obj.client.sales_contact == user.id
        elif (isinstance(obj, Event)):
            return obj.client.support_contact == user.id


def can_act(request, obj, method_name):
        user = request.user
        if is_superuser(user):
            return True
        elif user_has_permission(user, obj, method_name):
            return True
        elif is_in_charge_of(user, obj):
            return True
        else:
            return False


class CanGet(BasePermission):
    def has_object_permission(self, request, view, obj):
        method_name = "view"
        user = request.user
        if is_superuser(user):
            return True
        elif user_has_permission(user, obj, method_name):
            return True
        else:
            return False


class CanCreate(BasePermission):
    def has_object_permission(self, request, view, obj):
        method_name = "add"
        return can_act(request, obj, method_name)


class CanUpdate(BasePermission):
    def has_object_permission(self, request, view, obj):
        method_name = "change"
        return can_act(request, obj, method_name)


class CanDestroy(BasePermission):
    def has_object_permission(self, request, view, obj):
        method_name = "delete"
        return can_act(request, obj, method_name)
