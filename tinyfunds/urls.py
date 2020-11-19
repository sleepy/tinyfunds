"""tinyfunds URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import url
from django.views.generic import TemplateView
from .views import update_view
from .users import views as user_views
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('explore/', views.ExploreView.as_view(), name = 'explore'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('account/', TemplateView.as_view(template_name="account/account.html"), name='account'),
    path('account/edit', TemplateView.as_view(template_name="account/editAccount.html"), name='editAccount'),
    path('user/<int:pk>/', user_views.user, name='user'),
    path('event/<int:pk>/', views.EventView.as_view(), name='event'),
    path('explore/new', views.CreateEventView.as_view(), name='create_event'),
    path('event/edit/<int:pk>/', update_view, name='edit_event'),
    path('event/pledge/hours/<int:pk>/', views.pledge_hours, name='pledge_hours'),
    path('event/pledge/donation/<int:pk>/', views.pledge, name='pledge'),
    path('event/pledge/<int:pk>/confirm/', views.confirm, name='confirm'),
    path('event/confirm_paypal/', views.confirm_paypal, name='confirm_paypal'),
    path('event/donate/<int:pk>/<int:user_id>', views.donate, name='donate_event'),
    path('checkout/<int:pk>', views.checkout, name="checkout"),
    #url(r'^paypal/', include('paypal.standard.ipn.urls')),
]
