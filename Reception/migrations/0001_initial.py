# Generated by Django 2.2 on 2020-02-19 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailVerifyRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, verbose_name='验证码')),
                ('email', models.EmailField(max_length=50, verbose_name='邮箱')),
                ('send_type', models.CharField(choices=[('register', '注册'), ('forget', '找回密码')], max_length=10, verbose_name='验证码类型')),
                ('send_time', models.DateTimeField(auto_now_add=True, verbose_name='发送时间')),
            ],
            options={
                'verbose_name_plural': '邮箱验证码',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False, unique=True, verbose_name='邮箱')),
                ('name', models.CharField(max_length=150, verbose_name='用户名')),
                ('password', models.CharField(max_length=128, verbose_name='密码')),
                ('phone', models.CharField(max_length=11, verbose_name='电话')),
                ('avatar', models.ImageField(blank=True, default='avatar/default_avatar.jpg', null=True, upload_to='avatar/%Y%m%d/', verbose_name='头像')),
                ('add_date', models.DateTimeField(auto_now_add=True, verbose_name='注册时间')),
                ('update_date', models.DateTimeField(auto_now_add=True, verbose_name='更新时间')),
                ('status', models.PositiveIntegerField(choices=[(1, '正常'), (2, '冻结'), (3, '删除')], default=1, verbose_name='状态')),
            ],
            options={
                'verbose_name_plural': '用户',
            },
        ),
    ]
