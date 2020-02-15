from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.shortcuts import render, reverse, redirect
from django.utils import timezone  # 引入timezone模块
from django.views.generic import ListView, TemplateView
from django.views import View

from .form import AdminLoginForm
from .models import AdminUser
from VMwareWeb.tools.checklogin import LoginRequiredMixin
# from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class LoginView(TemplateView):
    """管理端登陆视图"""
    queryset = []
    template_name = 'Xadmin/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'admin_login_form': AdminLoginForm,
        })
        return context

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            # user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            request.session['username'] = username
            return redirect('admin_index')
        else:
            context = self.get_context_data()
            context.update({
                "msg": "用户名或密码错误！"
            })
            return render(request, self.template_name, context=context)


class LogoutView(View):
    """管理端退出视图"""
    def get(self, request):
        logout(request)
        return redirect('admin_login')


class IndexView(LoginRequiredMixin, ListView):
    """管理端首页视图"""
    template_name = 'Xadmin/index.html'
    context_object_name = 'admin'

    def get_queryset(self):
        username = self.request.session.get('username')
        queryset = AdminUser.objects.get(Q(username=username) | Q(email=username))
        return queryset


class PanelView(IndexView):
    """系统面板视图"""
    queryset = []
    template_name = 'Xadmin/welcome1.html'


class MemberListView(IndexView):
    """会员列表视图"""
    queryset = []
    template_name = 'Xadmin/member-list.html'


class DeleteMemberView(IndexView):
    """会员删除视图"""
    template_name = 'Xadmin/member-del.html'


class GradeManageView(IndexView):
    """会员等级管理"""
    template_name = 'Xadmin/member-list1.html'


class HomeView(IndexView):
    """系统home视图"""
    template_name = 'Xadmin/welcome.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = {
            'admin': super().get_queryset(),
            'now_time': timezone.now()
        }
        return context


class UnicodeView(IndexView):
    """图标对应字体视图"""
    template_name = 'Xadmin/unicode.html'



