"""EpicEvent_CRM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter

from api.views import (
    EventViewSet, ContractViewSet, ClientViewSet, EmployeeViewSet, CompanyViewSet, GroupViewSet,
    AddressViewSet, ClientAssociationViewSet, EventAssociationViewSet
)


router = SimpleRouter()
router.register(r'employees', EmployeeViewSet, basename='employees')  # .../api/employees/
employee_router = NestedSimpleRouter(router, r'employees', lookup='employee')
employee_router.register(r'clients', ClientViewSet, basename='employee-clients')  # .../api/employees/<id>/clients/
employee_router.register(r'events', EventViewSet, basename='employee-events')  # .../api/employees/<id>/events/

router.register(r'clients', ClientViewSet, basename='clients')  # .../api/clients/

router.register(r'contracts', ContractViewSet, basename='contracts')  # .../api/contracts/

router.register(r'events', EventViewSet, basename='events')  # .../api/events/

router.register(r'clientassociations', ClientAssociationViewSet, basename='clientassociations')  # .../api/clientassociations/

router.register(r'eventassociations', EventAssociationViewSet, basename='eventassociations')  # .../apieventassociations/

router.register(r'companies', CompanyViewSet, basename='companies')  # .../api/companies/
company_router = NestedSimpleRouter(router, r'companies', lookup='company')
company_router.register(r'clients', ClientViewSet, basename='company-clients')  # .../api/companies/<id>/clients/

router.register(r'addresses', AddressViewSet, basename='addresses')  # .../api/addresses/

router.register(r'groups', GroupViewSet, basename='groups')  # .../api/groups/
group_router = NestedSimpleRouter(router, r'groups', lookup='group')
group_router.register(r'employees', EmployeeViewSet, basename='group-employees')  # .../api/groups/<id>/employees/
group_employee_router = NestedSimpleRouter(group_router, r'employees', lookup='employee')
group_employee_router.register(r'contracts', ContractViewSet, basename='saler-contracts')  # .../api/groups/<id>/employees/<id>/contracts/
group_employee_router.register(r'clients', ClientViewSet, basename='saler-clients')  # .../api/groups/<id>/employees/<id>/clients/
group_employee_router.register(r'events', EventViewSet, basename='support-events')  # .../api/groups/<id>/employees/<id>/events/


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
    path('api/', include(employee_router.urls)),
    path('api/', include(company_router.urls)),
    path('api/', include(group_router.urls)),
    path('api/', include(group_employee_router.urls)),
    path('api/', include('api.urls'))
]
