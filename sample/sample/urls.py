"""
URL configuration for sample project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('adlogin/', views.adlogin, name='adlogin'),
    path('addashboard/', views.addashboard, name='addashboard'),
    path('add_jobs/', views.add_jobs, name='add_jobs'),
    path('manage_jobs/', views.manage_jobs, name='manage_jobs'),
    path('applications/', views.applications, name='applications'),
    path('users/', views.users, name='users'),
    path('user_register/', views.user_register, name='user_register'),
    path('user_login/', views.user_login, name='user_login'),
    path('', views.user_home, name='user_home'),
    path('user_jobs/', views.user_jobs, name='user_jobs'),
    path('user_about/', views.user_about, name='user_about'),
    path('user_contact/', views.user_contact, name='user_contact'),
    path('user_apply_jobs/', views.user_apply_jobs, name='user_apply_jobs'),
    path('delete_data/<int:id>/', views.delete_data, name='delete_data'),
    path('user_application/', views.user_application, name='user_application'),
    path('edit_jobs/<int:id>/', views.edit_jobs, name='edit_jobs'),
    path('delete_user/<int:id>/', views.delete_user, name='delete_user'),
    path('delete_application/<int:id>/', views.delete_application, name='delete_application'),
    path('faq/', views.faq, name='faq'),
    path('delete_faq/<int:id>/', views.delete_faq, name='delete_faq'),
    path('issues/', views.issues, name='issues'),
    path('delete_issue/<int:id>/', views.delete_issue, name='delete_issue'),
    path('logout/', views.logout, name='logout'),
    path('client_logout/', views.client_logout, name='client_logout'),
    path('delete_application1/<int:id>/', views.delete_application1, name='delete_application1'),
    path('help_center/', views.help_center, name='help_center'),
    path('documentation/', views.documentation, name='documentation'),
    # report issue with optional job id
    path('report_issue/', views.report_issue, name='report_issue'),
    path('report_issue/<int:id>/', views.report_issue, name='report_issue'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('terms_services/', views.terms_services, name='terms_services'),
    path('cookie_policy/', views.cookie_policy, name='cookie_policy'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
