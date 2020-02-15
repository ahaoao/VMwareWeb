from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.decorators import method_decorator

from Xadmin.models import AdminUser


class LoginRequiredMixin(object):
    """定义验证用户是否登录扩展类"""
    @classmethod
    def as_view(cls, **kwargs):
        view = super().as_view(**kwargs)
        # 未登陆时跳转到登陆页面
        return login_required(view, login_url='/admin/login')


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 设置用户名和邮箱登陆
            admin_user = AdminUser.objects.get(Q(username=username) | Q(email=username))
            if admin_user.check_password(password):
                return admin_user
        except Exception as e:
            return None

