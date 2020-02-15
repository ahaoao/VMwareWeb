"""VMwareWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from Xadmin import urls as XadminUrls

from Reception.views import ErrorView, RegisterView, HomeView


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('admin/', include(XadminUrls)),
    path('error_404', ErrorView.as_view(), name='error'),
    # path('avatar', AvatarView.as_view(), name='avatar'),
    path('register', RegisterView.as_view(), name='register'),
    path('', HomeView.as_view(), name='home')

]
