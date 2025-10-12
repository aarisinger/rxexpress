"""
URL configuration for refilltracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from rxexpress import views
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-patient/', views.patient_form_view, name='add_patient'),
    path('add-medication/', views.medication_form_view, name='add_medication'),
    path('add-prescription/', views.prescription_form_view, name='add_prescription'),
    # patient CRUD
    path('patients/', views.patient_list_view, name='patient_list'),
    path('patients/<int:pk>/', views.patient_detail_view, name='patient_detail'),
    path('patients/<int:pk>/edit/', views.patient_detail_view, name='patient_edit'),
    path('patients/<int:pk>/delete/', views.patient_delete_view, name='patient_delete'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
   

]

