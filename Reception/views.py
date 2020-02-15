import json

from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from Reception.models import User


# Create your views here.
class ErrorView(TemplateView):
    """404页面视图"""
    template_name = '404/404.html'


# class AvatarView(TemplateView):
#     template_name = 'Reception/avatar.html'
#
#     def post(self, request):
#         avatar = request.FILES.get('avatar')
#         Avatar.objects.create(avatar=avatar)
#         return HttpResponse('上传成功')


class RegisterView(TemplateView):
    template_name = 'Reception/register.html'

    def post(self, request):
        print(request.body)
        print(request.POST)
        username = make_password(request.POST.get('username'))
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        # avatar = request.POST.get('avatar')
        context = {
            'user': None,
            'username_error': None,
            'email_error': None,
            'password_error': None,
            'phone_error': None,
        }
        if User.objects.filter(email=email):
            context['email_error'] = "邮箱已被绑定，请使用其他邮箱"
            return HttpResponse(json.dumps(context))
        elif User.objects.filter(username=username):
            context['username_error'] = "用户名已经存在"
        elif User.objects.filter(phone=phone):
            context['phone_error'] = "电话已经存在"
        # elif
            # User.objects.create(username=username, email=email, password=password)

            context['user'] = 'ok'
            return HttpResponse(json.dumps(context))


class HomeView(TemplateView):

    template_name = 'Reception/index.html'

