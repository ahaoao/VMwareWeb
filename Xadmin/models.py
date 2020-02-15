import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.contrib.auth.hashers import make_password, check_password

from Reception.models import User


# Create your models here.
class AdminUser(AbstractUser):
    """系统管理用户表"""
    phone = models.CharField(max_length=11)


class VCenter(models.Model):
    """VCenter表"""
    uuid = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False,
                            verbose_name="vCenter唯一标志")
    ip = models.GenericIPAddressField(unique=True, verbose_name="vCenter服务器IP地址")
    web_url = models.CharField(max_length=255, verbose_name="WebService入口地址")
    user = models.CharField(max_length=150, verbose_name="vCenter管理员账号")
    password = models.CharField(max_length=128, verbose_name="vCenter管理员账号密码")

    def __str__(self):
        """设置返回字符串"""
        return self.uuid

    @classmethod
    def get_all(cls):
        return cls.objects.all()

    def _set_password(self, password):
        # 加密密码
        self.password = make_password(password)

    def _check_password(self, password):
        # 第一个参数为明文， 第二个参数为密文
        return check_password(password, self.password)

    class Meta:
        verbose_name_plural = "VCenter"


class VirtualPlatform(models.Model):
    """虚拟化平台表"""
    uuid = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False,
                            verbose_name="虚拟化平台唯一标志")
    ip = models.GenericIPAddressField(unique=True, verbose_name="vCenter服务器IP地址")
    vCenter_uuid = models.ForeignKey(VCenter, on_delete=models.CASCADE, verbose_name="vCenter")
    user = models.CharField(max_length=150, verbose_name="虚拟化平台管理员账号")
    password = models.CharField(max_length=128, verbose_name="虚拟化平台管理员账号密码")
    cpu_amount = models.PositiveIntegerField(verbose_name="CPU数量")
    memory = models.PositiveIntegerField(verbose_name="内存大小(GB)")
    data_store = models.BigIntegerField(verbose_name="数据存储大小(GB)")
    cpu_free = models.PositiveIntegerField(verbose_name="剩余CPU数量")
    memory_free = models.PositiveIntegerField(verbose_name="剩余内存大小(GB)")
    data_store_free = models.PositiveIntegerField(verbose_name="剩余数据存储大小(GB)")

    def __str__(self):
        return self.ip

    def _set_password(self, password):
        # 加密密码
        self.password = make_password(password)

    def _check_password(self, password):
        # 第一个参数为明文， 第二个参数为密文
        return check_password(password, self.password)

    class Meta:
        verbose_name_plural = "虚拟化平台"


class VirtualMachine(models.Model):
    """虚拟机表"""
    # from Reception.models import User

    uuid = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False,
                            verbose_name="虚拟机唯一标志")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    virtual_platform_uuid = models.ForeignKey(VirtualPlatform, on_delete=models.CASCADE, verbose_name="虚拟化平台")
    cpu = models.PositiveIntegerField(verbose_name="CPU个数")
    memory = models.PositiveIntegerField(verbose_name="内存大小")
    disk = models.PositiveIntegerField(verbose_name="虚拟磁盘大小")
    ip = models.OneToOneField('IpPool', verbose_name="IP地址", on_delete=models.CASCADE)
    template = models.ForeignKey('Template', verbose_name="虚拟机模板", on_delete=models.CASCADE)

    def __str__(self):
        return self.uuid


class IpPool(models.Model):
    """IP地址表"""
    ip = models.GenericIPAddressField(verbose_name="IP地址")
    # virtual_machine = models.ForeignKey(VirtualMachine, verbose_name="虚拟机", on_delete=models.CASCADE)


class Template(models.Model):
    """虚拟机模板表"""
    name = models.CharField(verbose_name="模板名称", max_length=255)
    path = models.CharField(verbose_name="保存路径", max_length=255)


class Snapshot(models.Model):
    """快照表"""
    uuid = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False,
                            verbose_name="快照UUID")
    # owner = models.ForeignKey(VirtualMachine, verbose_name="虚拟机", on_delete=models.CASCADE)
    owner = models.OneToOneField(VirtualMachine, verbose_name="虚拟机", on_delete=models.CASCADE)
    parent = models.UUIDField(verbose_name="父快照UUID")




