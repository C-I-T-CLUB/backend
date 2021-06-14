
from django.conf.urls import include
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/account/' ,include('account.urls')),
    path("api/v1/resources/" , include('resources.urls')),

]
