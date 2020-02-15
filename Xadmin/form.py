from django import forms

from .models import User


class AdminLoginForm(forms.ModelForm):
    """管理员登陆表单"""
    username = forms.CharField(
        label='用户名',
        max_length=150,
        widget=forms.widgets.Input(
            attrs={
                'name': 'username',
                'placeholder': '用户名',
                'type': 'text',
                'class': 'layui-input',
                'lay-verify': 'required',
            }
        )
    )
    password = forms.CharField(
        label='密码',
        max_length=128,
        widget=forms.widgets.Input(
            attrs={
                'lay-verify': "required",
                'type': 'password',
                'class': 'layui-input',
            }
        )
    )

    class Meta:
        model = User
        # 控制在网页显示的字段
        fields = ['username', 'password']