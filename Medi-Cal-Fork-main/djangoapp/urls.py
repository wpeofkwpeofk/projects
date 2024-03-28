"""
URL configuration for djangoapp project.

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
from django.urls import include, path
from core import views


#any url starting with schedule gets routed to that app's url file
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.default.as_view(), name="default"),
    path('home/',views.home.as_view(), name = 'home'),
    path('signup/', views.signup.as_view(), name='signup'),
    path('signin/',views.signin.as_view(), name = 'signin'),
    path('activate/',views.activate.as_view(), name = 'activate'),
    path('index/',views.index.as_view(), name = 'index'),
    path('masterschedule/',views.masterschedule.as_view(), name = 'masterschedule'),
    path('appointment/',views.appointment.as_view(), name = 'appointment'),
    path('personschedule/',views.personschedule.as_view(), name = 'personschedule'),
]

from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns