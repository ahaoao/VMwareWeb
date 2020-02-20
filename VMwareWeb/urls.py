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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from Xadmin import urls as XadminUrls
from .settings import base

from Reception.views import (
    ErrorView,  # RegisterView,
    IndexView, GetValidCodeImgView,
    LoginView, SignUpView, LogoutView,
    ActiveUserEmail, ActiveUserAgain,
)

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('admin/', include(XadminUrls)),
    path('error_404', ErrorView.as_view(), name='error'),
    # path('avatar', AvatarView.as_view(), name='avatar'),
    # path('register', RegisterView.as_view(), name='register'),
    path('signup', SignUpView.as_view(), name='sign_up'),
    path('', IndexView.as_view(), name='index'),
    path('get_valid_code_img', GetValidCodeImgView.as_view(), name='valid_code_img'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('active_user_email.html&token=<str:email_code>&<str:email>', ActiveUserEmail.as_view(), name='active_user'),
    path('active_user_again', ActiveUserAgain.as_view(), name='active_user_again'),

] + static(base.MEDIA_URL, document_root=base.MEDIA_ROOT)

# 加载媒体文件
# urlpatterns += static(base.MEDIA_URL, document_root=base.MEDIA_ROOT)
