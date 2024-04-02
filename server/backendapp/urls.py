"""
URL configuration for backendapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:id>/', views.UserDetail.as_view(), name='user-detail'),
    path('customers/', views.CustomerList.as_view(), name='customer-list'),
    path('customers/<int:id>/', views.CustomerDetail.as_view(), name='customer-detail'),
    path('invoices/', views.InvoiceList.as_view(), name='invoice-list'),
    path('invoices/<int:id>/', views.InvoiceDetail.as_view(), name='invoice-detail'),
    path('packages/', views.PackageList.as_view(), name='package-list'),
    path('packages/<int:id>/', views.PackageDetail.as_view(), name='package-detail'),
    path('package-categories/', views.PackageCategoryList.as_view(), name='package-category-list'),
    path('package-categories/<int:id>/', views.PackageCategoryDetail.as_view(), name='package-category-detail'),
    path('package-statuses/', views.PackageStatusList.as_view(), name='package-status-list'),
    path('package-statuses/<int:id>/', views.PackageStatusDetail.as_view(), name='package-status-detail'),
]
