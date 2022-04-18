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

from api.views import EventViewSet, ContractViewSet, ClientViewSet, EmployeeViewSet, CompanyViewSet, GroupViewSet


router = SimpleRouter()
router.register(r'events', EventViewSet, basename='events')

router.register(r'contracts', ContractViewSet, basename='contracts')

router.register(r'employees', EmployeeViewSet, basename='employees')

router.register(r'clients', ClientViewSet, basename='clients')

router.register(r'companies', CompanyViewSet, basename='companies')
company_router = NestedSimpleRouter(router, r'companies', lookup='company')
company_router.register(r'clients', ClientViewSet, basename='company-clients')

router.register(r'groups', GroupViewSet, basename='groups')
groups_router = NestedSimpleRouter(router, r'groups', lookup='group')
groups_router.register(r'employees', EmployeeViewSet, basename='group-employees')
group_employees_router = NestedSimpleRouter(groups_router, r'employees', lookup='employee')
group_employees_router.register(r'contracts', ContractViewSet, basename='saler-contracts')
group_employees_router.register(r'clients', ClientViewSet, basename='saler-clients')
group_employees_router.register(r'events', EventViewSet, basename='support-events')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
    path('core/', include('core.urls'))
]
