import datetime
import uuid

import uuid as uuid
from django.contrib.auth.hashers import make_password, check_password
from django.db import models


# Create your models here.
class User(models.Model):
    """用户表"""
    STATUS_NORMAL = 1
    STATUS_FROZEN = 2
    STATUS_DELETE = 3
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_FROZEN, '冻结'),
        (STATUS_DELETE, '删除'),
    )
    email = models.EmailField(primary_key=True, unique=True, verbose_name="邮箱")
    name = models.CharField(max_length=150, verbose_name="用户名")
    password = models.CharField(max_length=128, verbose_name="密码")
    phone = models.CharField(max_length=11, verbose_name="电话")
    avatar = models.ImageField(upload_to="avatar/%Y%m%d/", default='avatar/default_avatar.jpg', blank=True, null=True, verbose_name="头像")
    add_date = models.DateTimeField(auto_now_add=True, verbose_name="注册时间")
    update_date = models.DateTimeField(verbose_name="更新时间", auto_now_add=True)
    status = models.PositiveIntegerField(choices=STATUS_ITEMS, default=STATUS_FROZEN, verbose_name="状态")

    def __str__(self):
        return self.username

    def _set_password(self, password):
        # 加密密码
        self.password = make_password(password, None, 'pbkdf2_sha1')

    def _check_password(self, password):
        # 第一个参数为明文， 第二个参数为密文
        return check_password(password, self.password)

    class Meta:
        verbose_name_plural = "用户"


class EmailVerifyRecord(models.Model):
    """邮箱验证码表"""
    code = models.CharField(max_length=20, verbose_name="验证码")
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    # 包含注册验证和找回验证
    send_type = models.CharField(verbose_name="验证码类型", max_length=10,
                                 choices=(("register", "注册"), ("forget", "找回密码")))
    send_time = models.DateTimeField(verbose_name="发送时间", auto_now_add=True)

    class Meta:
        verbose_name_plural = "邮箱验证码"

    def __unicode__(self):
        return '{0}({1})'.format(self.code, self.email)