from random import Random  # 用于生成随机码
from urllib.parse import urlsplit

from django.core.mail import send_mail  # 发送邮件模块
from django.shortcuts import resolve_url

from Reception.models import EmailVerifyRecord  # 邮箱验证model
from VMwareWeb.settings.base import EMAIL_FROM

import datetime


# 生成随机字符串
def random_str(randomlength=6):
    """
    随机字符串
    :param randomlength: 字符串长度
    :return: String 类型字符串
    """
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


# 发送电子邮件
def send_code_email(email, request, send_type="register"):
    """
    发送电子邮件
    :param email: 要发送的邮箱
    :param send_type: 邮箱类型
    :return: True/False
    """
    email_record = EmailVerifyRecord()
    # 将给用户发的信息保存在数据库中
    code = random_str(6)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.send_time = datetime.datetime.now()
    email_record.save()
    # 生成验证链接
    http = urlsplit(request.build_absolute_uri(None)).scheme
    # 获取当前域名
    host = request.META['HTTP_HOST']
    # 激活链接
    active_url = http + '://' + host + resolve_url("active_user", code, email)

    # 初始化为空
    email_title = ""
    email_body = ""
    # 如果为注册类型
    if send_type == "register":
        email_title = "注册激活-七彩祥云"
        html_message = '<p>尊敬的用户您好！</p>' \
                       '<p>感谢您使用七彩祥云。</p>' \
                       '<p>您的邮箱为：{0} 。请在5分钟内点击此链接激活您的邮箱：</p>' \
                       '<p style="color: red;"><a href="{1}">{2}<a></p>' \
                       '<br><br><br><br>' \
                       '--七彩祥云-大学生校园云主机提供平台'.format(email, active_url, active_url)
        email_body = ""
        # 发送邮件
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email], html_message=html_message)
        if not send_status:
            return False
    if send_type == "forget":
        email_title = "找回密码"
        email_body = "欢迎您使用七彩祥云平台，您的邮箱验证码为：{0}, 该验证码有效时间为两分钟，请及时进行验证。".format(code)
        # 发送邮件
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if not send_status:
            return False
    return True
