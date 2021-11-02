"""RealEstate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from webscrape import views as scrape_views
from dataprocess import views as proc_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', proc_views.home, name ='home'),
    path('model', proc_views.model, name ='model'),
    path('analysis', proc_views.analysis, name ='analysis'),
    path('update', proc_views.update, name ='update'),
    path('scrape/', scrape_views.land_scrape, name ='scrape'),
    path('price-form/', proc_views.get_land, name ='price-form'),
    path('report/<int:search_id>/', proc_views.show_report, name='price-report'),
    path('register/', proc_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='dataprocess/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='dataprocess/logout.html'), name='logout')

]
