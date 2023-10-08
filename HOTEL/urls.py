"""Hotel URL Configuration

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
from django.urls import path
from hotelbot import views as botviews
from booking import views as bookingviews

urlpatterns = [
    path('', bookingviews.index, name='index'),
    path('admin/', admin.site.urls),
    path('index/', bookingviews.index, name='index'),
    path('enhanced/', bookingviews.enhanced, name='enhanced'),
    path('booking/<str:room_type>/', bookingviews.booking, name='booking'),
    path('roomsearch/', bookingviews.form_searchroom, name='datesearch'), 
    path('openCodeScaner/', bookingviews.openCodeScaner, name='openCodeScaner'), 
    path('updateUserInfo/', bookingviews.form_Userinfo, name='updateUserInfo'), 
    path('callback', botviews.callback),  
    path('confirm', botviews.confirmed, name= 'Confirm'),
    
]
