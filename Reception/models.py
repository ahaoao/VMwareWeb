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
    username = models.CharField(max_length=150, unique=True, verbose_name="用户名")
    password = models.CharField(max_length=128, verbose_name="密码")
    phone = models.CharField(max_length=11, verbose_name="电话")
    avatar = models.ImageField(upload_to="avatar/%Y%m%d/", blank=True, null=True, verbose_name="头像")
    add_date = models.DateTimeField(auto_now_add=True, verbose_name="注册时间")
    update_date = models.DateTimeField(verbose_name="更新时间", auto_now_add=True)
    status = models.PositiveIntegerField(choices=STATUS_ITEMS, default=STATUS_NORMAL, verbose_name="状态")

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