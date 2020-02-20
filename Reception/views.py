import datetime
from urllib.parse import urlsplit
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect, resolve_url
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView

from Reception.models import User, EmailVerifyRecord


# Create your views here.
from VMwareWeb.tools.email_send import send_code_email


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


# class RegisterView(TemplateView):
#     template_name = 'Reception/register.html'
#
#     def post(self, request):
#         print(request.body)
#         print(request.POST)
#         username = make_password(request.POST.get('username'))
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
#         password = request.POST.get('password')
#         # avatar = request.POST.get('avatar')
#         context = {
#             'user': None,
#             'username_error': None,
#             'email_error': None,
#             'password_error': None,
#             'phone_error': None,
#         }
#         if User.objects.filter(email=email):
#             context['email_error'] = "邮箱已被绑定，请使用其他邮箱"
#             return HttpResponse(json.dumps(context))
#         elif User.objects.filter(username=username):
#             context['username_error'] = "用户名已经存在"
#         elif User.objects.filter(phone=phone):
#             context['phone_error'] = "电话已经存在"
#             # elif
#             # User.objects.create(username=username, email=email, password=password)
#
#             context['user'] = 'ok'
#             return HttpResponse(json.dumps(context))


class IndexView(TemplateView):
    """用户端首页"""
    template_name = 'Reception/index.html'


def get_random_color():
    """随机取颜色"""
    import random
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


class GetValidCodeImgView(View):
    """获取验证码图片视图"""

    def get(self, request):
        from PIL import Image, ImageDraw, ImageFont  # pillow模块
        from io import BytesIO
        import random

        img = Image.new("RGB", (180, 60), color=get_random_color())
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("VMwareWeb/themes/bootstrap/static/Reception/fonts/Impact.ttf", size=32)
        valid_code_str = ""
        for i in range(4):
            random_num = str(random.randint(0, 9))  # 随机数字
            random_low_alpha = chr(random.randint(97, 122))  # 随机小写字母
            random_upper_alpha = chr(random.randint(65, 90))  # 随机大写字母
            random_char = random.choice([random_num, random_low_alpha, random_upper_alpha])
            draw.text(((i + 1) * 25 + 20, 8), random_char, get_random_color(), font=font)
            valid_code_str += random_char

        for i in range(40):
            # 噪点
            draw.point([random.randint(0, 180), random.randint(0, 60)], fill=get_random_color())

        for i in range(10):
            # 直线
            x1 = random.randint(0, 180)
            y1 = random.randint(0, 60)
            x2 = random.randint(0, 180)
            y2 = random.randint(0, 60)
            draw.line((x1, y1, x2, y2), fill=get_random_color())

        # 方式2：内存操作
        f = BytesIO()
        img.save(f, "png")
        data = f.getvalue()
        request.session["valid_code_str"] = valid_code_str
        """
            1.生成随机字符串: sdfsdfdfkg
            2.COOKIE {"seesionid": sdfsdfdfkg}
            3.django-session
                session-key          session-data
                sdfsdfdfkg           {"valid_code_str": valid_code_str}
        """
        return HttpResponse(data)


class LoginView(TemplateView):
    """用户登陆视图"""

    def post(self, request):
        response = {
            "user": None,
            "msg": None,
        }
        email = request.POST.get("email")
        password = request.POST.get("password")
        valid_code = request.POST.get("valid_code")  # 用户输入的验证码
        valid_code_str = request.session.get("valid_code_str")  # 系统生成的验证码
        if email == '':
            response["msg"] = "邮箱不能为空！"
        elif valid_code.upper() == valid_code_str.upper():  # 判断验证码，不区分大小写
            try:
                user = User.objects.get(email=email)
                if user.status != User.STATUS_NORMAL:
                    response["msg"] = "当前用户未激活，请前往邮箱激活！"
                    return JsonResponse(response)
                if user._check_password(password):
                    request.session.update({
                        'is_login': True,
                        'user_name': user.name,
                        'user_email': user.email,
                        'user_avatar': str(user.avatar.url),
                    })
                    response["user"] = user.email
                    response["msg"] = "登陆成功！"
                else:
                    response['msg'] = "密码不正确！"
            except User.DoesNotExist:
                response["msg"] = "邮箱不存在"
        else:
            response["msg"] = "验证码错误！"

        return JsonResponse(response)


class LogoutView(View):
    """用户退出视图"""
    def get(self, request):
        request.session.clear()
        return redirect('index')


class SignUpView(View):
    """用户注册视图"""
    def post(self, request):
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        response = {
            "user": None,
            "msg": None,
        }
        try:
            if email == '':
                response["msg"] = "邮箱不能为空！"
            elif User.objects.get(email=email):
                response['msg'] = "邮箱已经存在!"
        except User.DoesNotExist:
            if password1 != password2:
                response["msg"] = "两次密码输入不一致！"
            else:
                # 发送邮箱
                send_email = send_code_email(email, request)
                if send_email:
                    # 注册用户信息，状态设置为冻结
                    User.objects.create(email=email, password=make_password(password1, None, 'pbkdf2_sha1'))
                    response["msg"] = "注册成功,请前往邮箱验证"
                    response["user"] = "ok"
                else:
                    response["msg"] = "验证码发送失败，请稍后重试！"
        return JsonResponse(response)


class ActiveUserEmail(View):
    """用户邮箱激活视图"""
    template_name = 'Reception/active_user.html'

    def get(self, request, *args, **kwargs):
        response = {
            "msg": None,
            "status": True,
        }
        email_code = self.kwargs.get('email_code')
        email = self.kwargs.get('email')
        # 将email加入到session中，验证失败时从session获取email
        request.session.update({
            'email': email,
        })
        try:
            database_email_code = EmailVerifyRecord.objects.get(Q(code=email_code) & Q(email=email))
            send_time = database_email_code.send_time
            # 点击激活链接的时间
            clock_url_time = timezone.now()
            # print((clock_url_time-effective_time).seconds)
            # 时间差(秒数)< 300(5分钟)为有效期
            if (clock_url_time-send_time).seconds < 300:
                # 将用户状态设置为正常状态
                User.objects.filter(email=email).update(status=User.STATUS_NORMAL)
                response["msg"] = "激活成功，欢迎使用七彩祥云"
            else:
                response["msg"] = "验证码过期，点击重新发送验证链接"
                response["status"] = False
        except database_email_code.DoesNotExist:
            response["msg"] = "验证码无效，点击重新发送验证链接"
            response["status"] = False

        return render(request, self.template_name, context=response)


class ActiveUserAgain(View):
    """验证链接过期,重新发送"""
    def get(self, request):
        response = {
            "msg": None,
        }
        email = request.session.get("email")  # 从url中获取email
        try:
            send_email = send_code_email(email, request)
            if send_email:
                response["msg"] = "发送成功，请前往邮箱进行验证"
            else:
                response["msg"] = "发送失败，请联系管理员"
        except:
            response["msg"] = "出现异常，请联系管理员"

        return JsonResponse(response)








