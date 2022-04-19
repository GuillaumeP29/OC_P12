from django.urls import path

from . import views

urlpatterns = [
    path('', views.LoginPage.as_view(), name='login'),
    path('login/', views.LoginPage.as_view(), name='login'),
]
