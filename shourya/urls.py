"""
URL configuration for shourya project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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

from fooddonation import views
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('ngo/', views.ngo_view, name='ngo'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('create-donation/', views.create_donation_view, name='create_donation'),
    path('claim-donation/<int:donation_id>/', views.claim_donation_view, name='claim_donation'),
    path('logout/', views.logout_view, name='logout'),
    path(
           'forgot-password/',
           auth_views.PasswordResetView.as_view(
            template_name='forgot_password.html'
        ),
        name='password_reset'
         ),
          path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    path(
        'password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),
       path(
        'password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / 'fooddonation' / 'static')
