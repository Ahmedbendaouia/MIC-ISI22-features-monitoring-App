"""video_acquisition URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf.urls import handler404, handler500
from django.contrib import admin 
from django.urls import path,include
from . import views 

urlpatterns = [
    path('', views.home),   
    path('admin/', admin.site.urls),
    path('video_detection/',include('video_detection.urls')),        
    path("login/", views.loginPage,name='login'),
    path("logout/", views.logoutPage,name='logout')    
]

handler404 = views.error_404